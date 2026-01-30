"""
visualizations.py
Todas las visualizaciones del proyecto
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import roc_curve
import config


def create_all_plots(model, X_test, y_test, y_proba, y_pred, metrics, coef_df):
    """Crea todos los gráficos en una sola figura"""
    print("\n📊 Generando visualizaciones...")
    
    sns.set_style(config.STYLE)
    fig = plt.figure(figsize=config.FIGSIZE)
    
    # 1. Distribución de probabilidades
    ax1 = plt.subplot(2, 3, 1)
    plt.hist(y_proba[y_test==0], bins=30, alpha=0.6, label='No saludable', color='red', edgecolor='black')
    plt.hist(y_proba[y_test==1], bins=30, alpha=0.6, label='Saludable', color='green', edgecolor='black')
    plt.axvline(config.THRESHOLD_DEFAULT, color='black', linestyle='--', linewidth=2, label=f'Umbral {config.THRESHOLD_DEFAULT}')
    plt.xlabel('Probabilidad Predicha')
    plt.ylabel('Frecuencia')
    plt.title('Distribución de Probabilidades por Clase', fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 2. Curva ROC
    ax2 = plt.subplot(2, 3, 2)
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    plt.plot(fpr, tpr, linewidth=2.5, color='darkblue', label=f'AUC = {metrics["auc"]:.3f}')
    plt.plot([0, 1], [0, 1], 'k--', linewidth=1.5, label='Azar')
    plt.xlabel('Tasa Falsos Positivos (FPR)')
    plt.ylabel('Tasa Verdaderos Positivos (TPR)')
    plt.title('Curva ROC', fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 3. Matriz de confusión
    ax3 = plt.subplot(2, 3, 3)
    sns.heatmap(metrics['cm'], annot=True, fmt='d', cmap='Blues', cbar=False, 
                annot_kws={'size': 14, 'weight': 'bold'})
    plt.xlabel('Predicho')
    plt.ylabel('Real')
    plt.title('Matriz de Confusión', fontweight='bold')
    
    # 4. Top coeficientes
    ax4 = plt.subplot(2, 3, 4)
    top_coef = coef_df.head(10).sort_values('Coeficiente')
    colors = ['red' if x < 0 else 'green' for x in top_coef['Coeficiente']]
    y_pos = np.arange(len(top_coef))
    plt.barh(y_pos, top_coef['Coeficiente'], color=colors, edgecolor='black')
    plt.yticks(y_pos, top_coef['Variable'], fontsize=9)
    plt.xlabel('Coeficiente')
    plt.title('Top 10 Variables Más Influyentes', fontweight='bold')
    plt.axvline(0, color='black', linewidth=0.8)
    plt.grid(True, alpha=0.3, axis='x')
    
    # 5. Métricas vs umbral
    ax5 = plt.subplot(2, 3, 5)
    umbrales = np.linspace(0.2, 0.8, 30)
    
    from sklearn.metrics import precision_score, recall_score, f1_score
    precisions = [precision_score(y_test, (y_proba >= t).astype(int), zero_division=0) for t in umbrales]
    recalls = [recall_score(y_test, (y_proba >= t).astype(int), zero_division=0) for t in umbrales]
    f1s = [f1_score(y_test, (y_proba >= t).astype(int), zero_division=0) for t in umbrales]
    
    plt.plot(umbrales, precisions, marker='o', linewidth=2, label='Precision', color='blue')
    plt.plot(umbrales, recalls, marker='s', linewidth=2, label='Recall', color='orange')
    plt.plot(umbrales, f1s, marker='^', linewidth=2, label='F1-Score', color='green')
    plt.axvline(config.THRESHOLD_DEFAULT, color='black', linestyle='--', alpha=0.5, label=f'Umbral {config.THRESHOLD_DEFAULT}')
    plt.axvline(config.THRESHOLD_ALT, color='red', linestyle=':', alpha=0.7, label=f'Umbral {config.THRESHOLD_ALT}')
    plt.xlabel('Umbral de Decisión')
    plt.ylabel('Valor')
    plt.title('Trade-off: Precision vs Recall', fontweight='bold')
    plt.legend(fontsize=8)
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 1.05)
    
    # 6. Resumen de métricas
    ax6 = plt.subplot(2, 3, 6)
    metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC']
    values = [metrics['accuracy'], metrics['precision'], metrics['recall'], 
              metrics['f1'], metrics['auc']]
    
    colors_bar = ['green' if v > 0.7 else 'orange' if v > 0.6 else 'red' for v in values]
    bars = plt.bar(metrics_names, values, color=colors_bar, edgecolor='black', linewidth=1.5)
    
    # Añadir valores encima
    for bar, val in zip(bars, values):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.3f}', ha='center', va='bottom', fontweight='bold')
    
    plt.ylabel('Valor')
    plt.title('Resumen de Métricas', fontweight='bold')
    plt.ylim(0, 1.1)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('resultados_completos.png', dpi=config.DPI, bbox_inches='tight')
    print("✓ Visualizaciones guardadas: resultados_completos.png")
    plt.close()


def plot_eda(df, stats):
    """Crea gráficos del EDA"""
    print("\n📊 Generando gráficos EDA...")
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Balance de clases
    ax1 = axes[0]
    counts = stats['counts']
    ax1.bar(['No saludable (0)', 'Saludable (1)'], counts.values, 
            color=['red', 'green'], edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Frecuencia')
    ax1.set_title('Balance de Clases', fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Añadir valores
    for i, (val, pct) in enumerate(zip(counts.values, (counts/counts.sum()*100).values)):
        ax1.text(i, val, f'{val:,}\n({pct:.1f}%)', 
                ha='center', va='bottom', fontweight='bold')
    
    # Correlaciones
    ax2 = axes[1]
    top_corr = stats['correlations'].head(10)
    colors = ['red' if x < 0 else 'green' for x in top_corr['Correlación']]
    y_pos = np.arange(len(top_corr))
    ax2.barh(y_pos, top_corr['Correlación'], color=colors, edgecolor='black')
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(top_corr['Variable'], fontsize=9)
    ax2.set_xlabel('Correlación con Target')
    ax2.set_title('Top 10 Correlaciones', fontweight='bold')
    ax2.axvline(0, color='black', linewidth=0.8)
    ax2.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig('eda_analisis.png', dpi=300, bbox_inches='tight')
    print("✓ Gráficos EDA guardados: eda_analisis.png")
    plt.close()
