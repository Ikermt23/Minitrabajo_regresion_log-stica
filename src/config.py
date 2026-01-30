"""
config.py
Configuración centralizada del proyecto
"""

import os

# =============================================================================
# CARPETAS
# =============================================================================
DATA_DIR = "data"
OUTPUT_DIR = "outputs"

# Crear carpeta outputs si no existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =============================================================================
# DATOS
# =============================================================================
DATA_PATH = os.path.join(DATA_DIR, "newdata.csv")
TARGET_COL = 'is_healthy'

# Variables a usar en el modelo
FEATURES = [
    'Age', 'Weight (kg)', 'Height (m)', 'BMI',
    'Calories_Burned', 'Water_Intake (liters)',
    'Workout_Frequency (days/week)', 'Session_Duration (hours)',
    'Calories', 'Proteins', 'Carbs', 'Fats'
]

# =============================================================================
# MODELO
# =============================================================================
TEST_SIZE = 0.2
RANDOM_STATE = 42
MAX_ITER = 1000
CLASS_WEIGHT = 'balanced'

# Umbrales
THRESHOLD_DEFAULT = 0.5
THRESHOLD_ALT = 0.4

# =============================================================================
# VISUALIZACIÓN
# =============================================================================
FIGSIZE = (15, 10)
DPI = 300
STYLE = 'whitegrid'
