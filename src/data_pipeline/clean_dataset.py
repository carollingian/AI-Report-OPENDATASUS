import numpy as np
import pandas as pd

def transform_binary(df, column):
    df[column] = (
        df[column]
        .replace({2: 0, 9: pd.NA})
        .astype("Int64")
    )
    return df

def transform_evolution(df):
    df["EVOLUCAO"] = (
        df["EVOLUCAO"]
        .replace({2: 1, 1: 0, 3: 0, 9: pd.NA})
        .astype("Int64")
    )
    return df

def to_datetime(df, column):
   df[column] = pd.to_datetime(df[column], format="%Y-%m-%d", errors="coerce")

def drop_columns(df):
   null_pct = df.isna().mean()
   cols_to_drop = null_pct[null_pct > 0.5].index
   df = df.drop(columns=cols_to_drop)

   df.columns = (
        df.columns
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
        .str.upper()
    )
   
   cols_drop = ["NU_NOTIFIC", "DT_SIN_PRI", "SEM_NOT", "SEM_PRI", "ID_REGIONA", "CO_REGIONA", "ID_MUNICIP", 
                "CO_MUN_NOT", "NU_IDADE_N", "TP_IDADE","COD_IDADE","ID_PAIS","CO_PAIS","SG_UF","ID_RG_RESI", 
                "CO_RG_RESI", "ID_MN_RESI", "CO_MUN_RES", "CS_SEXO","CS_RACA", "CS_GESTANT", "CS_ESCOL_N", 
                "CS_ZONA", "NOSOCOMIAL", "AVE_SUINO", "FEBRE", "TOSSE","GARGANTA","DISPNEIA","DESC_RESP",
                "HISTO_VGM", "SATURACAO", "DIARREIA","VOMITO","OUTRO_SIN","ANTIVIRAL","TRAT_COV","HOSPITAL", 
                "SG_UF_INTE", "ID_RG_INTE","CO_RG_INTE", "DT_INTERNA", "DT_NASC","CO_MU_INTE", "SURTO_SG",
                "ID_MN_INTE", "NM_UN_INTE", "RAIOX_RES","SUPORT_VEN","AMOSTRA", "TP_AMOSTRA", "DT_COLETA",
                "PCR_RESUL","DT_PCR","PCR_VSR","PCR_PARA1","PCR_PARA2","PCR_PARA3","PCR_PARA4","PCR_ADENO",
                "PCR_METAP","PCR_BOCA","PCR_RINO","PCR_OUTRO","CLASSI_FIN","CRITERIO","DT_ENCERRA","DT_DIGITA",
                "PCR_SARS2","DOR_ABD","FADIGA","PERD_OLFT","PERD_PALA","TOMO_RES","RES_AN","AN_SARS2","AN_VSR",
                "AN_PARA1","AN_PARA2","AN_PARA3","AN_ADENO","AN_OUTRO","POV_CT","TEM_CPF","ESTRANG","FNT_IN_COV",
                "CO_DETEC","REINF"]
   
   return df.drop(columns=cols_drop, errors="ignore")

def clean_dataset(df):
   df = drop_columns(df)

   transform_evolution(df)
   transform_binary(df, "UTI")
   transform_binary(df, "VACINA")
   transform_binary(df, "VACINA_COV")
   to_datetime(df, "DT_NOTIFIC")
   to_datetime(df, "DT_EVOLUCA")

   df = df.rename(columns={
    "DT_NOTIFIC": "data_notificacao",
    "DT_EVOLUCA": "data_evolucao",
    "VACINA_COV": "vacina_covid",
    "UTI": "uti",
    "VACINA": "vacina",
    "EVOLUCAO": "evolucao",
    "SG_UF_NOT": "uf_notificacao",
    })
   
   return df