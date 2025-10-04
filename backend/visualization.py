import matplotlib.pyplot as plt

def grafico_produccion_por_anio(df):
    """
    Genera un gráfico de línea mostrando la producción promedio por año.
    """
    if "Year" not in df.columns or "Production" not in df.columns:
        raise ValueError("El dataset no contiene columnas 'Year' o 'Production'.")

    fig, ax = plt.subplots(figsize=(6,4))
    df.groupby("Year")["Production"].mean().plot(ax=ax, marker="o")
    ax.set_title("Producción agrícola promedio por año")
    ax.set_ylabel("Producción (toneladas/ha)")
    ax.set_xlabel("Año")
    plt.tight_layout()
    return fig
