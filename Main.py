"""
main.py - EDA COMPLETO para Regresión Logística
Incluye análisis univariante y bivariante completo
"""

import os
import pandas as pd
from DataLoader.load_data import (
    load_life_style_data, 
    identify_column_types,
    describe_variable_nature,
    univariate_statistics,
    detect_outliers,
    analyze_class_balance,
    correlation_analysis,
    variable_target_tests,
    categorical_target_analysis
)
from Graphics.eda_graphs import (
    save_numeric_graphs, 
    save_categorical_graphs, 
    correlation_matrix,
    save_all_summary_graphs,
    plot_variable_importance_by_pvalue
)

# =============================================================================
# CONFIGURACIÓN
# =============================================================================
file_path = 'data/newdata.csv'  # Ajusta la ruta a tu archivo
output_folder = 'output'
target = 'is_healthy'           # Variable objetivo: 0 = no saludable, 1 = saludable

os.makedirs(output_folder, exist_ok=True)

print("=" * 80)
print("EDA COMPLETO - PREDICCIÓN DE ESTILO DE VIDA SALUDABLE")
print("=" * 80)

# =============================================================================
# PASO 1: CARGA Y LIMPIEZA DE DATOS
# =============================================================================
print("\n🔄 PASO 1: Cargando y limpiando datos...")

df = load_life_style_data(file_path)

print(f"✓ Dataset cargado: {len(df)} filas, {len(df.columns)} columnas")

# IMPORTANTE: Convertir is_healthy a binaria si no lo es
if target in df.columns:
    # Verificar si tiene valores fuera de 0/1
    if df[target].min() < 0 or df[target].max() > 1 or not all(df[target].isin([0, 1])):
        print(f"\n⚠️ '{target}' tiene valores no binarios. Convirtiendo...")
        # Redondear a 0 o 1
        df[target] = df[target].round().astype(int)
        # Asegurar que solo tenga 0 y 1
        df[target] = df[target].clip(0, 1)
        print(f"✓ '{target}' convertida a binaria (0/1)")
else:
    raise ValueError(f"❌ La columna '{target}' no existe en el dataset")

# Identificar columnas
numeric_cols, categorical_cols = identify_column_types(df)
if target in numeric_cols: 
    numeric_cols.remove(target)
if target in categorical_cols: 
    categorical_cols.remove(target)

print(f"\nVariables numéricas ({len(numeric_cols)}): {numeric_cols}")
print(f"Variables categóricas ({len(categorical_cols)}): {categorical_cols}")

# =============================================================================
# EJERCICIO 3.1: ANÁLISIS UNIVARIANTE
# =============================================================================
print("\n" + "=" * 80)
print("EJERCICIO 3.1: ANÁLISIS UNIVARIANTE")
print("=" * 80)

# 3.1.1 Naturaleza de las variables
print("\n📊 3.1.1 - Descripción de la naturaleza de variables")
nature_df = describe_variable_nature(df, numeric_cols, categorical_cols)

# Guardar tabla
nature_df.to_csv(os.path.join(output_folder, 'variable_nature.csv'), index=False)
print(f"✓ Tabla guardada: variable_nature.csv")

# 3.1.2 Estadísticas descriptivas
print("\n📊 3.1.2 - Estadísticas descriptivas")
stats_df = univariate_statistics(df, numeric_cols)

# Guardar tabla
stats_df.to_csv(os.path.join(output_folder, 'descriptive_statistics.csv'), index=False)
print(f"✓ Tabla guardada: descriptive_statistics.csv")

# 3.1.3 Detección de outliers
print("\n📊 3.1.3 - Detección de valores extremos")
outliers_info = detect_outliers(df, numeric_cols)

# Guardar resumen de outliers
outliers_summary = pd.DataFrame([
    {'Variable': k, 'N_Outliers': v['count'], 'Porcentaje': v['percentage']}
    for k, v in outliers_info.items()
])
outliers_summary.to_csv(os.path.join(output_folder, 'outliers_summary.csv'), index=False)
print(f"✓ Tabla guardada: outliers_summary.csv")

# 3.1.4 Balanceo de clases (variable objetivo)
print("\n📊 3.1.4 - Análisis de balanceo de clases")
balance_info = analyze_class_balance(df, target)

# Guardar información de balance
balance_df = pd.DataFrame([
    {'Clase': k, 'Frecuencia': v, 'Porcentaje': balance_info['percentages'][k]}
    for k, v in balance_info['counts'].items()
])
balance_df['Ratio_Balance'] = balance_info['ratio']
balance_df['Recomendacion'] = balance_info['recommendation']
balance_df.to_csv(os.path.join(output_folder, 'class_balance.csv'), index=False)
print(f"✓ Tabla guardada: class_balance.csv")

# =============================================================================
# GRÁFICOS UNIVARIANTES
# =============================================================================
print("\n📈 Generando gráficos univariantes...")

# Gráficos por clase (originales)
save_numeric_graphs(df, numeric_cols, target, output_folder)
print(f"✓ Boxplots e histogramas por clase guardados en carpetas Class_X/")

