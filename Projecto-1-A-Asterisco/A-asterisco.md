# Explicación del Algoritmo A* en Pygame con Pyhton

## Introducción

Este código implementa el algoritmo A* utilizando la biblioteca Pygame para la visualización del proceso de búsqueda de camino en una cuadrícula. Se pueden definir nodos de inicio, fin y obstáculos en una interfaz gráfica.

## Dependencias

- `pygame`
- `heapq` (para manejar la cola de prioridad del algoritmo A*)

## Configuración Base de Pygame

Configuracion dada por el profesor [Eduardo Alcaraz (Lolero de corazón)](https://ealcaraz85.github.io/IA.io/#orgbe4d9ff)

### Sección 1: Inicio

Inicialización del entorno Pygame mas la configuracion del tamaño de la ventana.

```python
pygame.init()
ANCHO_VENTANA = 720
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Algoritmo A*")
```

Se define la ventana de la aplicación con un tamaño de 720x720 píxeles para ser compatible con la mayoria de dispositivos.

### Sección 2: Definición de colores

```python
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)
AZUL = (135, 206, 235)
```

Estos colores representan los diferentes tipos de nodos en la cuadrícula que se utilizaran a lo largo del programa, adicionalmente se agrego el color **AZUL** (en realidad es Azul celeste.) para colorear los recorridos que hizo el calculo a lo largo de la ejecución.

### Sección 3: Fuentes de las letras y tamaño

```python
pygame.font.init()
FUENTE = pygame.font.Font(None, 20)
```

En este caso no se utilizara una fuente pero el tamaño de los números y letras se colocara en 20.

### Sección 4: Definición de la Clase `Nodo`

Esta clase representa un nodo en la cuadrícula definiremos los puntos mas importantes antes de ver el código:

#### Significado de las variables

- `g`: Costo desde el nodo inicial.
- `h`: Heurística basada en la distancia Manhattan.
- `f`: Suma de `g` y `h`.
- `vecinos`: Lista de nodos adyacentes accesibles.

#### Métodos importantes

- `__lt__()`: Ordenar nodos en la cola de prioridad
- `get_pos()`: Obtener la posición del nodo actual.
- `es_pared()`: Verificar si el nodo es un obstáculo.
- `hacer_pared()`: Convierte el nodo en un obstáculo.
- `hacer_inicio()`: Marca el nodo como inicio.
- `hacer_fin()`: Marca el nodo como destino.
- `dibujar(ventana)`: Dibuja el nodo en la interfaz gráfica, mostrando los valores `G`, `H` y `F`.

### Sección 5: Creación y dibujo de la cuadrícula

```python
def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid
```

Se genera una cuadrícula de nodos con el tamaño especificado aclarando que siempre sera entero el numero de filas.

```python
def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))
```

Se dibuja la cuadrícula en la ventana usando líneas grises para separar los nodos y tener mejor visualización de la representación de la cuadrícula.

## Implementación del Algoritmo A*

Teniendo la cuadrícula y los nodos definidos, procedemos a implementar el algoritmo A* para encontrar el camino más corto desde el nodo inicial al nodo final a continuación se muestra el código de la implementación del algoritmo A y la heurística utilizada.

### Distancia Manhattan

```python
def distancia(nodo1, nodo2):
    return (abs(nodo1.fila - nodo2.fila) + abs(nodo1.col - nodo2.col)) * 10
```

Esta función calcula la heurística para el algoritmo A*, permitiendo solo movimientos en horizontal y vertical ademas de multiplicar por 10 para que sea compatible con la distancia real en la cuadrícula ya defina anteriormente en clases **(Coste de movimiento = 10)**.

### Algoritmo A*

Código completo del algoritmo A* implementado en Python utilizando la biblioteca `heapq` para manejar la cola de prioridad.

```python
def algoritmo_a_estrella(grid, inicio, fin):
    open_set = []
    heapq.heappush(open_set, (0, inicio))
    came_from = {}
    inicio.g = 0
    inicio.h = distancia(inicio, fin)
    inicio.f = inicio.g + inicio.h

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == fin:
            reconstruir_camino(came_from, fin, fin)
            return True

        for vecino in obtener_vecinos(current, grid):
            dx = abs(vecino.fila - current.fila)
            dy = abs(vecino.col - current.col)
            coste_movimiento = 14 if dx == 1 and dy == 1 else 10
            tentative_g = current.g + coste_movimiento

            if tentative_g < vecino.g:
                came_from[vecino] = current
                vecino.g = tentative_g
                vecino.h = distancia(vecino, fin)
                vecino.f = vecino.g + vecino.h
                heapq.heappush(open_set, (vecino.f, vecino))

                if vecino != fin and vecino != inicio:
                    vecino.color = AZUL

        dibujar(VENTANA, grid, len(grid), ANCHO_VENTANA)

    return False
```

## Explicación detallada del código por apartados

###

#### **1. Inicialización**

```python
def algoritmo_a_estrella(grid, inicio, fin):
    open_set = []
    heapq.heappush(open_set, (0, inicio))
    came_from = {}
    inicio.g = 0
    inicio.h = distancia(inicio, fin)
    inicio.f = inicio.g + inicio.h
```

- Se define una **lista de prioridad** (`open_set`), implementada como una cola de prioridad usando la librería de Python `heapq`.
- Se inserta el nodo `inicio` con prioridad `0`.
- Se inicializa el diccionario `came_from` para rastrear el camino.
- Se asignan los valores de costo:
  - `g` → Costo desde el inicio.
  - `h` → Heurística (estimación de distancia al objetivo ignorando obstáculos).
  - `f = g + h` → Función de costo total.

#### **2. Bucle principal**

```python
while open_set:
    current = heapq.heappop(open_set)[1]
```

- Mientras la **lista de prioridad** no esté vacía, se extrae el nodo con menor costo `f`.

#### **3. Verificación del objetivo**

```python
if current == fin:
    reconstruir_camino(came_from, fin, fin)
    return True
```

- Si el nodo actual es el **nodo objetivo**, se reconstruye el camino y el algoritmo finaliza exitosamente.

#### **4. Búsqueda de nodos vecinos**

```python
for vecino in obtener_vecinos(current, grid):
    dx = abs(vecino.fila - current.fila)
    dy = abs(vecino.col - current.col)
    coste_movimiento = 14 if dx == 1 and dy == 1 else 10
    tentative_g = current.g + coste_movimiento
```

- Se obtienen los **vecinos** del nodo actual.
- Se calcula el **costo de movimiento**:
  - **10** si es movimiento horizontal o vertical.
  - **14** si es diagonal (Redondeado a 14 para simplificar como lo acordado en clase).

#### **5. Evaluación del Mejor Camino**

```python
if tentative_g < vecino.g:
    came_from[vecino] = current
    vecino.g = tentative_g
    vecino.h = distancia(vecino, fin)
    vecino.f = vecino.g + vecino.h
    heapq.heappush(open_set, (vecino.f, vecino))
```

- Si `tentative_g` es mejor que `vecino.g`, se actualizan:
  - `came_from`: Guarda el mejor camino.
  - `g`: Nuevo costo desde el inicio.
  - `h`: Estimación de distancia al objetivo.
  - `f`: Suma de costos.
- Se inserta el **vecino** en la cola de prioridad para su evaluación.

#### **6. Visualización del Proceso**

```python
if vecino != fin and vecino != inicio:
    vecino.color = AZUL
```

- Se actualiza el nodo vecino a color azul para visualizar el proceso de búsqueda y a zu vez confirmar que no se esta haciendo una búsqueda a lo bruto recorriendo toda la cuadrícula.

#### **7. Dibujado en la Ventana**

```python
dibujar(VENTANA, grid, len(grid), ANCHO_VENTANA)
```

- Se actualiza la cuadrícula mostrando el progreso de la búsqueda con sus respectivos colores.

#### **8. Condición de No Solución**

```python
return False
```

- Si la cola de prioridad (`open_set`) queda vacía sin encontrar `fin`, el algoritmo devuelve `False`, indicando que **no hay camino posible** para evitar una búsqueda sin fin.

## Funciones Adicionales: Obtención de vecinos

```python
def obtener_vecinos(nodo, grid):
    vecinos = []
    filas = len(grid)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            x, y = nodo.fila + dx, nodo.col + dy
            if 0 <= x < filas and 0 <= y < filas and not grid[x][y].es_pared():
                vecinos.append(grid[x][y])
    return vecinos
```

Esta función se encarga de obtener los nodos adyacentes a un nodo dado en la cuadrícula.

### Explicación de la Función `obtener_vecinos`

- La función **`obtener_vecinos`** obtiene los nodos adyacentes al `nodo` en casilla actual.
- Con ayuda de ciclos `for` anidados, se iteran todas las combinaciones de desplazamiento (`dx`, `dy`) en un rango de `-1 a 1`, excluyendo `0, 0` ya que es el nodo actual.
- Se calcula la nueva posición `(x, y)` y se verifica lo siguiente:
  - Que esté dentro de los límites de la cuadrícula.
  - Que no sea una celda marcada como pared (`es_pared()`).
- Si los nodos vecinos son válidos se agregan a la lista y se termina la función  `obtener_vecinos` regresando la lista actualizada.

### Funciones Adicionales: Reconstrucción del camino

```python
def reconstruir_camino(came_from, current, fin):
    while current in came_from:
        current = came_from[current]
        if current != fin:
            current.color = VERDE
```

### **Explicación**

- **`reconstruir_camino`** se encarga de trazar el camino encontrado desde `fin` hasta `inicio`.
- Utiliza el diccionario `came_from` para seguir la ruta óptima.
- **Colorea en verde** (`VERDE`) los nodos del camino excepto el nodo final.

## Lógica principal `main` (Código completo)

```python
def main(ventana, ancho):
    FILAS = 11
    grid = crear_grid(FILAS, ancho)
    inicio = None
    fin = None
    corriendo = True
    boton_presionado = False

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio:
                    inicio = nodo
                    inicio.hacer_inicio()
                elif not fin:
                    fin = nodo
                    fin.hacer_fin()
                else:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.color = BLANCO
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin and not boton_presionado:
                    boton_presionado = True
                    algoritmo_a_estrella(grid, inicio, fin)

    pygame.quit()
```

### **Explicación de la lógica principal**

- Se define el número de filas de la cuadrícula.
- Se inicializa la cuadrícula (`grid`) con los valores de las filas y el ancho de la ventana.
- Se establecen los puntos de inicio y fin en `None`.
- Se inicia el bucle principal para gestionar los eventos del usuario donde:
  - **Click Izquierdo**:
    - Se obtiene la posición del mouse.
    - Se asigna el nodo como inicio, fin o pared en base a primer nodo inicio, segundo nodo fin y luego paredes.
  - **Click Derecho**:
    - Borra el nodo seleccionado.
  - **Tecla Espacio**:
    - Inicia el algoritmo A* si hay un inicio y un fin definidos.

## **Conclusión**

Este código implementa el algoritmo **A***, para encontrar el camino más corto entre dos puntos en una cuadrícula, se puede interactuar con la interfaz gráfica para definir el inicio, el fin y los obstáculos. La lógica del algoritmo A* se implementa utilizando:

- **Cola de prioridad** (Librería `heapq`) para seleccionar nodos con menor coste `f`.
- **Función heurística** (`h`) basada en la distancia estimada al objetivo.
- **Estructura de costos** (`g`, `h`, `f`) para determinar la mejor ruta base 10 en vertical y horizontal con un coste 14 en diagonal.
- **Dibujado dinámico** para la representación gráfica del proceso de búsqueda y validacion de la busqueda del mejor camino sin tener que calcular toda la cuadrícula.
- **Interfaz con Pygame** (Librería `pygame`) Usara para interactuar con la cuadrícula para selección manual de puntos y obstáculos.
