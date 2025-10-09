# visualization.py
import matplotlib.pyplot as plt
import pandas as pd

from .analysis import produccion_promedio_por_anio

def grafico_produccion_por_anio(df: pd.DataFrame):
    """
    Línea temporal del rendimiento promedio por año.
    Retorna la figura para que main.py pueda hacer plt.show().
    """
    serie = produccion_promedio_por_anio(df)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(serie.index, serie.values, marker="o")
    ax.set_title("Rendimiento promedio por año (t/ha)")
    ax.set_xlabel("Año")
    ax.set_ylabel("t/ha")
    ax.grid(True, alpha=0.3)
    return fig
