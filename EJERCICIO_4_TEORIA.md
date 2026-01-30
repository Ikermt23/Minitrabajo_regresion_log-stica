# EJERCICIO 4: LA REGRESIÓN LOGÍSTICA DESDE LA TEORÍA

## 4.1 La Función Logística

### ¿Qué hace la función logística?

La **función logística** (también llamada sigmoide) transforma cualquier valor real en una probabilidad entre 0 y 1.

**Fórmula matemática:**

```
σ(z) = 1 / (1 + e^(-z))
```

Donde:
- `z = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ` (combinación lineal de variables)
- `e` ≈ 2.718 (número de Euler)

### Interpretación conceptual:

La función logística actúa como un **traductor**:
- **Entrada:** Combinación lineal de variables (puede ser cualquier número: -∞ a +∞)
- **Salida:** Probabilidad (siempre entre 0 y 1)

**Comportamiento:**
- Si `z → +∞`, entonces `σ(z) → 1` (probabilidad cercana a 100%)
- Si `z → -∞`, entonces `σ(z) → 0` (probabilidad cercana a 0%)
- Si `z = 0`, entonces `σ(z) = 0.5` (probabilidad del 50%)

### ¿Por qué su salida está acotada entre 0 y 1?

Por la estructura matemática de la función:

1. El denominador siempre es `1 + e^(-z)`
2. Como `e^(-z)` es siempre **positivo** (la exponencial nunca es negativa)
3. El denominador es siempre **mayor que 1**
4. Por tanto: `0 < σ(z) < 1` siempre

**Ejemplo numérico:**
```
z = -5  →  σ(-5) = 1/(1 + e^5) = 1/148.4 ≈ 0.007  (0.7%)
z = 0   →  σ(0)  = 1/(1 + 1)   = 0.5              (50%)
z = 5   →  σ(5)  = 1/(1 + e^-5) = 1/1.007 ≈ 0.993 (99.3%)
```

---

## 4.2 Interpretación de los Coeficientes

### ¿Qué significa el signo de un coeficiente?

**Coeficiente positivo (β > 0):**
- Si la variable aumenta → la probabilidad de Y=1 **aumenta**
- Ejemplo: β_Ejercicio = +0.5 → Más ejercicio aumenta prob. vida saludable

**Coeficiente negativo (β < 0):**
- Si la variable aumenta → la probabilidad de Y=1 **disminuye**
- Ejemplo: β_Sedentarismo = -0.8 → Más sedentarismo reduce prob. vida saludable

### ¿Qué representa su magnitud?

La **magnitud** (valor absoluto) indica **qué tan fuerte** es el efecto:

- |β| pequeño (ej: 0.1) → efecto débil
- |β| grande (ej: 2.0) → efecto fuerte

**PERO:** La magnitud NO se interpreta directamente como "cambio en probabilidad" porque la relación es **no lineal**.

### ¿Por qué no se interpretan igual que en regresión lineal?

| Aspecto | Regresión Lineal | Regresión Logística |
|---------|------------------|---------------------|
| Relación | **Lineal**: Y = β₀ + β₁X | **No lineal**: P(Y=1) = σ(β₀ + β₁X) |
| Interpretación β | Cambio absoluto en Y | Cambio en **log-odds** |
| Ejemplo β=0.5 | "Y aumenta 0.5 unidades" | "Log-odds aumenta 0.5" |

En regresión lineal: β₁ = cambio directo en Y
En regresión logística: β₁ = cambio en el **logaritmo de las odds**

Por eso necesitamos el concepto de **Odds Ratio** para interpretar correctamente.

---

## 4.3 Odds y Odds Ratio

### ¿Qué son las Odds?

Las **odds** (momios) son otra forma de expresar probabilidad:

```
Odds = P(evento) / P(no evento) = P / (1-P)
```

**Ejemplo:**
- Si P(vida saludable) = 0.75 (75%)
- Odds = 0.75 / 0.25 = 3
- Interpretación: "Es **3 veces más probable** tener vida saludable que no tenerla"

**Relación con probabilidad:**
- P = 0.5 → Odds = 1 (evento y no evento igual de probables)
- P = 0.75 → Odds = 3 (evento 3 veces más probable)
- P = 0.9 → Odds = 9 (evento 9 veces más probable)

### ¿Qué es un Odds Ratio?

El **Odds Ratio (OR)** es el **cociente de dos odds**:

```
OR = Odds₁ / Odds₀
```

**En regresión logística:**

```
OR = e^β
```

Es decir, el **exponencial del coeficiente**.

### ¿Cómo se relacionan con los coeficientes del modelo?

La regresión logística modela el **logaritmo de las odds**:

```
log(Odds) = β₀ + β₁X₁ + β₂X₂ + ...
```

Por tanto:
```
Odds = e^(β₀ + β₁X₁ + β₂X₂ + ...)
```

Cuando una variable X₁ aumenta en 1 unidad:
```
OR = e^β₁
```

### Interpretación práctica de un Odds Ratio

**Ejemplo real del proyecto:**

Supongamos que en nuestro modelo:
- Variable: `Workout_Frequency` (días de ejercicio por semana)
- Coeficiente: β = 0.693
- Odds Ratio: OR = e^0.693 = 2.0

**Interpretación:**
> "Por cada día adicional de ejercicio por semana, las **odds** de tener un estilo de vida saludable se **multiplican por 2** (se duplican), manteniendo todas las demás variables constantes."

**O equivalentemente:**
> "Una persona que hace ejercicio 4 días/semana tiene el **doble de odds** de vida saludable comparado con alguien que hace ejercicio 3 días/semana (asumiendo todo lo demás igual)."

### Valores típicos de Odds Ratio:

| OR | Interpretación |
|----|----------------|
| OR = 1 | Sin efecto (la variable no afecta) |
| OR = 2 | Duplica las odds (efecto positivo) |
| OR = 0.5 | Reduce las odds a la mitad (efecto negativo) |
| OR = 3 | Triplica las odds (efecto positivo fuerte) |
| OR = 0.33 | Reduce las odds a un tercio (efecto negativo fuerte) |

---

## Resumen: Cadena de Interpretación

```
Coeficiente (β) 
    ↓
log(Odds) = β₀ + β₁X
    ↓
Odds = e^(β₀ + β₁X)
    ↓
OR = e^β₁  (cuando X aumenta en 1)
    ↓
Probabilidad P = Odds / (1 + Odds)
```

**Ejemplo completo:**
1. β_Ejercicio = 0.693
2. OR = e^0.693 = 2.0
3. Si antes: P = 0.5 (Odds = 1)
4. Después de +1 día ejercicio: Odds = 2 → P = 2/(1+2) = 0.67 (67%)

**Interpretación final:**
"Un día adicional de ejercicio aumenta la probabilidad de vida saludable de 50% a 67%"
