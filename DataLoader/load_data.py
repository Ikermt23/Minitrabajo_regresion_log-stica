"""
DataLoader/load_data.py
Funciones para cargar datos y análisis estadístico básico
"""

import pandas as pd
import numpy as np
from scipy import stats


def load_life_style_data(file_path: str):
    """
    Carga el dataset, limpia duplicados y valores faltantes,
    y devuelve un DataFrame listo para análisis.
    """
    df = pd.read_csv(file_path)

    # Eliminar duplicados
    df = df.drop_duplicates()

    # Rellenar valores nulos de columnas importantes (ejemplo: edad)
    if 'edad' in df.columns:
        df['edad'].fillna(df['edad'].median(), inplace=True)

    # Eliminar filas que aún tengan NaN
    df = df.dropna()

    return df


def identify_column_types(df):
    """
    Identifica columnas numéricas y categóricas
    """
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    return numeric_cols, categorical_cols


# =============================================================================
# NUEVAS FUNCIONES PARA ANÁLISIS UNIVARIANTE
# =============================================================================

def describe_variable_nature(df, numeric_cols, categorical_cols):
    """
    Describe la naturaleza de cada variable (continua, discreta, categórica)
    
    Returns:
        DataFrame con descripción de cada variable
    """
    print("\n" + "=" * 80)
    print("NATURALEZA DE LAS VARIABLES")
    print("=" * 80)
    
    descriptions = []
    
    # Variables numéricas
    for col in numeric_cols:
        unique_count = df[col].nunique()
        total_count = len(df[col])
        unique_ratio = unique_count / total_count
        
        # Determinar si es continua o discreta
        if unique_ratio > 0.05 or unique_count > 20:
            nature = "Continua"
        else:
            nature = "Discreta"
        
        descriptions.append({
            'Variable': col,
            'Tipo': 'Numérica',
            'Naturaleza': nature,
            'Valores únicos': unique_count,
            'Rango': f"[{df[col].min():.2f}, {df[col].max():.2f}]"
        })
    
    # Variables categóricas
    for col in categorical_cols:
        unique_count = df[col].nunique()
        descriptions.append({
            'Variable': col,
            'Tipo': 'Categórica',
            'Naturaleza': 'Nominal',
            'Valores únicos': unique_count,
            'Rango': '-'
        })
    
    desc_df = pd.DataFrame(descriptions)
    print("\n", desc_df.to_string(index=False))
    
    return desc_df


def univariate_statistics(df, numeric_cols):
    """
    Calcula estadísticas descriptivas completas para variables numéricas
    
    Returns:
        DataFrame con estadísticas
    """
    print("\n" + "=" * 80)
    print("ESTADÍSTICAS DESCRIPTIVAS - VARIABLES NUMÉRICAS")
    print("=" * 80)
    
    stats_list = []
    
    for col in numeric_cols:
        stats_dict = {
            'Variable': col,
            'N': df[col].count(),
            'Media': df[col].mean(),
            'Mediana': df[col].median(),
            'Desv.Std': df[col].std(),
            'Mínimo': df[col].min(),
            'Q1': df[col].quantile(0.25),
            'Q3': df[col].quantile(0.75),
            'Máximo': df[col].max(),
            'Asimetría': df[col].skew(),
            'Curtosis': df[col].kurtosis()
        }
        stats_list.append(stats_dict)
    
    stats_df = pd.DataFrame(stats_list)
    print("\n", stats_df.to_string(index=False))
    
    # Interpretación de asimetría
    print("\n📊 Interpretación de Asimetría:")
    for col in numeric_cols:
        skew = df[col].skew()
        if abs(skew) < 0.5:
            interp = "distribución simétrica"
        elif skew > 0:
            interp = "sesgo positivo (cola derecha)"
        else:
            interp = "sesgo negativo (cola izquierda)"
        print(f"  • {col}: {skew:.2f} → {interp}")
    
    return stats_df


