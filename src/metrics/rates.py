import pandas as pd


# MÉTRICA 1: TAXA DE AUMENTO DE CASOS
def increase_cases_rate(df, days):
    """
    Função que calcula a taxa de aumento de casos nos últimos 'days' dias
    Retorna a taxa em porcentagem
    """
    
    df = df.copy()
    df["data_notificacao"] = pd.to_datetime(df["data_notificacao"], errors="coerce")

    cases_day = (
        df
        .dropna(subset=["data_notificacao"])
        .groupby(df["data_notificacao"].dt.date)
        .size()
        .sort_index()
    )

    if len(cases_day) < 2 * days:
        return 0.0

    current = cases_day[-days:].mean()
    previous = cases_day[-2 * days:-days].mean()

    if previous == 0:
        return 0.0

    return ((current - previous) / previous) * 100

# MÉTRICA 2: TAXA DE MORTALIDADE
# MÉTRICA 3: TAXA DE OCUPAÇÃO DE UTI
# MÉTRICA 4: TAXA DE VACINAÇÃO
def metrics_rate(df, days, feature):
    """
    Função que calcula a taxa de um dado feature 
    (evolucao, uti, vacina, vacina_covid) 
    nos últimos 'days' dias
    Retorna a taxa em porcentagem
    """

    if feature == "evolucao":
        date = "data_evolucao"
    else:
        date = "data_notificacao"

    df = df.copy()
    df[date] = pd.to_datetime(df[date], errors="coerce")

    ref_day = pd.Timestamp.today().normalize()
    start_day = ref_day - pd.Timedelta(days=days)

    df_period = df[
        (df[date].notna()) &
        (df[date] >= start_day) &
        (df[date] <= ref_day)
    ]

    if len(df_period) == 0:
        return 0.0

    feat = (df_period[feature] == 1).sum()
    return (feat / len(df_period)) * 100