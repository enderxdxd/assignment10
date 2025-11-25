import os
import random
import requests
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import ContinentForm
from .helpers import save_search_to_mongo, get_search_history

REST_COUNTRIES_URL = "https://restcountries.com/v3.1/region/{continent}"
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

def home(request):
    """
    Exibe o formulário para o usuário escolher o continente.
    """
    if request.method == 'POST':
        form = ContinentForm(request.POST)
        if form.is_valid():
            continent = form.cleaned_data['continent']
            # Redireciona para a view de resultados, passando o continente na querystring
            return redirect('search_results') + f'?continent={continent}'
    else:
        form = ContinentForm()

    return render(request, 'continent_form.html', {'form': form})


def search_results(request):
    """
    Recebe o continente, chama REST Countries, escolhe 5 países aleatórios,
    consulta o clima das capitais no OpenWeather e salva tudo no MongoDB.
    """
    continent = request.GET.get('continent')
    error_message = None
    weather_data = []

    if not continent:
        error_message = "No continent provided."
        return render(request, 'search_results.html', {
            'error_message': error_message,
            'weather_data': weather_data,
            'continent': None,
        })

    # 1. REST Countries: pegar países do continente
    try:
        response = requests.get(REST_COUNTRIES_URL.format(continent=continent), timeout=10)
        response.raise_for_status()
        countries_json = response.json()
    except requests.RequestException as e:
        error_message = f"Error fetching countries data: {e}"
        return render(request, 'search_results.html', {
            'error_message': error_message,
            'weather_data': weather_data,
            'continent': continent,
        })

    # Filtra países que têm capital
    valid_countries = [
        c for c in countries_json
        if c.get('capital') and isinstance(c.get('capital'), list)
    ]

    if len(valid_countries) < 5:
        error_message = "Not enough countries with capital found for this continent."
        return render(request, 'search_results.html', {
            'error_message': error_message,
            'weather_data': weather_data,
            'continent': continent,
        })

    # Seleciona 5 aleatórios
    selected_countries = random.sample(valid_countries, 5)

    api_key = settings.OPENWEATHERMAP_API_KEY
    if not api_key or api_key == 'COLOQUE_SUA_KEY_AQUI':
        error_message = "OpenWeatherMap API key is not configured."
        return render(request, 'search_results.html', {
            'error_message': error_message,
            'weather_data': weather_data,
            'continent': continent,
        })

    # 2. Para cada país, buscar clima da capital
    for country in selected_countries:
        country_name = country.get('name', {}).get('common', 'Unknown')
        capital_list = country.get('capital', [])
        capital = capital_list[0] if capital_list else 'Unknown'
        population = country.get('population', 'Unknown')
        latlng = country.get('latlng', ['N/A', 'N/A'])

        city_weather = {
            'country': country_name,
            'capital': capital,
            'population': population,
            'latitude': latlng[0] if len(latlng) > 0 else 'N/A',
            'longitude': latlng[1] if len(latlng) > 1 else 'N/A',
            'temperature': None,
            'description': None,
            'icon': None,
            'error': None,
        }

        # Chamada ao OpenWeather
        try:
            params = {
                'q': capital,
                'appid': api_key,
                'units': 'metric'
            }
            weather_response = requests.get(OPENWEATHER_URL, params=params, timeout=10)
            weather_response.raise_for_status()
            w_json = weather_response.json()

            city_weather['temperature'] = w_json.get('main', {}).get('temp')
            city_weather['description'] = w_json.get('weather', [{}])[0].get('description')
            city_weather['icon'] = w_json.get('weather', [{}])[0].get('icon')

        except requests.RequestException as e:
            city_weather['error'] = f"Error fetching weather: {e}"
        except Exception as e:
            city_weather['error'] = f"Unexpected error: {e}"

        weather_data.append(city_weather)

    # 3. Salvar no MongoDB
    try:
        save_search_to_mongo(continent, weather_data)
    except Exception as e:
        # Não quebra o app se o Mongo der erro; apenas mostra a mensagem
        error_message = error_message or f"Warning: could not save history to MongoDB ({e})."

    return render(request, 'search_results.html', {
        'continent': continent,
        'weather_data': weather_data,
        'error_message': error_message,
    })


def history_view(request):
    """
    Mostra as últimas buscas salvas no MongoDB.
    """
    try:
        history_records = get_search_history(limit=10)
        error_message = None
    except Exception as e:
        history_records = []
        error_message = f"Error reading history from MongoDB: {e}"

    return render(request, 'history.html', {
        'history_records': history_records,
        'error_message': error_message,
    })
