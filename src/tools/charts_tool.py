import pandas as pd
from langchain.tools import tool

from src.metrics.charts import plot_last_12m, plot_last_30d

DATA_PATH = "data/processed/srag_clean.csv"
OUTPUT_PATH = "report/charts"

@tool
def charts_tool(arg):
    """
    Tool que gera os gráficos
    - Número diário de casos de SRAG (Últimos 30 Dias)
    - Número mensal de casos de SRAG (Últimos 12 Meses)
    e retorna os caminhos dos arquivos png
    """

    df = pd.read_csv(DATA_PATH)

    daily_path = f"{OUTPUT_PATH}/cases_last_30d.png"
    monthly_path = f"{OUTPUT_PATH}/cases_last_12m.png"

    plot_last_30d(df, daily_path)
    plot_last_12m(df, monthly_path)

    return {
        "daily_cases_chart": daily_path,
        "monthly_cases_chart": monthly_path
    }