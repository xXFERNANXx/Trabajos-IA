# Documentación - Mona China Tetona Haciendo de Mario Bros

## Variables Globales

### Variables de Pantalla y Configuración

- `w, h = 1400, 720`: Dimensiones de la ventana del juego
- `pantalla`: Superficie principal de Pygame
- `BLANCO = (255, 255, 255)`, `NEGRO = (0, 0, 0)`: Colores utilizados en el juego

### Variables de Entidades del Juego

- `jugador`: Rectángulo que representa al jugador
- `bala`: Rectángulo que representa la bala horizontal
- `bala2`: Rectángulo que representa la bala vertical
- `nave`: Rectángulo que representa la nave horizontal
- `nave2`: Rectángulo que representa la nave vertical
- `fondo`: Variable para el fondo animado
- `menu`: Variable para el menú

### Variables de Posición y Movimiento

- `posicion_original_x = 90`: Posición X inicial del jugador
- `posicion_original_y = h - 100`: Posición Y inicial del jugador
- `velocidad_bala = -18`: Velocidad de la bala horizontal
- `velocidad_bala2 = 5`: Velocidad de la bala vertical
- `velocidad_dezplazamiento = 6`: Velocidad de desplazamiento lateral
- `desplazamiento = 46`: Distancia máxima de desplazamiento lateral

### Variables de Salto y Física

- `salto = False`: Indica si el jugador está saltando
- `en_suelo = True`: Indica si el jugador está en el suelo
- `salto_altura = 15`: Velocidad inicial del salto
- `gravedad = 3`: Fuerza de gravedad aplicada al salto

### Variables de Estados de Movimiento

- `izquierda = False`: Indica movimiento hacia la izquierda
- `ida = False`: Indica la fase de ida del movimiento lateral
- `vuelta = False`: Indica la fase de vuelta del movimiento lateral
- `sin_movimiento = True`: Indica si no hay movimiento lateral
- `bala_disparada = False`: Estado de disparo de la bala horizontal
- `bala2_disparada = False`: Estado de disparo de la bala vertical

### Variables de Control del Juego

- `pausa = False`: Estado de pausa del juego
- `menu_activo = True`: Estado del menú principal
- `modo_auto = False`: Indica si el juego está en modo automático
- `modelo = 0`: Identificador del modelo de IA seleccionado

### Variables de Animación

- `current_frame = 0`: Frame actual de la animación del jugador
- `frame_speed = 3`: Velocidad de animación del jugador
- `frame_count = 0`: Contador de frames del jugador
- `current_frame_nave = 0`: Frame actual de la animación de la nave
- `frame_speed_nave = 0.5`: Velocidad de animación de la nave
- `frame_count_nave = 0`: Contador de frames de la nave
- `current_frame_fondo = 0`: Frame actual de la animación del fondo
- `frame_speed_fondo = 0.5`: Velocidad de animación del fondo
- `frame_count_fondo = 0`: Contador de frames del fondo

### Variables de Machine Learning

- `datos_modelo = []`: Lista para almacenar datos de entrenamiento
- `nnNetwork = None`: Modelo de red neuronal
- `decisionTree = None`: Modelo de árbol de decisiones
- `regresionLineal = None`: Modelo de regresión lineal
- `knnModel = None`: Modelo K-Nearest Neighbors (declarado implícitamente)

### Variables de UI

- `fuente`: Fuente de texto para el menú
- `titulo`: Fuente de texto para títulos

---

## Funciones de Manejo de Proyectiles

### `disparar_bala()`

Activa el disparo de la bala horizontal si no está ya disparada. Establece una velocidad aleatoria entre -20 y -18 para crear variabilidad en el juego.

### `disparar_bala2()`

Activa el disparo de la bala vertical (bala2) si no está ya disparada.

### `reset_bala()`

Reinicia la posición de la bala horizontal a su posición inicial en el lado derecho de la pantalla y desactiva el estado de disparo.

### `reset_bala2()`

Reinicia la posición de la bala vertical a su posición inicial en la parte superior y desactiva el estado de disparo.

---

## Funciones de Movimiento del Jugador

### `manejar_salto()`

