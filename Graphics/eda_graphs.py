"""
Graphics/eda_graphs.py
Funciones para generar todos los gráficos del EDA
"""

import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
import numpy as np

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 5)


def create_class_folders(df, target, output_folder):
    """
    Crea subcarpetas por clase para guardar gráficos
    """
    class_folders = {}
    for cls in sorted(df[target].unique()):
        cls_folder = os.path.join(output_folder, f'Class_{cls}')
        os.makedirs(cls_folder, exist_ok=True)
        class_folders[cls] = cls_folder
    return class_folders


def save_numeric_graphs(df, numeric_cols, target, output_folder):
    """
    Boxplots e histogramas de variables numéricas por clase
    """
    class_folders = create_class_folders(df, target, output_folder)
    for cls in class_folders:
        subset = df[df[target] == cls]
        folder = class_folders[cls]
        for col in numeric_cols:
            # Boxplot
            plt.figure()
            sns.boxplot(y=subset[col], color='skyblue')
            plt.title(f'Boxplot {col} - Clase {cls}')
            plt.ylabel(col)
            plt.savefig(f'{folder}/boxplot_{col}.png')
            plt.close()

            # Histograma
            plt.figure()
            sns.histplot(subset[col], bins=30, kde=True, color='salmon')
            plt.title(f'Histograma {col} - Clase {cls}')
            plt.xlabel(col)
            plt.ylabel('Frecuencia')
            plt.savefig(f'{folder}/hist_{col}.png')
            plt.close()


def save_categorical_graphs(df, categorical_cols, target, output_folder):
    """
    Gráficos de barras de variables categóricas por clase
    """
    if not categorical_cols:
        print("No hay variables categóricas para graficar")
        return
    
    class_folders = create_class_folders(df, target, output_folder)
    for cls in class_folders:
        subset = df[df[target] == cls]
        folder = class_folders[cls]
        for col in categorical_cols:
            plt.figure()
            subset[col].value_counts().plot(kind='bar', color='lightgreen', edgecolor='black')
            plt.title(f'{col} - Clase {cls}')
            plt.ylabel('Frecuencia')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f'{folder}/cat_{col}.png')
            plt.close()


def correlation_matrix(df, numeric_cols, output_folder):
    """
    Calcula y guarda la matriz de correlación de variables numéricas
    """
    corr = df[numeric_cols].corr()
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', center=0)
    plt.title("Matriz de correlación entre variables numéricas")
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'correlation_matrix.png'))
    plt.close()
    return corr


# =============================================================================
# NUEVAS FUNCIONES DE VISUALIZACIÓN
# =============================================================================

def plot_distributions_comparison(df, numeric_cols, target, output_folder):
    """
    Histogramas superpuestos comparando clases
    """
    print("Generando comparación de distribuciones por clase...")
    
    n_cols = len(numeric_cols)
    n_rows = (n_cols + 2) // 3
    
    fig, axes = plt.subplots(n_rows, 3, figsize=(15, 5 * n_rows))
    axes = axes.flatten() if n_cols > 1 else [axes]
    
    colors = ['#FF6B6B', '#4ECDC4']
    classes = sorted(df[target].unique())
    
    for idx, col in enumerate(numeric_cols):
        ax = axes[idx]
        
        for i, cls in enumerate(classes):
            subset = df[df[target] == cls][col]
            ax.hist(subset, bins=30, alpha=0.6, label=f'Clase {cls}', 
                   color=colors[i % len(colors)], edgecolor='black')
        
        ax.set_title(f'Distribución de {col} por Clase', fontweight='bold')
        ax.set_xlabel(col)
        ax.set_ylabel('Frecuencia')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    # Ocultar ejes vacíos
    for idx in range(n_cols, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'distributions_comparison.png'), dpi=300)
    plt.close()
    print(f"✓ Guardado: distributions_comparison.png")


def plot_boxplots_comparison(df, numeric_cols, target, output_folder):
    """
    Boxplots comparativos por clase
    """
    print("Generando boxplots comparativos...")
    
    n_cols = len(numeric_cols)
    n_rows = (n_cols + 2) // 3
    
    fig, axes = plt.subplots(n_rows, 3, figsize=(15, 5 * n_rows))
    axes = axes.flatten() if n_cols > 1 else [axes]
    
    colors = ['#FF6B6B', '#4ECDC4']
    
    for idx, col in enumerate(numeric_cols):
        ax = axes[idx]
        
        # Preparar datos para boxplot
        classes = sorted(df[target].unique())
        data_to_plot = [df[df[target] == cls][col].dropna() for cls in classes]
        
        bp = ax.boxplot(data_to_plot, labels=[f'Clase {cls}' for cls in classes],
                       patch_artist=True)
        
        # Colorear las cajas
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
        
        ax.set_title(f'{col} por Clase', fontweight='bold')
        ax.set_ylabel(col)
        ax.grid(True, alpha=0.3, axis='y')
    
    # Ocultar ejes vacíos
    for idx in range(n_cols, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'boxplots_comparison.png'), dpi=300)
    plt.close()
    print(f"✓ Guardado: boxplots_comparison.png")


