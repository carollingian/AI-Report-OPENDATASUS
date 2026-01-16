import pandas as pd
from langchain.tools import tool

from src.metrics.calculate_rates import calculate_rates

DATA_PATH = "data/processed/srag_clean.csv"


@tool
def rates_tool(arg):
    """
    Tool que calcula e retorna as métricas:
    - Taxa de aumento de casos (7, 14, 30 dias)
    - Taxa de mortalidade (7, 14, 30 dias)
    - Taxa de ocupação da UTI (7, 14, 30 dias)
    - Taxa de vacinação (gripe e COVID-19) (7, 14, 30 dias)
    """
    # Retorna métricas requisitadas para o relatório
    df = pd.read_csv(DATA_PATH)
    return calculate_rates(df)
