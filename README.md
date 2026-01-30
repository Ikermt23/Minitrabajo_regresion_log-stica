# 🚀 Proyecto Regresión Logística - Estructura Simple

Proyecto completo de regresión logística organizado por **lógica funcional**.

---

## 📁 Estructura del Proyecto

```
proyecto/
│
├── config.py                 # ⚙️ Configuración (rutas, parámetros)
├── data_processing.py        # 📥 Carga y preparación de datos
├── model.py                  # 🎯 Entrenamiento y evaluación
├── visualizations.py         # 📊 Gráficos
├── main.py                   # ▶️ Script principal
│
├── data/
│   └── newdata.csv          # 📄 Dataset
│
└── outputs/                 # 📁 Resultados (se crea automáticamente)
    ├── eda_analisis.png
    ├── resultados_completos.png
    ├── metricas_modelo.csv
    ├── coeficientes_modelo.csv
    └── comparacion_umbrales.csv
```

---

## ⚡ Uso Ultra-Simple

```bash
# 1. Asegúrate de tener tu dataset en data/newdata.csv
# 2. Ejecuta:
python main.py
```

**¡Eso es todo!** El script hace TODO automáticamente.

---

## 📚 Descripción de Archivos

### 1. `config.py`
Configuración centralizada:
- Ruta del dataset
- Variables a usar
- Parámetros del modelo
- Umbrales de decisión

### 2. `data_processing.py`
Funciones de datos:
- `load_data()` - Carga y limpia el CSV
- `prepare_data()` - Escala y divide train/test
- `get_eda_stats()` - Estadísticas para EDA

### 3. `model.py`
Funciones del modelo:
- `train_model()` - Entrena regresión logística
- `get_coefficients()` - Obtiene coeficientes ordenados
- `make_predictions()` - Predice con umbral personalizado
- `evaluate_model()` - Calcula todas las métricas
- `compare_thresholds()` - Compara umbrales 0.5 vs 0.4

### 4. `visualizations.py`
Funciones de gráficos:
- `plot_eda()` - Gráficos del análisis exploratorio
- `create_all_plots()` - 6 visualizaciones del modelo

### 5. `main.py`
Script principal que ejecuta todo en orden:
1. Carga y EDA
2. Preparación de datos
3. Entrenamiento
4. Evaluación
5. Visualizaciones
6. Conclusiones

---

## 📊 Lo que Genera

### Gráficos:

**eda_analisis.png** (2 gráficos):
1. Balance de clases
2. Top 10 correlaciones

**resultados_completos.png** (6 gráficos):
1. Distribución de probabilidades por clase
2. Curva ROC
3. Matriz de confusión
4. Top 10 variables influyentes
5. Trade-off precision vs recall
6. Resumen de métricas

### CSVs:

1. **metricas_modelo.csv** - Accuracy, Precision, Recall, F1, AUC
2. **coeficientes_modelo.csv** - Coeficientes, Odds Ratio, importancia
3. **comparacion_umbrales.csv** - Umbrales 0.5 vs 0.4

---

## 🔧 Personalización

### Cambiar variables del modelo:

Edita `config.py`:
```python
FEATURES = [
    'Age',
    'BMI',
    'Calories',
    # Añade o quita variables aquí
]
```

### Cambiar umbrales:

```python
THRESHOLD_DEFAULT = 0.5
THRESHOLD_ALT = 0.3  # Cambia a 0.3 si quieres
```

### Cambiar tamaño de test:

```python
TEST_SIZE = 0.3  # 30% test en vez de 20%
```

---

## 🎯 Flujo del Pipeline

```
main.py ejecuta:

1️⃣ data_processing.load_data()
    ↓
   [DataFrame limpio]
    ↓
2️⃣ data_processing.get_eda_stats()
    ↓
   [Estadísticas EDA]
    ↓
3️⃣ visualizations.plot_eda()
    ↓
   [eda_analisis.png]
    ↓
4️⃣ data_processing.prepare_data()
    ↓
   [X_train, X_test, y_train, y_test]
    ↓
5️⃣ model.train_model()
    ↓
   [Modelo entrenado]
    ↓
6️⃣ model.make_predictions()
    ↓
   [y_proba, y_pred]
    ↓
7️⃣ model.evaluate_model()
    ↓
   [Métricas]
    ↓
8️⃣ visualizations.create_all_plots()
    ↓
   [resultados_completos.png]
    ↓
9️⃣ Guardar CSVs
    ↓
   ✅ Proyecto completado
```

