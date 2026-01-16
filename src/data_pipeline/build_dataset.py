import os

import pandas as pd
from dotenv import load_dotenv

from src.data_pipeline.clean_dataset import clean_dataset

# Carrega variáveis de ambiente do .env
load_dotenv()

URL = os.getenv("OPENDATASUS_URL")
RAW_PATH = "data/raw/srag_raw.csv"
OUTPUT_PATH = "data/processed/srag_clean.csv"

def build_clean_dataset():
    if os.path.exists(OUTPUT_PATH):
        print("Arquivo limpo já existe. Pulando download.")
        return
    
    elif os.path.exists(RAW_PATH):
        print("Arquivo bruto já existe localmente. Pulando download.")
        df = pd.read_csv(RAW_PATH, sep=';', encoding='latin1')
        print("Sucesso: Dados carregados localmente.")

    else:
        try:
        # Tenta ler da URL
            print(f"Tentando download: {URL}\nEste processo pode levar alguns minutos...")
            df = pd.read_csv(URL, sep=';', encoding='latin1')
            print("Sucesso: Dados carregados diretamente da nuvem.")

        except Exception as e:
        # Se der erro, cai aqui e lê o local
            print(f"Aviso: Falha ao acessar a URL. Erro: {e}")
    
        
    df_clean = clean_dataset(df)
    df_clean.to_csv(OUTPUT_PATH, index=False)
    print("Dataset limpo gerado com sucesso em 'data/processed/srag_clean.csv'")

if __name__ == "__main__":
    build_clean_dataset()
