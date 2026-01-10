import os
import subprocess
from datetime import date

from src.data_pipeline.build_dataset import build_clean_dataset
from src.agent.orchestrator import build_agent

def markdown_to_pdf(md_path, pdf_path):
    try:
        subprocess.run(
            [
                "pandoc",
                md_path,
                "-o",
                pdf_path,
                "--pdf-engine=xelatex"
            ],
            check=True
        )
        print(f"PDF gerado com sucesso: {pdf_path}")
    except subprocess.CalledProcessError as e:
        print("Erro ao gerar PDF:", e)

def main():
    # 1: Construir dataset limpo
    print("Construindo dataset limpo...")
    build_clean_dataset()

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
    report_body = result.content if hasattr(result, "content") else result

    # HEADER COM DATA ATUAL
    data_geracao = date.today().strftime("%d/%m/%Y")

    report_header = f"""# Relatório Epidemiológico SRAG no Brasil

**Relatório gerado em:** {data_geracao}

---

"""

    final_report = report_header + report_body

    print("\n__________________RELATÓRIO FINAL__________________\n")
    print(final_report)

    # Salvando em Markdown
    md_path = "report/final_report.md"
    pdf_path = "report/final_report.pdf"

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(final_report)
        print(f"\nRelatório salvo em '{md_path}'")

    print("\nGerando PDF a partir do Markdown...")
    markdown_to_pdf(md_path=md_path, pdf_path=pdf_path)

if __name__ == "__main__":
    main()