---

## 💡 Ventajas de Esta Estructura

### ✅ Simple
- Solo 5 archivos Python
- Cada archivo tiene propósito claro
- Fácil de entender y modificar

### ✅ Modular
- Funciones reutilizables
- Fácil de testear cada parte
- Puedes importar funciones en otros proyectos

### ✅ Limpio
- Separación clara: datos / modelo / visualización
- main.py es muy legible
- Sin código duplicado

### ✅ Profesional
- Configuración centralizada
- Código documentado
- Fácil de mantener

---

## 📝 Para tu Memoria

### Ejercicios 1-2:
Ya los tienes escritos ✓

### Ejercicio 3 (EDA):
```
Copia el output de: data_processing.get_eda_stats()
Incluye: eda_analisis.png
```

### Ejercicio 4 (Teoría):
Lee: **EJERCICIO_4_TEORIA.md** (lo tienes aparte)

### Ejercicio 5 (Preparación):
```
Copia el output de: data_processing.prepare_data()
Explica: StandardScaler, train/test split
```

### Ejercicio 6 (Entrenamiento):
```
Copia: coeficientes_modelo.csv
Interpreta los 3 coeficientes más importantes
```

### Ejercicio 7 (Umbrales):
```
Copia: comparacion_umbrales.csv
Justifica elección del umbral 0.4
```

### Ejercicio 8 (Evaluación):
```
Copia: metricas_modelo.csv
Incluye interpretación de matriz de confusión
```

### Ejercicio 9 (Visualización):
```
Incluye: resultados_completos.png
Explica cada uno de los 6 gráficos
```

### Ejercicio 10 (Conclusiones):
```
Copia el output final de main.py
Añade reflexión personal
```

---

## 🐛 Troubleshooting

### Error: "No such file: data/newdata.csv"
```python
# En config.py, cambia la ruta:
DATA_PATH = 'C:/ruta/completa/newdata.csv'
```

### Error: "is_healthy not found"
El código convierte automáticamente. Verifica que la columna exista.

### Quiero ver paso a paso
```python
# En vez de ejecutar main.py, puedes ejecutar cada parte:
from data_processing import load_data
df = load_data()

from data_processing import prepare_data
X_train, X_test, y_train, y_test, scaler = prepare_data(df)

# etc...
```

---

## 📦 Dependencias

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

---

## 🎓 Conceptos Cubiertos

✅ Carga y limpieza de datos  
✅ Análisis exploratorio (EDA)  
✅ Feature scaling (StandardScaler)  
✅ Train/test split estratificado  
✅ Regresión logística binaria  
✅ Interpretación de coeficientes  
✅ Odds Ratio  
✅ Umbrales de decisión  
✅ Matriz de confusión  
✅ Métricas: Accuracy, Precision, Recall, F1, AUC  
✅ Curva ROC  
✅ Trade-off precision/recall  
✅ Visualización de resultados  
✅ Conclusiones y pensamiento crítico  

---

## 📞 Estructura de Llamadas

```python
# main.py importa y usa:
from data_processing import load_data, prepare_data, get_eda_stats
from model import train_model, evaluate_model, ...
from visualizations import plot_eda, create_all_plots

# Flujo:
df = load_data()                    # data_processing
stats = get_eda_stats(df)           # data_processing
plot_eda(df, stats)                 # visualizations
X_train, X_test, ... = prepare_data(df)  # data_processing
model = train_model(X_train, y_train)    # model
metrics = evaluate_model(...)       # model
create_all_plots(...)              # visualizations
```

---

¡Todo listo para ejecutar! 🚀

```bash
python main.py
```

**Tiempo estimado de ejecución:** ~10-30 segundos