if categorical_cols:
    save_categorical_graphs(df, categorical_cols, target, output_folder)
    print(f"✓ Gráficos categóricos guardados")

# Gráficos de resumen adicionales
save_all_summary_graphs(df, numeric_cols, categorical_cols, target, output_folder)

# =============================================================================
# EJERCICIO 3.2: ANÁLISIS BIVARIANTE
# =============================================================================
print("\n" + "=" * 80)
print("EJERCICIO 3.2: ANÁLISIS BIVARIANTE")
print("=" * 80)

# 3.2.1 Correlación entre variables (multicolinealidad)
print("\n📊 3.2.1 - Análisis de correlación y multicolinealidad")
corr_matrix, high_corr_pairs = correlation_analysis(df, numeric_cols, threshold=0.7)

# Guardar matriz de correlación
corr_matrix.to_csv(os.path.join(output_folder, 'correlation_matrix.csv'))
print(f"✓ Matriz de correlación guardada: correlation_matrix.csv")

# Guardar pares de alta correlación
if high_corr_pairs:
    high_corr_df = pd.DataFrame(high_corr_pairs)
    high_corr_df.to_csv(os.path.join(output_folder, 'high_correlations.csv'), index=False)
    print(f"✓ Pares de alta correlación guardados: high_correlations.csv")

# 3.2.2 Relación variable explicativa ↔ variable objetivo
print("\n📊 3.2.2 - Tests estadísticos: Variables vs Target")
test_results = variable_target_tests(df, numeric_cols, target)

# Guardar resultados de tests
test_results.to_csv(os.path.join(output_folder, 'variable_target_tests.csv'), index=False)
print(f"✓ Resultados de tests guardados: variable_target_tests.csv")

# Gráfico de importancia de variables
plot_variable_importance_by_pvalue(test_results, output_folder)

# 3.2.3 Variables categóricas vs target (si existen)
if categorical_cols:
    print("\n📊 3.2.3 - Análisis de variables categóricas vs target")
    cat_results = categorical_target_analysis(df, categorical_cols, target)
    
    if cat_results:
        cat_results_df = pd.DataFrame(cat_results)
        cat_results_df.to_csv(os.path.join(output_folder, 'categorical_tests.csv'), index=False)
        print(f"✓ Tests categóricos guardados: categorical_tests.csv")

# Gráfico de correlación (original)
corr = correlation_matrix(df, numeric_cols, output_folder)
print(f"✓ Heatmap de correlación guardado: correlation_matrix.png")

# =============================================================================
# RESUMEN FINAL
# =============================================================================
print("\n" + "=" * 80)
print("✅ EDA COMPLETADO EXITOSAMENTE")
print("=" * 80)

print(f"""
📊 RESUMEN EJECUTIVO:

Dataset:
  • Total de observaciones: {len(df):,}
  • Variables numéricas: {len(numeric_cols)}
  • Variables categóricas: {len(categorical_cols)}

Variable Objetivo '{target}':
  • Clases: {list(balance_info['counts'].keys())}
  • Ratio de balance: {balance_info['ratio']:.3f}
  • Estado: {"Balanceado" if balance_info['is_balanced'] else "Desbalanceado"}

Outliers:
  • Variables con >5% outliers: {sum(1 for v in outliers_info.values() if v['percentage'] > 5)}
  • Variables con >10% outliers: {sum(1 for v in outliers_info.values() if v['percentage'] > 10)}

Multicolinealidad:
  • Pares de variables con |r| > 0.7: {len(high_corr_pairs)}

Relación con Target:
  • Variables significativas (p < 0.05): {len(test_results[test_results['p-value'] < 0.05])}
  • Variables no significativas: {len(test_results[test_results['p-value'] >= 0.05])}

📁 ARCHIVOS GENERADOS:
""")

# Listar archivos generados
all_files = []
for root, dirs, files in os.walk(output_folder):
    for file in files:
        rel_path = os.path.relpath(os.path.join(root, file), output_folder)
        all_files.append(rel_path)

# Separar por tipo
csv_files = [f for f in all_files if f.endswith('.csv')]
png_files = [f for f in all_files if f.endswith('.png')]

print("\n📄 Tablas CSV:")
for f in sorted(csv_files):
    print(f"  • {f}")

print("\n📊 Gráficos PNG:")
for f in sorted(png_files):
    print(f"  • {f}")

print(f"""
📝 PRÓXIMOS PASOS:

1. Revisar los archivos CSV con las tablas de análisis
2. Examinar los gráficos generados para interpretación visual
3. Documentar hallazgos en el informe (Ejercicio 3)
4. Tomar decisiones de preprocesamiento basadas en:
   • Outliers detectados
   • Variables correlacionadas (multicolinealidad)
   • Variables significativas vs no significativas
   • Balance de clases

5. Continuar con Ejercicio 4: Teoría de Regresión Logística

¡EDA finalizado! 🎉
Todos los resultados están en la carpeta '{output_folder}/'
""")
