# Evaluación Redes Neuronales MediaPipe

## Nombre: Luis Fernando Chávez Martínez

## Calificación: ______

---

### Modelar una red neuronal que pueda identificar emociones a través de los valores obtenidos de los landmarks que genera mediapipe

---

#### 1. Definir el tipo de red neuronal y describir cada una de sus partes

Para la red neuronal se utilizara una combinación de distintas estrategias para llevar a cabo la detección de emociones donde entraran: Red Neuronal Convolucional (CNN), LSTM (Long Short-Term Memory) y Softmax.

- **Capa de Entrada:** los 468 puntos de landmarks × 2 valores [0,1] = 936, lo que nos deja con 936 neuronas de entrada.
- **Capas Ocultas:** Las necesarias para que las LSTM puedan aprender y retener esa información.
- **Capa de Salida:** Función softmax con 6 neuronas (Pueden ser más pero con 6 buscaremos las emociones básicas).

#### 2. Definir los patrones a utilizar

Patrones clave que nos sirven para identificar las emociones:

- Distancia entre labios (felicidad o enojo).
- Altura de las cejas (miedo o tristeza).
- Apertura de los ojos (sorpresa).
- Arrugas frontales (enojo o sorpresa).
- Distancia entre labio superior e inferior (detectar boca abierta = sorpresa).
- Sin expresión (neutral).

#### 3. Definir la función de activación es necesaria para este problema

**Capas Ocultas:** ReLU (Rectified Linear Unit) por su eficiencia computacional.

**Capa de Salida:** Softmax (para clasificación multi-clase)

#### 4. Definir el número máximo de entradas

- **Máximo:** 468 landmarks × 2 valores [0,1] = 936 entradas, llevado el caso a lo extremo donde se toma el 100% de los puntos dados por landmarks.

#### 5. ¿Qué valores a la salida de la red se podrían esperar?

Un vector de probabilidades con 6 valores (en este caso por las 6 emociones básicas):

- **Felicidad** [0.85, 0.02, 0.01, 0.1, 0.02, 0.0]
- **Tristeza** [0.02, 0.85, 0.01, 0.1, 0.02, 0.0]
- **Sorpresa** [0.02, 0.01, 0.85, 0.1, 0.02, 0.0]
- **Enojo** [0.02, 0.01, 0.1, 0.85, 0.02, 0.0]
- **Miedo** [0.02, 0.01, 0.1, 0.02, 0.85, 0.0]
- **Neutral** [0.02, 0.01, 0.1, 0.02, 0.0, 0.85]

Los valores siempre estarán entre 0 y 1, lo que representa la probabilidad de cada emoción.

#### 6. ¿Cuáles son los valores máximos que puede tener el bias?

No existe, No se sabe, No se puede predecir, el bias siempre cambia dependiendo de la información que se le pase a la red.