def plot_target_distribution(df, target, output_folder):
    """
    Gráfico de distribución de la variable objetivo
    """
    print("Generando gráfico de distribución del target...")
    
    counts = df[target].value_counts().sort_index()
    pcts = (counts / len(df)) * 100
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Gráfico de barras
    colors = ['#FF6B6B', '#4ECDC4']
    bars = ax1.bar(counts.index, counts.values, color=colors, edgecolor='black', linewidth=1.5)
    ax1.set_xlabel('Clase', fontsize=12)
    ax1.set_ylabel('Frecuencia', fontsize=12)
    ax1.set_title('Distribución de la Variable Objetivo', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Añadir valores sobre las barras
    for bar, count, pct in zip(bars, counts.values, pcts.values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{count:,}\n({pct:.1f}%)',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Gráfico de pastel
    ax2.pie(counts.values, labels=[f'Clase {i}' for i in counts.index],
           autopct='%1.1f%%', colors=colors, startangle=90,
           explode=[0.05] * len(counts), shadow=True)
    ax2.set_title('Proporción de Clases', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'target_distribution.png'), dpi=300)
    plt.close()
    print(f"✓ Guardado: target_distribution.png")


def plot_outliers_summary(df, numeric_cols, output_folder):
    """
    Resumen visual de outliers en todas las variables
    """
    print("Generando resumen de outliers...")
    
    outliers_data = []
    
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        n_outliers = len(df[(df[col] < lower_bound) | (df[col] > upper_bound)])
        pct_outliers = (n_outliers / len(df)) * 100
        
        outliers_data.append({
            'Variable': col,
            'Porcentaje': pct_outliers
        })
    
    outliers_df = pd.DataFrame(outliers_data)
    
    # Gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = ['red' if x > 10 else 'orange' if x > 5 else 'green' 
             for x in outliers_df['Porcentaje']]
    
    bars = ax.barh(outliers_df['Variable'], outliers_df['Porcentaje'], 
                   color=colors, edgecolor='black')
    
    ax.set_xlabel('Porcentaje de Outliers (%)', fontsize=12)
    ax.set_title('Porcentaje de Outliers por Variable', fontsize=14, fontweight='bold')
    ax.axvline(5, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='5% umbral')
    ax.axvline(10, color='red', linestyle='--', linewidth=2, alpha=0.7, label='10% umbral')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='x')
    
    # Añadir valores
    for bar, val in zip(bars, outliers_df['Porcentaje']):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
               f'{val:.1f}%',
               ha='left', va='center', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'outliers_summary.png'), dpi=300)
    plt.close()
    print(f"✓ Guardado: outliers_summary.png")


def plot_correlation_heatmap_annotated(df, numeric_cols, output_folder, threshold=0.7):
    """
    Heatmap de correlación con anotaciones de multicolinealidad
    """
    print("Generando heatmap de correlación mejorado...")
    
    corr = df[numeric_cols].corr()
    
    # Crear máscara para valores por encima del umbral
    mask_high_corr = np.abs(corr) > threshold
    np.fill_diagonal(mask_high_corr.values, False)
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Heatmap base
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', center=0,
               square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
    
    # Resaltar correlaciones altas
    for i in range(len(corr)):
        for j in range(len(corr)):
            if mask_high_corr.iloc[i, j]:
                ax.add_patch(plt.Rectangle((j, i), 1, 1, fill=False, 
                                          edgecolor='black', lw=3))
    
    ax.set_title("Matriz de Correlación\n(Recuadros negros = |r| > 0.7)", 
                fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'correlation_matrix_annotated.png'), dpi=300)
    plt.close()
    print(f"✓ Guardado: correlation_matrix_annotated.png")


def plot_variable_importance_by_pvalue(results_df, output_folder):
    """
    Gráfico de importancia de variables según p-value
    
    Args:
        results_df: DataFrame con resultados de tests estadísticos
    """
    print("Generando gráfico de importancia de variables...")
    
    # Ordenar por p-value
    results_sorted = results_df.sort_values('p-value')
    
    # Crear colores según significancia
    colors = ['green' if p < 0.01 else 'orange' if p < 0.05 else 'red' 
             for p in results_sorted['p-value']]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.barh(results_sorted['Variable'], -np.log10(results_sorted['p-value']),
                   color=colors, edgecolor='black')
    
    ax.set_xlabel('-log10(p-value)', fontsize=12)
    ax.set_title('Importancia de Variables para Predecir el Target\n(Mayor valor = más significativa)',
                fontsize=14, fontweight='bold')
    
    # Líneas de referencia
    ax.axvline(-np.log10(0.05), color='orange', linestyle='--', 
              linewidth=2, alpha=0.7, label='p=0.05')
    ax.axvline(-np.log10(0.01), color='green', linestyle='--', 
              linewidth=2, alpha=0.7, label='p=0.01')
    
    ax.legend()
    ax.grid(True, alpha=0.3, axis='x')
    
    # Añadir valores de p
    for bar, pval in zip(bars, results_sorted['p-value']):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
               f' p={pval:.4f}',
               ha='left', va='center', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'variable_importance.png'), dpi=300)
    plt.close()
    print(f"✓ Guardado: variable_importance.png")


def save_all_summary_graphs(df, numeric_cols, categorical_cols, target, output_folder):
    """
    Genera todos los gráficos adicionales de resumen
    """
    print("\n" + "=" * 80)
    print("GENERANDO GRÁFICOS DE RESUMEN")
    print("=" * 80)
    
    # Distribución del target
    plot_target_distribution(df, target, output_folder)
    
    # Comparación de distribuciones
    plot_distributions_comparison(df, numeric_cols, target, output_folder)
    
    # Comparación de boxplots
    plot_boxplots_comparison(df, numeric_cols, target, output_folder)
    
    # Resumen de outliers
    plot_outliers_summary(df, numeric_cols, output_folder)
    
    # Heatmap anotado
    plot_correlation_heatmap_annotated(df, numeric_cols, output_folder)
    
    print("\n✅ Todos los gráficos de resumen generados")
