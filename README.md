# 📊 EDA Completo - Análisis Exploratorio de Datos

Código mejorado para realizar un **Análisis Exploratorio de Datos completo** que cumple con todos los requisitos del **Ejercicio 3**.

---

## 🎯 Ejercicio 3 - Requisitos Completos

### ✅ 3.1 Análisis Univariante

**Para variables explicativas:**
- ✅ Describe su naturaleza (continua, discreta, categórica)
- ✅ Analiza distribuciones
- ✅ Analiza escalas
- ✅ Analiza valores extremos (outliers)

**Para variable objetivo:**
- ✅ Analiza el balanceo de clases
- ✅ Discute posibles consecuencias del desbalance

### ✅ 3.2 Análisis Bivariante

**Explora la relación entre:**
- ✅ Cada variable explicativa y la variable objetivo
- ✅ Variables explicativas entre sí (multicolinealidad)

**Se apoya en:**
- ✅ Gráficos
- ✅ Tablas
- ✅ Estadísticos descriptivos

---

## 📁 Estructura del Proyecto

```
proyecto_eda/
│
├── DataLoader/
│   └── load_data.py          ← Carga de datos + análisis estadístico
│
├── Graphics/
│   └── eda_graphs.py         ← Todas las visualizaciones
│
├── data/
│   └── newdata.csv           ← Tu dataset
│
├── output/                   ← Resultados (se crea automáticamente)
│   ├── *.csv                 ← Tablas de análisis
│   ├── *.png                 ← Gráficos
│   └── Class_X/              ← Gráficos por clase
│
└── main.py                   ← Script principal
```

---

## 🚀 Cómo Usar

### 1. Asegúrate de tener tu dataset

Coloca tu archivo CSV en `data/newdata.csv`

### 2. Ejecuta el análisis completo

```bash
python main.py
```

### 3. Revisa los resultados

Todos los archivos se guardan en la carpeta `output/`

---

## 📊 Lo que Genera el Código

### 📄 Tablas CSV (análisis estadístico)

1. **variable_nature.csv**
   - Tipo de cada variable (numérica/categórica)
   - Naturaleza (continua/discreta/nominal)
   - Valores únicos y rangos

2. **descriptive_statistics.csv**
   - Media, mediana, desviación estándar
   - Mínimo, Q1, Q3, máximo
   - Asimetría (skewness) y curtosis

3. **outliers_summary.csv**
   - Número y porcentaje de outliers por variable
   - Identificados con método IQR

4. **class_balance.csv**
   - Distribución de la variable objetivo
   - Frecuencias y porcentajes por clase
   - Ratio de balance
   - Recomendaciones para el modelo

5. **correlation_matrix.csv**
   - Matriz de correlación completa
   - Para detectar multicolinealidad

6. **high_correlations.csv**
   - Pares de variables con |r| > 0.7
   - Solo se genera si hay multicolinealidad

7. **variable_target_tests.csv**
   - Tests estadísticos (t-test, Mann-Whitney)
   - p-values y significancia
   - Diferencia de medias entre clases

8. **categorical_tests.csv** (si hay variables categóricas)
   - Tests chi-cuadrado
   - Relación con variable objetivo

### 📊 Gráficos PNG (visualizaciones)

#### Gráficos Generales:

1. **target_distribution.png**
   - Distribución de la variable objetivo
   - Barras + gráfico de pastel

2. **distributions_comparison.png**
   - Histogramas superpuestos por clase
   - Para todas las variables numéricas

3. **boxplots_comparison.png**
   - Boxplots comparativos por clase
   - Muestra diferencias entre grupos

4. **outliers_summary.png**
   - Gráfico de barras con % de outliers
   - Código de colores por severidad

5. **correlation_matrix.png**
   - Heatmap de correlación básico

6. **correlation_matrix_annotated.png**
   - Heatmap con recuadros negros en correlaciones altas

7. **variable_importance.png**
   - Importancia de variables según p-value
   - Muestra qué variables son significativas

#### Gráficos por Clase:

Dentro de `Class_0/` y `Class_1/`:

- **boxplot_[variable].png** - Boxplot de cada variable
- **hist_[variable].png** - Histograma con curva KDE
- **cat_[variable].png** - Gráficos de barras (categóricas)

---

## 🔍 Funciones Nuevas Añadidas

### En `load_data.py`:

```python
describe_variable_nature()       # Clasifica variables (continua/discreta/categórica)
univariate_statistics()          # Estadísticas descriptivas completas
detect_outliers()                # Detecta outliers con método IQR
analyze_class_balance()          # Analiza balanceo y da recomendaciones
correlation_analysis()           # Detecta multicolinealidad
variable_target_tests()          # Tests estadísticos vs target
categorical_target_analysis()    # Chi-cuadrado para categóricas
```

### En `eda_graphs.py`:

```python
plot_distributions_comparison()  # Histogramas superpuestos por clase
plot_boxplots_comparison()       # Boxplots comparativos
plot_target_distribution()       # Distribución del target
plot_outliers_summary()          # Resumen visual de outliers
plot_correlation_heatmap_annotated()  # Heatmap mejorado
plot_variable_importance_by_pvalue()  # Importancia de variables
save_all_summary_graphs()        # Genera todos los gráficos de resumen
```

---

## 📝 Para tu Informe

### Sección 3.1: Análisis Univariante

Puedes incluir:

