from src.metrics.rates import (
    increase_cases_rate,
    metrics_rate
)

# Calcula as métricas para o relatório
def calculate_rates(df):
    """
    Calcula e retorna as métricas:
    - Taxa de aumento de casos (7, 14, 30 dias)
    - Taxa de mortalidade (7, 14, 30 dias)
    - Taxa de ocupação da UTI (7, 14, 30 dias)
    - Taxa de vacinação (gripe e COVID-19) (7, 14, 30 dias)
    """
    return {
        "taxa_aumento_casos_7_dias": round(increase_cases_rate(df, 7), 2),
        "taxa_aumento_casos_14_dias": round(increase_cases_rate(df, 14), 2),
        "taxa_aumento_casos_30_dias": round(increase_cases_rate(df, 30), 2),
        "taxa_mortalidade_7_dias": round(metrics_rate(df, 7, "evolucao"), 2),
        "taxa_mortalidade_14_dias": round(metrics_rate(df, 14, "evolucao"), 2),
        "taxa_mortalidade_30_dias": round(metrics_rate(df, 30, "evolucao"), 2),
        "taxa_ocupacao_uti_7_dias": round(metrics_rate(df, 7, "uti"), 2),
        "taxa_ocupacao_uti_14_dias": round(metrics_rate(df, 14, "uti"), 2),
        "taxa_ocupacao_uti_30_dias": round(metrics_rate(df, 30, "uti"), 2),
        "taxa_vacinacao_7_dias": round(metrics_rate(df, 7, "vacina"), 2),
        "taxa_vacinacao_14_dias": round(metrics_rate(df, 14, "vacina"), 2),
        "taxa_vacinacao_30_dias": round(metrics_rate(df, 30, "vacina"), 2),
        "taxa_vacinacao_7_dias": round(metrics_rate(df, 7, "vacina_covid"), 2),
        "taxa_vacinacao_14_dias": round(metrics_rate(df, 14, "vacina_covid"), 2),
        "taxa_vacinacao_30_dias": round(metrics_rate(df, 30, "vacina_covid"), 2)
    }