def detect_outliers(df, numeric_cols):
    """
    Detecta outliers usando el método IQR
    
    Returns:
        Dict con información de outliers por variable
    """
    print("\n" + "=" * 80)
    print("DETECCIÓN DE VALORES EXTREMOS (OUTLIERS)")
    print("=" * 80)
    
    outliers_info = {}
    
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        n_outliers = len(outliers)
        pct_outliers = (n_outliers / len(df)) * 100
        
        outliers_info[col] = {
            'count': n_outliers,
            'percentage': pct_outliers,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound
        }
        
        print(f"\n{col}:")
        print(f"  Límite inferior: {lower_bound:.2f}")
        print(f"  Límite superior: {upper_bound:.2f}")
        print(f"  Outliers detectados: {n_outliers} ({pct_outliers:.2f}%)")
        
        if pct_outliers > 10:
            print(f"  ⚠️ MÁS DEL 10% SON OUTLIERS - Considerar transformación")
        elif pct_outliers > 5:
            print(f"  ⚠️ Más del 5% son outliers - Revisar")
        else:
            print(f"  ✓ Porcentaje aceptable de outliers")
    
    return outliers_info


def analyze_class_balance(df, target):
    """
    Analiza el balanceo de la variable objetivo
    
    Returns:
        Dict con métricas de balance
    """
    print("\n" + "=" * 80)
    print("ANÁLISIS DE BALANCEO DE CLASES")
    print("=" * 80)
    
    counts = df[target].value_counts().sort_index()
    pcts = df[target].value_counts(normalize=True).sort_index() * 100
    
    print(f"\n📊 Distribución de '{target}':")
    for cls in counts.index:
        print(f"  Clase {cls}: {counts[cls]:,} observaciones ({pcts[cls]:.2f}%)")
    
    # Calcular ratio de balance
    ratio = min(counts) / max(counts)
    print(f"\n📈 Ratio de balance: {ratio:.3f}")
    
    # Interpretación
    if ratio >= 0.8:
        status = "✓ BALANCEADO"
        recommendation = "No se requieren técnicas especiales de balanceo"
    elif ratio >= 0.5:
        status = "⚠️ LIGERO DESBALANCE"
        recommendation = "Usar F1-score y considerar class_weight='balanced'"
    else:
        status = "❌ DESBALANCE SEVERO"
        recommendation = "Aplicar técnicas de balanceo (SMOTE, undersampling)"
    
    print(f"\nEstado: {status}")
    print(f"Recomendación: {recommendation}")
    
    # Consecuencias del desbalance
    print("\n📋 Posibles consecuencias del desbalance:")
    if ratio < 0.8:
        print("  • El modelo puede sesgarse hacia la clase mayoritaria")
        print("  • Accuracy alto pero modelo potencialmente inútil")
        print("  • Baja capacidad para detectar la clase minoritaria")
        print("  • Necesidad de usar métricas alternativas (F1, Precision, Recall)")
    else:
        print("  • No se esperan problemas significativos por desbalance")
    
    return {
        'counts': counts.to_dict(),
        'percentages': pcts.to_dict(),
        'ratio': ratio,
        'is_balanced': ratio >= 0.8,
        'recommendation': recommendation
    }


# =============================================================================
# NUEVAS FUNCIONES PARA ANÁLISIS BIVARIANTE
# =============================================================================

def correlation_analysis(df, numeric_cols, threshold=0.7):
    """
    Análisis detallado de correlaciones
    
    Returns:
        Tuple (correlation_matrix, high_correlations)
    """
    print("\n" + "=" * 80)
    print("ANÁLISIS DE CORRELACIÓN (MULTICOLINEALIDAD)")
    print("=" * 80)
    
    corr_matrix = df[numeric_cols].corr()
    
    # Identificar pares con alta correlación
    high_corr_pairs = []
    
    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):
            corr_value = corr_matrix.iloc[i, j]
            if abs(corr_value) > threshold:
                high_corr_pairs.append({
                    'Variable 1': corr_matrix.columns[i],
                    'Variable 2': corr_matrix.columns[j],
                    'Correlación': corr_value
                })
    
    print(f"\n🔗 Pares con correlación alta (|r| > {threshold}):")
    
    if high_corr_pairs:
        for pair in high_corr_pairs:
            print(f"  • {pair['Variable 1']} ↔ {pair['Variable 2']}: r = {pair['Correlación']:.3f}")
        
        print(f"\n⚠️ MULTICOLINEALIDAD DETECTADA")
        print("Implicaciones:")
        print("  • Los coeficientes del modelo pueden ser inestables")
        print("  • Dificulta la interpretación individual de variables")
        print("  • Considerar eliminar una variable de cada par correlacionado")
    else:
        print("  ✓ No se detectó multicolinealidad significativa")
    
    return corr_matrix, high_corr_pairs


