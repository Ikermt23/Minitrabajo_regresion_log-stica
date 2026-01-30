"""
main.py
Script principal - Ejecuta todo el pipeline de regresión logística
"""

import warnings
warnings.filterwarnings('ignore')

from data_processing import load_data, prepare_data, get_eda_stats
from model import (train_model, get_coefficients, make_predictions, 
                   evaluate_model, print_evaluation, compare_thresholds)
from visualizations import create_all_plots, plot_eda
import config

print("="*80)
print("REGRESIÓN LOGÍSTICA: PREDICCIÓN DE ESTILO DE VIDA SALUDABLE")
print("="*80)

# =============================================================================
# 1. CARGA Y EDA
# =============================================================================
print("\n[1/5] CARGA Y ANÁLISIS EXPLORATORIO")
print("-"*80)

df = load_data()
stats = get_eda_stats(df)

print(f"\nBalance de clases:")
print(stats['counts'])
print(f"Ratio: {stats['ratio']:.3f}")

print(f"\nTop 5 correlaciones con target:")
print(stats['correlations'].head(5).to_string(index=False))

# Graficar EDA
plot_eda(df, stats)

# =============================================================================
# 2. PREPARACIÓN DE DATOS
# =============================================================================
print("\n[2/5] PREPARACIÓN DE DATOS")
print("-"*80)

X_train, X_test, y_train, y_test, scaler = prepare_data(df)

# =============================================================================
# 3. ENTRENAMIENTO
# =============================================================================
print("\n[3/5] ENTRENAMIENTO DEL MODELO")
print("-"*80)

model = train_model(X_train, y_train)
coef_df = get_coefficients(model)

print(f"\nTop 5 variables más influyentes:")
print(coef_df[['Variable', 'Coeficiente', 'Odds_Ratio']].head(5).to_string(index=False))

# =============================================================================
# 4. PREDICCIÓN Y EVALUACIÓN
# =============================================================================
print("\n[4/5] EVALUACIÓN DEL MODELO")
print("-"*80)

# Predicciones con umbral por defecto
y_proba, y_pred = make_predictions(model, X_test, config.THRESHOLD_DEFAULT)

# Evaluar
metrics = evaluate_model(y_test, y_pred, y_proba)
print_evaluation(metrics)

# Comparar umbrales
threshold_comparison = compare_thresholds(model, X_test, y_test)

# =============================================================================
# 5. VISUALIZACIONES
# =============================================================================
print("\n[5/5] GENERACIÓN DE VISUALIZACIONES")
print("-"*80)

create_all_plots(model, X_test, y_test, y_proba, y_pred, metrics, coef_df)

# =============================================================================
# CONCLUSIONES
# =============================================================================
print("\n" + "="*80)
print("CONCLUSIONES")
print("="*80)

auc = metrics['auc']
f1 = metrics['f1']

# Clasificar rendimiento
if auc > 0.9:
    rendimiento = "EXCELENTE"
elif auc > 0.8:
    rendimiento = "MUY BUENO"
elif auc > 0.7:
    rendimiento = "BUENO"
else:
    rendimiento = "NECESITA MEJORAS"

print(f"""
RESUMEN EJECUTIVO:

1. RENDIMIENTO DEL MODELO: {rendimiento}
   • AUC-ROC: {auc:.3f}
   • F1-Score: {f1:.3f}
   • Accuracy: {metrics['accuracy']:.3f}

2. VARIABLES MÁS IMPORTANTES:
   {coef_df.head(3)['Variable'].tolist()}

3. ¿RESPONDE AL OBJETIVO?
   {'✓ SÍ' if auc > 0.75 else '⚠️ PARCIALMENTE'} - El modelo {'puede' if auc > 0.75 else 'tiene dificultad para'} predecir estilos de vida saludables

4. LIMITACIONES:
   • Posible desbalance de clases (ratio: {stats['ratio']:.3f})
   • Solo usa {len(config.FEATURES)} de 39+ variables disponibles
   • Asume relaciones lineales (log-odds)

5. MEJORAS PROPUESTAS:
   • Feature engineering (interacciones, ratios)
   • Incluir variables de sueño y estrés
   • Probar modelos ensemble (XGBoost, Random Forest)
   • Técnicas de balanceo (SMOTE)

6. ¿CONFIAR EN EL MODELO?
   {"✓ SÍ, con precaución" if auc > 0.8 else "⚠️ Requiere mejoras"}
   • Útil como herramienta de screening
   • Debe complementarse con evaluación profesional
   • Validar con datos externos

RECOMENDACIONES:
   • Usar umbral {config.THRESHOLD_ALT} para maximizar recall
   • Monitorear métricas en producción
   • Actualizar modelo periódicamente
""")

# Guardar resultados
print("\n" + "="*80)
print("GUARDANDO RESULTADOS")
print("="*80)

# Guardar métricas
import pandas as pd
metrics_df = pd.DataFrame({
    'Métrica': ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC-ROC'],
    'Valor': [metrics['accuracy'], metrics['precision'], metrics['recall'], 
              metrics['f1'], metrics['auc']]
})
metrics_df.to_csv('metricas_modelo.csv', index=False)
print("✓ metricas_modelo.csv")

# Guardar coeficientes
coef_df.to_csv('coeficientes_modelo.csv', index=False)
print("✓ coeficientes_modelo.csv")

# Guardar comparación de umbrales
threshold_comparison.to_csv('comparacion_umbrales.csv', index=False)
print("✓ comparacion_umbrales.csv")

print("\n" + "="*80)
print("✓ PROYECTO COMPLETADO")
print("="*80)

print("""
Archivos generados:
  📊 eda_analisis.png - Análisis exploratorio
  📊 resultados_completos.png - 6 gráficos del modelo
  📄 metricas_modelo.csv - Métricas de evaluación
  📄 coeficientes_modelo.csv - Coeficientes e importancia
  📄 comparacion_umbrales.csv - Comparación de umbrales

¡Proyecto finalizado! 🎉
""")
