from backend.loader import cargar_dataset, limpiar_dataset
from backend.analysis import produccion_promedio_por_anio, correlacion_clima_produccion, resumen_estadistico
from backend.visualization import grafico_produccion_por_anio
import matplotlib.pyplot as plt
from flask import Flask, render_template, send_file
import io
import base64
import random
import matplotlib
matplotlib.use('Agg')  # Evita que use interfaces gráficas como Tkinter
from reportlab.pdfgen import canvas
import pandas as pd

'''
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
'''

app = Flask(__name__)

@app.route('/')
def index():
    # Cargar datos reales
    df = cargar_dataset("data/climate_change_impact_on_agriculture_2024.csv")
    if df is None:
        return "Error: No se pudo cargar el dataset", 500
    
    df = limpiar_dataset(df)
    
    # Calcular métricas clave
    metricas = {
        'rendimiento_promedio': round(df['Crop_Yield_MT_per_HA'].mean(), 2),
        'rendimiento_max': round(df['Crop_Yield_MT_per_HA'].max(), 2),
        'rendimiento_min': round(df['Crop_Yield_MT_per_HA'].min(), 2),
        'temperatura_promedio': round(df['Average_Temperature_C'].mean(), 1),
        'precipitacion_promedio': round(df['Total_Precipitation_mm'].mean(), 0),
        'total_registros': len(df),
        'anios': f"{int(df['Year'].min())} - {int(df['Year'].max())}"
    }
    
    # Calcular top 3 factores de mayor impacto
    correlaciones = correlacion_clima_produccion(df)
    top_factores = []
    for factor, valores in correlaciones.head(3).iterrows():
        impacto = "positivo" if valores['pearson'] > 0 else "negativo"
        top_factores.append({
            'nombre': factor,
            'valor': round(valores['pearson'], 3),
            'impacto': impacto,
            'porcentaje': abs(round(valores['pearson'] * 100, 1))
        })
    
    # Generar GRÁFICO 1: Rendimiento por año
    fig1 = grafico_produccion_por_anio(df)
    img1 = io.BytesIO()
    fig1.savefig(img1, format='png', bbox_inches='tight', dpi=100)
    img1.seek(0)
    grafico_base64 = base64.b64encode(img1.getvalue()).decode()
    plt.close(fig1)
    
    # Generar GRÁFICO 2: Correlaciones
    from backend.visualization import grafico_correlaciones
    fig2 = grafico_correlaciones(df)
    img2 = io.BytesIO()
    fig2.savefig(img2, format='png', bbox_inches='tight', dpi=100)
    img2.seek(0)
    grafico_correlaciones_base64 = base64.b64encode(img2.getvalue()).decode()
    plt.close(fig2)
    
    # Pasar datos a la plantilla
    return render_template('index.html', 
                         grafico_base64=grafico_base64,
                         grafico_correlaciones_base64=grafico_correlaciones_base64,
                         metricas=metricas,
                         top_factores=top_factores)

@app.route('/exportar')
def exportar_pdf():
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import Table, TableStyle
    import matplotlib.pyplot as plt
    import pandas as pd
    
    # Cargar y procesar datos
    df = cargar_dataset("data/climate_change_impact_on_agriculture_2024.csv")
    if df is None:
        return "Error: No se pudo cargar el dataset", 500
    
    df = limpiar_dataset(df)
    
    # Obtener análisis
    prod_anual = produccion_promedio_por_anio(df)
    correlaciones = correlacion_clima_produccion(df)
    resumen = resumen_estadistico(df)
    
    # Crear PDF
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter
    
    # === PÁGINA 1: PORTADA Y RESUMEN ===
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "Reporte AgriClimate 2025")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, "Análisis del impacto del cambio climático en la agricultura")
    c.drawString(50, height - 100, f"Generado: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Datos generales
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 140, "📊 Datos Generales del Dataset")
    c.setFont("Helvetica", 11)
    c.drawString(70, height - 165, f"• Total de registros: {len(df)}")
    c.drawString(70, height - 185, f"• Años analizados: {df['Year'].min()} - {df['Year'].max()}")
    c.drawString(70, height - 205, f"• Regiones: {df['Region'].nunique() if 'Region' in df.columns else 'N/A'}")
    c.drawString(70, height - 225, f"• Tipos de cultivo: {df['Crop_Type'].nunique() if 'Crop_Type' in df.columns else 'N/A'}")
    
    # Estadísticas clave
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 265, "🌾 Rendimiento Agrícola")
    c.setFont("Helvetica", 11)
    rendimiento_promedio = df['Crop_Yield_MT_per_HA'].mean()
    rendimiento_max = df['Crop_Yield_MT_per_HA'].max()
    rendimiento_min = df['Crop_Yield_MT_per_HA'].min()
    
    c.drawString(70, height - 290, f"• Rendimiento promedio: {rendimiento_promedio:.2f} MT/HA")
    c.drawString(70, height - 310, f"• Rendimiento máximo: {rendimiento_max:.2f} MT/HA")
    c.drawString(70, height - 330, f"• Rendimiento mínimo: {rendimiento_min:.2f} MT/HA")
    
    # Top 3 correlaciones
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 370, "🔗 Top 3 Factores de Mayor Impacto")
    c.setFont("Helvetica", 11)
    y_pos = height - 395
    for i, (factor, valor) in enumerate(correlaciones.head(3).iterrows(), 1):
        impacto = "positivo" if valor['pearson'] > 0 else "negativo"
        c.drawString(70, y_pos, f"{i}. {factor}: {valor['pearson']:.3f} (impacto {impacto})")
        y_pos -= 20
    
    # === PÁGINA 2: GRÁFICO ===
    c.showPage()
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "📈 Evolución del Rendimiento Agrícola")
    
    # Generar gráfico
    fig = grafico_produccion_por_anio(df)
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
    img_buffer.seek(0)
    plt.close(fig)
    
    # Insertar gráfico en PDF
    from reportlab.lib.utils import ImageReader
    img = ImageReader(img_buffer)
    c.drawImage(img, 50, height - 450, width=500, height=350, preserveAspectRatio=True)
    
    # === PÁGINA 3: TABLA DE CORRELACIONES ===
    c.showPage()
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "📊 Correlaciones Clima ↔ Rendimiento")
    
    c.setFont("Helvetica", 10)
    y_pos = height - 90
    
    # Encabezados
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y_pos, "Factor Climático")
    c.drawString(300, y_pos, "Pearson")
    c.drawString(400, y_pos, "Spearman")
    y_pos -= 20
    
    # Datos
    c.setFont("Helvetica", 9)
    for factor, valores in correlaciones.iterrows():
        if y_pos < 100:  # Nueva página si se acaba el espacio
            c.showPage()
            y_pos = height - 50
        
        c.drawString(50, y_pos, str(factor)[:35])
        c.drawString(300, y_pos, f"{valores['pearson']:.4f}")
        c.drawString(400, y_pos, f"{valores['spearman']:.4f}")
        y_pos -= 15
    
    # Pie de página
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(50, 30, "© 2025 AgriClimate Team - Generado con Flask + ReportLab + Pandas")
    
    # Guardar PDF
    c.save()
    pdf_buffer.seek(0)
    
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="Reporte_AgriClimate_Completo.pdf",
        mimetype="application/pdf"
    )

if __name__ == '__main__':
    app.run(debug=True)
