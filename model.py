"""
model.py
Funciones para entrenar y evaluar el modelo
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (confusion_matrix, accuracy_score, precision_score,
                             recall_score, f1_score, roc_auc_score, roc_curve)
import config


def train_model(X_train, y_train):
    """Entrena el modelo de regresión logística"""
    print("\n🎯 Entrenando modelo...")
    
    model = LogisticRegression(
        max_iter=config.MAX_ITER,
        random_state=config.RANDOM_STATE,
        class_weight=config.CLASS_WEIGHT
    )
    
    model.fit(X_train, y_train)
    print("✓ Modelo entrenado")
    
    return model


def get_coefficients(model):
    """Obtiene los coeficientes del modelo ordenados por importancia"""
    coef_df = pd.DataFrame({
        'Variable': config.FEATURES,
        'Coeficiente': model.coef_[0],
        'Odds_Ratio': np.exp(model.coef_[0]),
        'Abs_Coef': np.abs(model.coef_[0])
    }).sort_values('Abs_Coef', ascending=False)
    
    return coef_df


def make_predictions(model, X_test, threshold=0.5):
    """Hace predicciones con un umbral específico"""
    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_proba >= threshold).astype(int)
    return y_proba, y_pred


def evaluate_model(y_test, y_pred, y_proba):
    """Evalúa el modelo y retorna todas las métricas"""
    metrics = {
        'cm': confusion_matrix(y_test, y_pred),
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred),
        'auc': roc_auc_score(y_test, y_proba)
    }
    
    return metrics


def print_evaluation(metrics):
    """Imprime las métricas de evaluación de forma legible"""
    cm = metrics['cm']
    
    print("\n" + "="*80)
    print("EVALUACIÓN DEL MODELO")
    print("="*80)
    
    print("\n📊 Matriz de Confusión:")
    print(f"                    Predicho: 0    Predicho: 1")
    print(f"Real: 0 (No salud)  {cm[0,0]:6d}         {cm[0,1]:6d}  (VN, FP)")
    print(f"Real: 1 (Saludable) {cm[1,0]:6d}         {cm[1,1]:6d}  (FN, VP)")
    
    print(f"\n📈 Métricas:")
    print(f"  • Accuracy:  {metrics['accuracy']:.4f}")
    print(f"  • Precision: {metrics['precision']:.4f}")
    print(f"  • Recall:    {metrics['recall']:.4f}")
    print(f"  • F1-Score:  {metrics['f1']:.4f}")
    print(f"  • AUC-ROC:   {metrics['auc']:.4f}")


def compare_thresholds(model, X_test, y_test):
    """Compara rendimiento con diferentes umbrales"""
    print("\n" + "="*80)
    print("COMPARACIÓN DE UMBRALES")
    print("="*80)
    
    results = []
    
    for threshold in [config.THRESHOLD_DEFAULT, config.THRESHOLD_ALT]:
        y_proba, y_pred = make_predictions(model, X_test, threshold)
        
        recall = recall_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        
        results.append({
            'Umbral': threshold,
            'Precision': precision,
            'Recall': recall
        })
        
        print(f"\nUmbral {threshold}:")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
    
    return pd.DataFrame(results)