Controla la física del salto del jugador:

- Aplica movimiento vertical hacia arriba
- Reduce gradualmente la velocidad del salto aplicando gravedad
- Detecta cuando el jugador toca el suelo para terminar el salto
- Restablece las variables de salto para permitir un nuevo salto

### `manejar_desplazamiento()`

Controla el movimiento lateral del jugador:

- Maneja la fase de "ida" (movimiento hacia la izquierda)
- Maneja la fase de "vuelta" (regreso a la posición original)
- Controla la velocidad y distancia del desplazamiento
- Restablece el estado a "sin_movimiento" al completar el ciclo

---

## Funciones de Control del Juego

### `pausa_juego()`

Alterna entre los estados de pausa y reproducción del juego:

- Pausa/reanuda la música de fondo
- Cambia el estado global de pausa
- Imprime mensajes informativos en la consola

### `mostrar_menu()`

Presenta el menú principal del juego con las siguientes opciones:

- **M**: Modo Manual - El jugador controla directamente
- **A**: Modo Automático - La IA toma decisiones
- **G**: Mostrar gráfica del dataset de entrenamiento
- **Q**: Salir del juego

Maneja la entrada del usuario y configura las variables globales según la selección.

### `reiniciar_juego()`

Reinicia todas las variables del juego a su estado inicial después de una colisión:

- Reposiciona al jugador y proyectiles
- Restablece estados de movimiento y disparo
- Reproduce el sonido de muerte
- Maneja el guardado de datos de entrenamiento si existen
- Retorna al menú principal

### `guardar_datos()`

Recopila y almacena datos para el entrenamiento de modelos de IA:

- **Entradas**: Distancia a bala horizontal, velocidad de bala, distancia a bala vertical
- **Salidas**: Estado de salto, estado de movimiento lateral
- Aplica filtros para reducir ruido en los datos
- Almacena los datos en la lista `datos_modelo`

---

## Funciones de Selección de Modelos

### `seleccionar_modelo()`

Presenta una interfaz para seleccionar entre 4 modelos de IA:

1. **Red Neuronal**: Modelo de aprendizaje profundo
2. **Árbol de Decisiones**: Modelo basado en reglas
3. **Regresión Lineal**: Modelo estadístico lineal
4. **K Nearest Neighbor**: Modelo basado en proximidad

Inicializa el modelo seleccionado y configura las variables correspondientes.

### `preguntar_sobrescribir_modelo()`

Presenta una opción para entrenar nuevos modelos cuando hay datos disponibles:

- Permite sobrescribir modelos existentes
- Guarda los datos en formato CSV
- Entrena todos los modelos disponibles
- Limpia archivos anteriores de modelos e imágenes

### `graficar()`

Ejecuta un script externo para visualizar el dataset de entrenamiento:

- Verifica la existencia del archivo de datos
- Ejecuta `grafica.py` con los parámetros apropiados
- Muestra características y objetivos del dataset

---

## Funciones de Utilidad

### `asegurar_directorios()`

Crea la estructura de directorios necesaria para el almacenamiento de modelos:

- `./Models/`: Directorio principal de modelos
- `./Models/Data/`: Datos de entrenamiento
- `./Models/PDF/`: Archivos de visualización

---

## Modelos de Machine Learning

### `enRedNeural()`

Implementa y entrena una red neuronal multicapa:

- **Arquitectura**: Una capa oculta con 10 neuronas
- **Activación**: ReLU
- **Salidas**: Clasificación binaria para salto e izquierda
- **Configuración**: Tasa de aprendizaje 0.01, máximo 40,000 iteraciones
- Carga modelo existente o entrena uno nuevo según disponibilidad

### `predecirConRedNeuronal(param_entrada)`

Realiza predicciones usando la red neuronal entrenada:

- Recibe parámetros de entrada (distancias y velocidades)
- Retorna decisiones booleanas para saltar y moverse
- Incluye manejo de errores y logging detallado

### `decision_tree()`

Implementa un árbol de decisiones para múltiples salidas:

- **Configuración**: Profundidad máxima de 10 niveles
- **Salidas**: Clasificación simultánea para ambas acciones
- Guarda el modelo entrenado en formato joblib

