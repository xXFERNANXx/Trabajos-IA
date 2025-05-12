# Regresión Lineal

*Definición:*  
Es una técnica de análisis de datos que predice el valor de datos desconocidos mediante el uso de otro valor de datos relacionado y conocido.

Una técnica de regresión consiste en trazar un gráfico lineal entre dos variables de datos: la variable independiente se traza a lo largo del eje horizontal. Las variables independientes también se denominan variables explicativas o variables predictivas. La variable dependiente \( y \) se traza en el eje vertical. También puede hacer referencia a los valores \( y \) como variables de respuesta o variables pronosticadas.

\[ y = ax + b \]

- \( y \): Variable dependiente  
- \( a \): Pendiente  
- \( x \): Variable independiente  
- \( b \): Intercepto  

*Desviación o Error*

## Aplicación al Modelo Phaser

**¿Se puede aplicar regresión lineal al modelo phaser?**  

Depende de la naturaleza de los datos:

- ✅ **Sí es adecuado** si la relación entre variables es aproximadamente lineal y los residuos siguen una distribución normal
- ❌ **No es adecuado** si los datos muestran patrones complejos no lineales o interacciones entre variables

**Alternativas cuando no funciona:**

1. Transformaciones no lineales de variables
2. Modelos polinómicos
3. Otros algoritmos (redes neuronales, árboles)

---

# Árbol de Decisión

*Definición:*  
Es un algoritmo de aprendizaje supervisado no paramétrico, que se utiliza tanto para tareas de clasificación como de regresión. Tiene una estructura jerárquica de un árbol, que consta de un nodo raíz, ramas, nodos internos y nodos de hoja.

**Ventajas para modelo phaser:**

- Maneja relaciones no lineales
- Interpretable
- No requiere normalización de datos

**Limitaciones:**

- Propenso a overfitting
- Sensible a pequeñas variaciones en datos

### Tabla de Modos

| Enfernal | Mode    | Enfernal | Mode    |
|---|---|---|---|
| Leap Mode | Leap Mode | Leap Mode | Leap Mode |

---

# Redes Neuronales

*Definición:*  
Modelos computacionales inspirados en el cerebro humano, capaces de aprender patrones complejos mediante capas de neuronas artificiales.

**Aplicación al phaser:**

- ✅ Ideal para patrones complejos no lineales
- ✅ Puede capturar interacciones entre múltiples variables
- ❌ Requiere más datos y potencia computacional
- ❌ Menos interpretable ("caja negra")

**Arquitecturas recomendadas:**

- MLP (Multilayer Perceptron) para regresión
- Redes recurrentes si hay dependencia temporal

---

# Comparativa de Modelos para Phaser

| Modelo          | Ventajas                          | Desventajas                   |
|-----------------|-----------------------------------|-------------------------------|
| Regresión Lineal| Simple, interpretable            | Solo captura relaciones lineales |
| Árbol Decisión | Maneja no linealidades, robusto  | Propenso a overfitting        |
| Red Neuronal   | Máxima flexibilidad, precisión   | Complejidad, requiere muchos datos |

**Recomendación final:**  

1. Comenzar con regresión lineal como baseline
2. Si falla, probar árboles de decisión con regularización
3. Para máxima precisión (y con datos suficientes), usar redes neuronales
