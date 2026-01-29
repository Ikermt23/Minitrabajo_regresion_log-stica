import os
from DataLoader.load_data import load_life_style_data, identify_column_types
from Graphics.eda_graphs import save_numeric_graphs, save_categorical_graphs, correlation_matrix

# -----------------------
# CONFIGURACIÓN
# -----------------------
file_path = 'data/newdata.csv'  # Ajusta la ruta
output_folder = 'output'
target = 'deficit_calorico'     # Variable objetivo 0/1

os.makedirs(output_folder, exist_ok=True)

# -----------------------
# CARGA Y LIMPIEZA DE DATOS
# -----------------------
df = load_life_style_data(file_path)

# Identificar columnas
numeric_cols, categorical_cols = identify_column_types(df)
if target in numeric_cols: numeric_cols.remove(target)
if target in categorical_cols: categorical_cols.remove(target)

print("Variables numéricas:", numeric_cols)
print("Variables categóricas:", categorical_cols)

# -----------------------
# ANÁLISIS UNIVARIANTE
# -----------------------
save_numeric_graphs(df, numeric_cols, target, output_folder)
save_categorical_graphs(df, categorical_cols, target, output_folder)

# -----------------------
# ANÁLISIS BIVARIANTE
# -----------------------
corr = correlation_matrix(df, numeric_cols, output_folder)
print("EDA completado. Todos los gráficos se guardaron en la carpeta 'output/'")