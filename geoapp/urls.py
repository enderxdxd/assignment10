from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('results/', views.search_results, name='search_results'),
    path('history/', views.history_view, name='history'),
]
