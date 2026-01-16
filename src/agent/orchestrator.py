from langchain.agents import AgentType, initialize_agent
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from langchain_groq import ChatGroq

from src.agent.orchestrator_prompt import ORCHESTRATOR_PROMPT
from src.tools.charts_tool import charts_tool
from src.tools.news_tool import news_tool
from src.tools.rates_tool import rates_tool


def build_agent():
    # LLM Reader
    llm_reader = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct", temperature=0.0)

    # LLM Writer
    llm_writer = ChatGroq(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        temperature=0.3,  # Maior temperatura para redigir mais
        max_tokens=8192,
    )

    tools = [
        Tool.from_function(
            func=rates_tool,
            name="Calcular Metricas",
            description="Calcula taxas de aumento, mortalidade, UTI e "
            "vacinação (gripe e COVID-19) "
            "dos dados do OpenDataSUS processados..",
        ),
        Tool.from_function(
            func=charts_tool,
            name="Gerar Graficos",
            description="Gera dois graficos temporais de casos "
            "(ultimos 30 dias e ultimos 12 meses) "
            "dos dados do OpenDataSUS processados.",
        ),
        Tool.from_function(
            func=news_tool,
            name="Buscar Noticias",
            description="Busca noticias recentes sobre SRAG, gripe, "
            "COVID-19 e vacinacao no Brasil. "
            "Retorna titulo, fonte, data e resumo de cada notícia.",
        ),
    ]

    # 1: AGENTE LEITOR
    reader_agent = initialize_agent(
        tools=tools,
        llm=llm_reader,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
    )

    # 2: CADEIA DO ESCRITOR
    report_prompt_template = PromptTemplate(
        input_variables=["dados_coletados"],
        template=ORCHESTRATOR_PROMPT + "\n\nCONTEXTO DOS DADOS EXTRAÍDOS PELAS FERRAMENTAS:"
        "\n{dados_coletados}\n\nREDAÇÃO DO RELATÓRIO:",
    )

    writer_chain = report_prompt_template | llm_writer
    return reader_agent, writer_chain


def run_analysis():
    agent, writer = build_agent()

    print("_________ 1. Reader coletando métricas _________")

    query = (
        "Use suas ferramentas para coletar TODAS as métricas disponíveis "
        "(casos, mortalidade, UTI, vacina), "
        "gerar os gráficos de 30 dias e 12 meses, e buscar as 5 notícias mais relevantes. "
        "Sua Resposta Final deve ser apenas um compilado estruturado desses dados brutos, "
        "sem análise."
    )

    raw_data = agent.run(query)

    print("_________ 2. Writer escrevendo relatório _________")
    final_report = writer.invoke({"dados_coletados": raw_data})

    return final_report.content
