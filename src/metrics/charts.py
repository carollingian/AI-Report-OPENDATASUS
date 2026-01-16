import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Número diário de casos dos últimos 30 dias
def plot_last_30d(df, output_path):
    """
    Função que plota o número diário de casos dos últimos 30 dias e salva o gráfico em output_path
    """

    df = df.copy()
    df["data_notificacao"] = pd.to_datetime(df["data_notificacao"], errors="coerce")

    ref_day = pd.Timestamp.today().normalize()
    start_day = ref_day - pd.Timedelta(days=30)

    df_30d = df[
        (df["data_notificacao"].notna())
        & (df["data_notificacao"] >= start_day)
        & (df["data_notificacao"] <= ref_day)
    ]

    daily_cases = df_30d.groupby(df_30d["data_notificacao"].dt.date).size()

    full_idx = pd.date_range(start=start_day, end=ref_day, freq="D")
    daily_cases.index = pd.to_datetime(daily_cases.index)
    daily_cases = daily_cases.reindex(full_idx, fill_value=0)

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(daily_cases.index, daily_cases.values, linewidth=2.5, marker="o", markersize=4)
    ax.fill_between(daily_cases.index, daily_cases.values, alpha=0.2)

    ax.set_title(
        "Número diário de casos (Últimos 30 Dias)",
        fontsize=16,
        fontweight="bold",
        loc="left",
        pad=20,
    )
    ax.set_ylabel("Casos Diários")

    ax.xaxis.set_major_locator(mdates.DayLocator(interval=4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%b"))

    sns.despine(left=True, bottom=True)

    max_val = daily_cases.max()
    if max_val > 0:
        max_date = daily_cases.idxmax()
        ax.annotate(
            f"Pico: {int(max_val)}",
            xy=(max_date, max_val),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            va="bottom",
            bbox=dict(boxstyle="round,pad=0.3", fc="#e74c3c", ec="none", alpha=0.8),
            color="white",
            fontweight="bold",
        )

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def plot_last_12m(df, output_path):
    """
    Função que plota o número mensal de casos dos últimos 12 meses e salva o gráfico em output_path
    """

    df = df.copy()
    df["data_notificacao"] = pd.to_datetime(df["data_notificacao"], errors="coerce")

    ref_day = pd.Timestamp.today().normalize()
    start_day = ref_day - pd.DateOffset(months=12)

    df_12m = df[
        (df["data_notificacao"].notna())
        & (df["data_notificacao"] >= start_day)
        & (df["data_notificacao"] <= ref_day)
    ]

    monthly_cases = df_12m.groupby(df_12m["data_notificacao"].dt.to_period("M")).size()

    monthly_cases.index = monthly_cases.index.to_timestamp()

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(12, 6))

    bars = ax.bar(monthly_cases.index, monthly_cases.values, width=20)
    ax.plot(monthly_cases.index, monthly_cases.values, marker="o", linestyle="--", linewidth=2)

    ax.set_title(
        "Número mensal de casos (Últimos 12 Meses)",
        fontsize=16,
        fontweight="bold",
        loc="left",
        pad=20,
    )
    ax.set_ylabel("Quantidade de Casos")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b/%y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())

    sns.despine(left=True, bottom=True)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{int(height)}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