1. **Tabla 1:** `variable_nature.csv`
   - "Naturaleza de las variables explicativas"

2. **Tabla 2:** `descriptive_statistics.csv`
   - "Estadísticas descriptivas"

3. **Figura 1:** `distributions_comparison.png`
   - "Distribuciones de variables numéricas por clase"

4. **Tabla 3:** `outliers_summary.csv`
   - "Resumen de valores extremos"

5. **Figura 2:** `target_distribution.png`
   - "Distribución de la variable objetivo"

6. **Tabla 4:** `class_balance.csv`
   - "Análisis de balanceo de clases"

**Interpretación:**
- Comenta la naturaleza de cada variable
- Interpreta la asimetría de las distribuciones
- Discute qué hacer con los outliers
- Explica las consecuencias del desbalance

### Sección 3.2: Análisis Bivariante

Puedes incluir:

1. **Figura 3:** `correlation_matrix_annotated.png`
   - "Matriz de correlación entre variables"

2. **Tabla 5:** `high_correlations.csv` (si existe)
   - "Pares de variables con alta correlación"

3. **Tabla 6:** `variable_target_tests.csv`
   - "Tests estadísticos: Variables vs Target"

4. **Figura 4:** `variable_importance.png`
   - "Importancia de variables para predecir el target"

5. **Figura 5:** `boxplots_comparison.png`
   - "Comparación de variables por clase"

**Interpretación:**
- Identifica pares de variables correlacionadas (multicolinealidad)
- Explica qué variables son significativas
- Interpreta las diferencias entre clases
- Propón qué variables eliminar o combinar

---

## 💡 Interpretación de Resultados

### Asimetría (Skewness):

- **|skew| < 0.5**: Distribución simétrica
- **skew > 0**: Sesgo positivo (cola derecha)
- **skew < 0**: Sesgo negativo (cola izquierda)
- **|skew| > 1**: Considerar transformación logarítmica

### Outliers:

- **< 5%**: Aceptable
- **5-10%**: Revisar, posiblemente conservar
- **> 10%**: Considerar transformación o eliminación

### Balance de Clases:

- **Ratio ≥ 0.8**: Balanceado ✓
- **0.5 ≤ Ratio < 0.8**: Ligero desbalance ⚠️
- **Ratio < 0.5**: Desbalance severo ❌

### Correlación:

- **|r| < 0.3**: Correlación débil
- **0.3 ≤ |r| < 0.7**: Correlación moderada
- **|r| ≥ 0.7**: Correlación alta → Multicolinealidad ⚠️

### p-value:

- **p < 0.01**: Muy significativa ✓✓
- **p < 0.05**: Significativa ✓
- **p ≥ 0.05**: No significativa ✗

---

## 🎯 Decisiones Basadas en el EDA

### Si hay multicolinealidad (|r| > 0.7):

**Opciones:**
1. Eliminar una de las variables correlacionadas
2. Combinarlas en una sola (ej: índice compuesto)
3. Usar regularización (Ridge, Lasso)
4. Aplicar PCA

### Si hay desbalance de clases:

**Opciones:**
1. **Ratio > 0.5**: Usar `class_weight='balanced'` en el modelo
2. **Ratio < 0.5**: Aplicar SMOTE o undersampling
3. Usar F1-score en vez de accuracy

### Si hay outliers:

**Decisión:**
- **< 5%**: Conservar (información valiosa)
- **5-10%**: Decidir caso por caso
- **> 10%**: Considerar:
  - Transformación logarítmica
  - Winsorización (recortar extremos)
  - Eliminar si son errores de datos

### Si hay variables no significativas (p > 0.05):

**Opciones:**
1. Eliminarlas del modelo
2. Combinarlas con otras variables
3. Crear variables derivadas

---

## 🐛 Solución de Problemas

### Error: "No such file or directory: 'data/newdata.csv'"

**Solución:**
```python
# En main.py, cambia la ruta:
file_path = 'ruta/completa/a/tu/archivo.csv'
```

### Error: "KeyError: 'deficit_calorico'"

**Solución:**
```python
# Verifica que tu CSV tenga la columna 'deficit_calorico'
# O cambia el nombre en main.py:
target = 'nombre_de_tu_columna_objetivo'
```

### No se generan gráficos categóricos

**Normal si no hay variables categóricas:**
```python
# El código detecta automáticamente si hay variables categóricas
# Si no las hay, simplemente no genera esos gráficos
```

---

## 📚 Dependencias

```bash
pip install pandas numpy scipy matplotlib seaborn
```

---

## ✅ Checklist del EDA

Después de ejecutar, verifica que tengas:

**Análisis Univariante:**
- [ ] Tabla de naturaleza de variables
- [ ] Estadísticas descriptivas completas
- [ ] Detección de outliers
- [ ] Análisis de balanceo de clases
- [ ] Gráficos de distribuciones
- [ ] Boxplots por variable

**Análisis Bivariante:**
- [ ] Matriz de correlación
- [ ] Identificación de multicolinealidad
- [ ] Tests estadísticos vs target
- [ ] Gráficos comparativos por clase
- [ ] Gráfico de importancia de variables

**Documentación:**
- [ ] Todas las tablas en CSV
- [ ] Todos los gráficos en PNG
- [ ] Interpretación de resultados
- [ ] Decisiones documentadas

---

¡Todo listo para completar el Ejercicio 3 de tu memoria! 🎉
