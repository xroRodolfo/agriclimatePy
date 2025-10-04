def produccion_promedio_por_anio(df):
    """
    Retorna la producción promedio agrupada por año.
    Ajustado al dataset de Kaggle.
    """
    if "Year" in df.columns and "Production" in df.columns:
        return df.groupby("Year")["Production"].mean()
    else:
        raise ValueError("El dataset no contiene columnas 'Year' o 'Production'.")

def correlacion_clima_produccion(df):
    """
    Calcula correlaciones entre factores climáticos y la producción.
    Columnas ajustadas al dataset: Temperature, Rainfall, Natural_disasters, Production
    """
    variables = ["Temperature", "Rainfall", "Natural_disasters", "Production"]
    disponibles = [col for col in variables if col in df.columns]
    if len(disponibles) < 2:
        raise ValueError("No hay suficientes columnas climáticas y de producción para calcular correlación.")
    return df[disponibles].corr()
