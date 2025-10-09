# analysis.py
import pandas as pd

TARGET_COL = "Crop_Yield_MT_per_HA"

CLIMATE_COLS = [
    "Average_Temperature_C",
    "Total_Precipitation_mm",
    "Extreme_Weather_Events",
    "Irrigation_Access_%",
    "Pesticide_Use_KG_per_HA",
    "Fertilizer_Use_KG_per_HA",
    "Soil_Health_Index",
    "CO2_Emissions_MT",
    "Economic_Impact_Million_USD"  # opcional, quítala si no quieres variables económicas
]

def produccion_promedio_por_anio(df: pd.DataFrame) -> pd.Series:
    """
    Promedio anual del rendimiento (t/ha) según el CSV.
    """
    if "Year" not in df.columns or TARGET_COL not in df.columns:
        raise ValueError("Faltan columnas 'Year' o el objetivo de rendimiento en el dataset.")
    return df.groupby("Year")[TARGET_COL].mean().rename("Avg_Yield_MT_per_HA")

def correlacion_clima_produccion(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula correlaciones Pearson y Spearman entre variables climáticas y el rendimiento.
    Devuelve un DataFrame con ambas correlaciones ordenadas por |Pearson|.
    """
    disponibles = [c for c in CLIMATE_COLS if c in df.columns]
    cols = [TARGET_COL] + disponibles
    datos = df[cols].select_dtypes("number").dropna()

    if datos.shape[1] < 2:
        raise ValueError("No hay suficientes columnas numéricas para correlación.")

    pearson = datos.corr(method="pearson")[TARGET_COL].drop(TARGET_COL)
    spearman = datos.corr(method="spearman")[TARGET_COL].drop(TARGET_COL)

    out = pd.DataFrame({
        "pearson": pearson,
        "spearman": spearman
    }).sort_values(by="pearson", key=lambda s: s.abs(), ascending=False)

    return out

def resumen_estadistico(df: pd.DataFrame) -> pd.DataFrame:
    """
    Resumen estadístico de todas las columnas numéricas.
    """
    return df.select_dtypes("number").describe().T
