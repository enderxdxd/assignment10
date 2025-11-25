from django.conf import settings
from pymongo import MongoClient
from datetime import datetime

def get_mongo_collection():
    client = MongoClient(settings.MONGODB_URI)
    db = client[settings.MONGODB_DB_NAME]
    collection = db[settings.MONGODB_COLLECTION_NAME]
    return collection

def save_search_to_mongo(continent, results):
    """
    Salva uma busca no MongoDB como um documento JSON.
    results deve ser uma lista de dicionários com informações dos países/climas.
    """
    collection = get_mongo_collection()
    doc = {
        "continent": continent,
        "results": results,
        "created_at": datetime.utcnow()
    }
    collection.insert_one(doc)

def get_search_history(limit=10):
    """
    Recupera as últimas buscas feitas, ordenadas por data decrescente.
    """
    collection = get_mongo_collection()
    cursor = collection.find().sort("created_at", -1).limit(limit)
    return list(cursor)
