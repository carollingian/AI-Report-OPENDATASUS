import pandas as pd
from clean_dataset import clean_dataset

URL = "https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SRAG/2025/INFLUD25-22-12-2025.csv"
RAW_PATH = "data/raw/srag_raw.csv"
OUTPUT_PATH = "data/processed/srag_clean.csv"

def build_clean_dataset():
    try:
    # Tenta ler da URL
        print(f"Tentando download: {URL}")
        df = pd.read_csv(URL, sep=';', encoding='latin1')
        print("Sucesso: Dados carregados diretamente da nuvem.")

    except Exception as e:
    # Se der erro, cai aqui e lê o local
        print(f"Aviso: Falha ao acessar a URL. Erro: {e}")
        print("Tentando carregar do arquivo local...")
    
        df = pd.read_csv(RAW_PATH, sep=';', encoding='latin1')
        print("Sucesso: Dados carregados localmente.")
    df_clean = clean_dataset(df)
    df_clean.to_csv(OUTPUT_PATH, index=False)

if __name__ == "__main__":
    build_clean_dataset()