def variable_target_tests(df, numeric_cols, target):
    """
    Tests estadísticos para relación variable-target
    
    Returns:
        DataFrame con resultados de tests
    """
    print("\n" + "=" * 80)
    print("TESTS ESTADÍSTICOS: VARIABLES vs TARGET")
    print("=" * 80)
    
    results = []
    
    for col in numeric_cols:
        # Separar por clase
        classes = df[target].unique()
        groups = [df[df[target] == cls][col].dropna() for cls in sorted(classes)]
        
        # Estadísticas por grupo
        means = [g.mean() for g in groups]
        medians = [g.median() for g in groups]
        
        # Test de normalidad (Shapiro-Wilk)
        normality_tests = []
        for g in groups:
            if len(g) > 3:
                sample = g.sample(min(5000, len(g)))
                _, p_norm = stats.shapiro(sample)
                normality_tests.append(p_norm > 0.05)
            else:
                normality_tests.append(False)
        
        # Elegir test apropiado
        if all(normality_tests) and len(groups) == 2:
            # t-test si ambos grupos son normales
            stat, p_value = stats.ttest_ind(groups[0], groups[1])
            test_name = 't-test'
        elif len(groups) == 2:
            # Mann-Whitney si no son normales
            stat, p_value = stats.mannwhitneyu(groups[0], groups[1])
            test_name = 'Mann-Whitney'
        else:
            # Kruskal-Wallis para más de 2 grupos
            stat, p_value = stats.kruskal(*groups)
            test_name = 'Kruskal-Wallis'
        
        is_significant = p_value < 0.05
        
        result = {
            'Variable': col,
            'Test': test_name,
            'Estadístico': stat,
            'p-value': p_value,
            'Significativa': '✓' if is_significant else '✗',
            'Diferencia medias': abs(means[0] - means[1]) if len(means) == 2 else np.std(means)
        }
        
        results.append(result)
        
        print(f"\n{col}:")
        for i, cls in enumerate(sorted(classes)):
            print(f"  Clase {cls}: media = {means[i]:.2f}, mediana = {medians[i]:.2f}")
        print(f"  {test_name}: estadístico = {stat:.3f}, p-value = {p_value:.4f}")
        
        if is_significant:
            print(f"  ✓ DIFERENCIA SIGNIFICATIVA (p < 0.05)")
            print(f"  → Variable relevante para predecir {target}")
        else:
            print(f"  ✗ No hay diferencia significativa")
            print(f"  → Variable posiblemente poco útil")
    
    results_df = pd.DataFrame(results)
    print("\n📊 Resumen de tests (ordenado por p-value):")
    print(results_df.sort_values('p-value')[['Variable', 'Test', 'p-value', 'Significativa']].to_string(index=False))
    
    return results_df


def categorical_target_analysis(df, categorical_cols, target):
    """
    Análisis de relación entre variables categóricas y target
    
    Returns:
        List de resultados de chi-cuadrado
    """
    if not categorical_cols:
        return []
    
    print("\n" + "=" * 80)
    print("ANÁLISIS: VARIABLES CATEGÓRICAS vs TARGET")
    print("=" * 80)
    
    results = []
    
    for col in categorical_cols:
        # Tabla de contingencia
        contingency_table = pd.crosstab(df[col], df[target])
        
        # Test chi-cuadrado
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        
        is_significant = p_value < 0.05
        
        result = {
            'Variable': col,
            'Chi-cuadrado': chi2,
            'p-value': p_value,
            'Significativa': '✓' if is_significant else '✗'
        }
        
        results.append(result)
        
        print(f"\n{col}:")
        print("Tabla de contingencia:")
        print(contingency_table.to_string())
        print(f"Chi-cuadrado: {chi2:.3f}, p-value: {p_value:.4f}")
        
        if is_significant:
            print(f"✓ RELACIÓN SIGNIFICATIVA con {target}")
        else:
            print(f"✗ No hay relación significativa")
    
    return results
