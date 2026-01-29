import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10,5)

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
        subset = df[df[target]==cls]
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
    class_folders = create_class_folders(df, target, output_folder)
    for cls in class_folders:
        subset = df[df[target]==cls]
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
    plt.figure(figsize=(12,10))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', center=0)
    plt.title("Matriz de correlación entre variables numéricas")
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder,'correlation_matrix.png'))
    plt.close()
    return corr