### `predecirConArbolDecisiones(param_entrada)`

Realiza predicciones usando el árbol de decisiones:

- Procesa entrada y retorna decisiones binarias
- Manejo robusto de errores
- Logging de predicciones para debugging

### `regrecionLineal()`

Implementa regresión lineal con múltiples salidas:

- **Pipeline**: Normalización + Regresión lineal
- **Multisalida**: Predice ambas acciones simultáneamente
- Utiliza `StandardScaler` para normalización de características

### `predecirConRegresionLineal(param_entrada)`

Realiza predicciones usando regresión lineal:

- Convierte salidas continuas a decisiones binarias
- **Umbrales**: 0.55 para salto, 0.50 para movimiento lateral
- Manejo de errores y logging detallado

### `kNearestNeighbor()`

Implementa K-Nearest Neighbors con múltiples salidas:

- **Configuración**: 5 vecinos, pesos por distancia
- **Pipeline**: Normalización + KNN multiclase
- Algoritmo automático para optimización

### `predecirConKNN(param_entrada)`

Realiza predicciones usando KNN:

- Procesa entrada limitando a 3 características
- Retorna decisiones binarias basadas en vecinos más cercanos
- Logging completo para análisis

---

## Función de Actualización Principal

### `update()`

Función central que actualiza todos los elementos visuales del juego:

#### Renderizado de Fondo

- Actualiza animación del fondo con 39 frames
- Controla velocidad de animación del fondo

#### Animación de Personajes

- Actualiza frames del jugador (7 frames disponibles)
- Controla animación de las naves (17 frames)
- Maneja contadores y velocidades de animación

#### Movimiento de Proyectiles

- Actualiza posición de balas según sus velocidades
- Maneja reinicio automático cuando salen de pantalla
- Sincroniza disparo automático de proyectiles

#### Renderizado de Elementos

- Dibuja jugador con sprite animado
- Renderiza proyectiles con sus respectivas imágenes
- Dibuja naves con animaciones
- Muestra hitboxes para debugging (rectángulos verdes y rojos)

#### Detección de Colisiones

- Verifica colisión jugador-bala horizontal
- Verifica colisión jugador-bala vertical
- Activa secuencia de muerte y reinicio en caso de colisión

---

## Función Principal

### `main()`

Bucle principal del juego que coordina todos los sistemas:

#### Inicialización

- Configura reloj del juego (30 FPS)
- Inicia música de fondo en bucle
- Muestra menú inicial

#### Manejo de Eventos

- **QUIT**: Cierra el juego
- **SPACE**: Activa salto (solo en modo manual y si está en suelo)
- **LEFT**: Activa movimiento lateral (solo en modo manual)
- **P**: Pausa/reanuda el juego
- **Q**: Salida rápida del juego

#### Lógica de Modo Manual

- El jugador controla directamente las acciones
- Se ejecutan funciones de salto y desplazamiento según input
- Se guardan datos de entrenamiento continuamente

#### Lógica de Modo Automático

Según el modelo seleccionado (1-4):

- **Modelo 1**: Red Neuronal - Predicción basada en capas neuronales
- **Modelo 2**: Árbol de Decisiones - Decisiones basadas en reglas
- **Modelo 3**: Regresión Lineal - Predicción estadística continua
- **Modelo 4**: KNN - Decisiones basadas en vecinos similares

#### Actualizaciones Continuas

- Disparo automático de proyectiles
- Actualización de elementos visuales
- Renderizado a 30 FPS constantes

#### Sistema de Entrada para IA

Todos los modelos reciben como entrada:

- Distancia horizontal a la bala principal
- Velocidad de la bala horizontal  
- Distancia vertical a la bala secundaria

#### Sistema de Salida de IA

Todos los modelos retornan dos decisiones booleanas:

- ¿Debe saltar? (evitar bala horizontal)
- ¿Debe moverse lateralmente? (evitar bala vertical)

La función principal integra todos estos sistemas para crear una experiencia de juego fluida donde el jugador puede alternar entre control manual y observar cómo diferentes algoritmos de IA aprenden a jugar.
