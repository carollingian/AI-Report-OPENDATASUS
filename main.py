import os
from src.agent.orchestrator import build_agent

def main():
    reader_agent, writer_chain = build_agent()

    print("Iniciando coleta de dados com o Reader Agent...")
    
    query = (
        "Execute as seguintes ações sequencialmente:\n"
        "1. Use 'Calcular Metricas' para obter todas as taxas disponíveis.\n"
        "2. Use 'Gerar Graficos' para obter os dados de visualização.\n"
        "3. Use 'Buscar Noticias' para buscar as 5 notícias mais recentes.\n"
        "Retorne APENAS um compilado estruturado desses dados brutos. Não faça análises."
    )
    
    # Executa o agente leitor
    raw_data = reader_agent.run(query)
    
    print("\nDados brutos coletados com sucesso!")
    print("\nRedigindo o relatório final com o Writer Chain...")

    result = writer_chain.invoke({"dados_coletados": raw_data})
    final_report = result.content if hasattr(result, 'content') else result

    print("\n__________________RELATÓRIO FINAL__________________\n")
    print(final_report)

    # Salvando em Markdown
    with open("report/final_report.md", "w", encoding="utf-8") as f:
        f.write(final_report)
        print("\nRelatório concluído com sucesso e salvo em 'final_report.md'")

if __name__ == "__main__":
    main()