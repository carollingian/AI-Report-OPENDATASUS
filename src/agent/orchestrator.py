from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

from src.tools.news_tool import news_tool
from src.tools.rates_tool import rates_tool
from src.tools.charts_tool import charts_tool


def build_agent():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    tools = [

        Tool.from_function(
            func=rates_tool,
            name="Calcular Metricas Epidemiologicas",
            description=(
                "Calcula as metricas quantitativas"
                "- Taxa de aumento de casos (7, 14, 30 dias)"
                "- Taxa de mortalidade (7, 14, 30 dias)"
                "- Taxa de ocupação da UTI (7, 14, 30 dias)"
                "- Taxa de vacinação (gripe e COVID-19) (7, 14, 30 dias)"
                "a partir dos dados do OpenDataSUS processados."
            )
        ),

        Tool.from_function(
            func=charts_tool,
            name="Gerar Graficos Epidemiologicos",
            description=(
                "Gera dois graficos temporais de casos (ultimos 30 dias e ultimos 12 meses) dos dados do OpenDataSUS processados."
            )
        ),

        Tool.from_function(
            func=news_tool,
            name="Pesquisar Noticias Epidemiologicas",
            description=(
                "Busca noticias recentes sobre SRAG, gripe, COVID-19 e vacinacao no Brasil. Retorna titulo, fonte, data e resumo de cada notícia."
            )
        )
    ]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    return agent
