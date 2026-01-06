import pandas as pd
from langchain.tools import tool
from src.metrics.calculate_rates import calculate_rates

DATA_PATH = "data/processed/srag_clean.csv"

@tool
def get_rates():
    # Retorna métricas requisitadas para o relatório
    df = pd.read_csv(DATA_PATH)
    return calculate_rates(df)
