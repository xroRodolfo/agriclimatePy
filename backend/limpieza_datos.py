
import pandas as pd

df = pd.read_csv("data/climate_change_impact_on_agriculture_2024.csv")

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

df.drop_duplicates(inplace=True)

df['country'] = df['country'].str.strip().str.title()
df['region'] = df['region'].str.strip().str.title()
df['crop_type'] = df['crop_type'].str.strip().str.capitalize()
df['adaptation_strategies'] = df['adaptation_strategies'].str.strip().str.title()

df = df[(df['average_temperature_c'] > -10) & (df['average_temperature_c'] < 60)]

numeric_cols = [
    'average_temperature_c', 'total_precipitation_mm', 'co2_emissions_mt',
    'crop_yield_mt_per_ha', 'extreme_weather_events', 'irrigation_access_%',
    'pesticide_use_kg_per_ha', 'fertilizer_use_kg_per_ha',
    'soil_health_index', 'economic_impact_million_usd'
]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

df.fillna(df.mean(numeric_only=True), inplace=True)

df.to_csv("dataset_unificado.csv", index=False)

print("✅ Limpieza completada correctamente")
print("Registros finales:", len(df))
print("Columnas:", list(df.columns))
print(df.head(5))
