from backend.loader import cargar_dataset, limpiar_dataset
from backend.analysis import produccion_promedio_por_anio, correlacion_clima_produccion
from backend.visualization import grafico_produccion_por_anio
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Cargar datos
    df = cargar_dataset("data/climate_change_impact_on_agriculture_2024.csv")
    if df is not None:
        df = limpiar_dataset(df)

        # Análisis
        print("Producción promedio por año:")
        print(produccion_promedio_por_anio(df))

        print("\nCorrelación entre variables climáticas y producción:")
        print(correlacion_clima_produccion(df))

        # Visualización
        fig = grafico_produccion_por_anio(df)
        plt.show()
