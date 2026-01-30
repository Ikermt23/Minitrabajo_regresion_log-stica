"""
data_processing.py
Funciones para cargar y preparar los datos
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from src import config


def load_data():
    """Carga el dataset y hace limpieza básica"""
    print("📂 Cargando datos...")
    df = pd.read_csv(config.DATA_PATH)
    
    # Eliminar nulos
    df = df.dropna()
    
    # Convertir target a binario
    df[config.TARGET_COL] = df[config.TARGET_COL].round().clip(0, 1).astype(int)
    
    print(f"✓ Dataset: {len(df)} filas, {len(df.columns)} columnas")
    return df


def prepare_data(df):
    """Prepara datos para el modelo: escalado y división train/test"""
    print("\n🔧 Preparando datos...")
    
    # Separar X e y
    X = df[config.FEATURES]
    y = df[config.TARGET_COL]
    
    # Escalar variables
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y,
        test_size=config.TEST_SIZE,
        random_state=config.RANDOM_STATE,
        stratify=y
    )
    
    print(f"✓ Train: {len(X_train)}, Test: {len(X_test)}")
    print(f"✓ Variables escaladas con StandardScaler")
    
    return X_train, X_test, y_train, y_test, scaler


def get_eda_stats(df):
    """Obtiene estadísticas para el EDA"""
    # Balance de clases
    y = df[config.TARGET_COL]
    counts = y.value_counts()
    ratio = counts.min() / counts.max()
    
    # Correlaciones con target
    correlations = pd.DataFrame({
        'Variable': config.FEATURES,
        'Correlación': [df[col].corr(y) for col in config.FEATURES]
    }).sort_values('Correlación', key=abs, ascending=False)
    
    stats = {
        'counts': counts,
        'ratio': ratio,
        'correlations': correlations
    }
    
    return stats
