import os
from dotenv import load_dotenv
from langchain.tools import tool
import requests
from urllib.parse import urlparse

load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")


def portugal_source(url):
    # Retorna True se a URL for de Portugal (.pt)
    
    try:
        domain = urlparse(url).netloc.lower()
        return domain.endswith(".pt")
    except Exception:
        return False

def newsapi_tool():
    # Busca notícias recentes sobre SRAG e vacinação com a NewsAPI

    url = "https://newsapi.org/v2/everything"

    key_words = (
        'síndrome respiratória aguda grave OR srag OR '
        'vacina gripe OR vacina influenza OR '
        'gripe brasil OR vacina covid brasil OR '
        'vacina covid-19 brasil OR síndrome respiratória'
    )

    params = {
        "q": key_words,
        "language": "pt",
        "sortBy": "publishedAt",
        "pageSize": 20,  # pede mais para compensar o filtro
        "apiKey": NEWSAPI_KEY
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    articles = response.json().get("articles", [])

    filtered_articles = []

    for a in articles:
        url_article = a.get("url", "")
        if not url_article:
            continue

        if portugal_source(url_article):
            continue

        filtered_articles.append({
            "title": a.get("title"),
            "source": a.get("source", {}).get("name"),
            "date": a.get("publishedAt", "")[:10],
            "summary": a.get("description"),
            "url": url_article
        })


    return filtered_articles

print(newsapi_tool())