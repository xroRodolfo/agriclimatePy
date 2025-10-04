import pandas as pd

def cargar_dataset(ruta):
    """
    Carga un dataset CSV y lo devuelve como DataFrame de pandas.
    """
    try:
        df = pd.read_csv(ruta)
        print(f"Dataset cargado con éxito. Columnas: {df.columns.tolist()}")
        return df
    except Exception as e:
        print(f"Error al cargar dataset: {e}")
        return None

def limpiar_dataset(df):
    """
    Limpieza básica del dataset:
    - Elimina duplicados
    - Rellena valores faltantes con promedio (numéricos) o 'Desconocido' (categóricos)
    """
    df = df.drop_duplicates()

    for col in df.columns:
        if df[col].dtype in ["int64", "float64"]:
            df[col] = df[col].fillna(df[col].mean())
        else:
            df[col] = df[col].fillna("Desconocido")
    
    return df
