import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")


def portugal_source(url):
    """
    Função que verifica e retorna True se a URL é de uma fonte de Portugal (.pt)
    """

    try:
        domain = urlparse(url).netloc.lower()
        return domain.endswith(".pt")
    except Exception:
        return False


@tool
def news_tool(arg):
    """
    Tool que busca e filtra notícias recentes sobre SRAG
    por meio de palavras-chave com a NewsAPI
    """

    url = "https://newsapi.org/v2/everything"

    key_words = (
        "síndrome respiratória aguda grave OR srag OR "
        "vacina gripe brasil OR síndrome respiratória brasil OR "
        "gripe brasil"
    )

    params = {
        "q": key_words,
        "language": "pt",
        "sortBy": "publishedAt",
        "pageSize": 20,
        "apiKey": NEWSAPI_KEY,
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    articles = response.json().get("articles", [])

    filtered_articles = []

    for a in articles:
        url_article = a.get("url", "")
        if not url_article:
            continue

        # Remove artigos de fontes de Portugal para centralizar no Brasil
        if portugal_source(url_article):
            continue

        filtered_articles.append(
            {
                "title": a.get("title"),
                "source": a.get("source", {}).get("name"),
                "date": a.get("publishedAt", "")[:10],
                "summary": a.get("description"),
                "url": url_article,
            }
        )

    return filtered_articles
