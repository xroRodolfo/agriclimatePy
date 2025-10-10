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

def grafico_correlaciones(df: pd.DataFrame):
    """
    Gráfico de barras horizontales mostrando correlaciones de factores climáticos
    con el rendimiento agrícola.
    """
    from .analysis import correlacion_clima_produccion
    
    correlaciones = correlacion_clima_produccion(df)
    
    # Preparar datos
    factores = [f.replace('_', ' ') for f in correlaciones.index]
    valores = correlaciones['pearson'].values
    colores = ['#43a047' if v > 0 else '#e53935' for v in valores]
    
    # Crear gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(factores, valores, color=colores, alpha=0.8)
    ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
    ax.set_xlabel('Correlación con Rendimiento')
    ax.set_title('Impacto de Factores Climáticos en el Rendimiento Agrícola')
    ax.grid(True, axis='x', alpha=0.3)
    
    # Invertir orden para que el mayor esté arriba
    ax.invert_yaxis()
    
    plt.tight_layout()
    return fig
    