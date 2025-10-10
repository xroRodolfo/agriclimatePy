# 🌾 agriclimatePy

- **Descripción general**  
  - agriclimatePy es un proyecto para el análisis del impacto del cambio climático en la agricultura. Proporciona un flujo reproducible —desde la preparación de los datos hasta el análisis estadístico y la visualización— que facilita explorar la relación entre variables climáticas, prácticas agrícolas y rendimiento de cultivos.

- **Estructura del repositorio**  
 **Contenido y dónde encontrarlo**  
- **`backend/`** — lógica reutilizable y preparación de datos  
  - `limpiezaDeDatos.py` — script de preparación: normaliza nombres de columnas, elimina duplicados, limpia variables textuales (país, región, tipo de cultivo, estrategias de adaptación), filtra temperaturas fuera de rango, convierte columnas numéricas y guarda `dataset_unificado.csv`. *(Punto de entrada para obtener datos listos para análisis.)*  
  - `analysis.py` — funciones para análisis: promedio de producción por año, correlaciones Pearson/Spearman entre variables climáticas y rendimiento, y resumen estadístico. *(Se usa desde notebooks o scripts.)*  
  - `visualization.py` — funciones que generan figuras matplotlib y devuelven `fig/ax` (por ejemplo, serie temporal del rendimiento promedio por año). *(Diseñado para integrarse en notebooks o en un flujo de presentación.)*  
- **`data/`** — CSV fuente con observaciones climáticas, productivas y económicas.  
  - `climate_change_impact_on_agriculture_2024.csv` —  datos crudos *(Después de la limpieza se genera `dataset_unificado.csv`.)*  
  - `dataset_unificado.csv` - datos procesados, generado despues de la limpieza
- **`notebooks/`** — notebooks con narrativa y resultados  
  - `graficospseudo.ipynb` — exploración y visualización: selección de variables, gráficos exploratorios y análisis visual para detectar patrones y anomalías.  
  - `regresiones.ipynb` — modelado: regresiones (lineal simple/múltiple u otras), métricas (R², MAE, RMSE) y discusión interpretativa de los resultados.
  - `limpieza_notebook.ipynb` — notebook complementario que documenta y valida el proceso de limpieza (paralelo a `limpiezaDeDatos.py`): carga y previsualización del CSV crudo, pasos de normalización de columnas, diagnóstico y visualización de valores faltantes, comprobación de conversiones numéricas y detección/tratamiento de outliers, comparativa **antes/después** y verificación final del `dataset_unificado.csv`.


- **Dependencias principales (contexto técnico)**  
    - pandas, numpy, matplotlib.  
    - seaborn, scikit-learn, statsmodels.  
    *(Este README es descriptivo; no incluye instrucciones de instalación.)*
