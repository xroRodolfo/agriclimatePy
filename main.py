from backend.loader import cargar_dataset, limpiar_dataset
from backend.analysis import produccion_promedio_por_anio, correlacion_clima_produccion, resumen_estadistico
from backend.visualization import grafico_produccion_por_anio
import matplotlib.pyplot as plt

if __name__ == "__main__":
    df = cargar_dataset("data/climate_change_impact_on_agriculture_2024.csv")
    if df is not None:
        df = limpiar_dataset(df)

        print("Resumen estadístico:\n", resumen_estadistico(df), "\n")

        print("Producción promedio por año:")
        print(produccion_promedio_por_anio(df), "\n")

        print("Correlación clima ↔ rendimiento:")
        print(correlacion_clima_produccion(df), "\n")

        fig = grafico_produccion_por_anio(df)
        plt.show()
