import pygame
import heapq

# Configuración de Pygame
pygame.init()
ANCHO_VENTANA = 720
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Algoritmo A*")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)
AZUL = (135, 206, 235)

# Fuente para los números
pygame.font.init()
FUENTE = pygame.font.Font(None, 20)

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.g = float("inf")  # Coste desde el inicio
        self.h = float("inf")  # Heurística (distancia al final)
        self.f = float("inf")  # Coste total (g + h)
        self.vecinos = []

    def __lt__(self, other):
        return self.f < other.f  # Ordenar nodos en la cola de prioridad

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_fin(self):
        self.color = PURPURA

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

        # Dibujar valores de G, H y F en todos los nodos explorados
        if self.g < float("inf"):
            g_text = FUENTE.render(f"G: {int(self.g)}", True, NEGRO)
            h_text = FUENTE.render(f"H: {int(self.h)}", True, NEGRO)
            f_text = FUENTE.render(f"F: {int(self.f)}", True, NEGRO)

            ventana.blit(g_text, (self.x + 5, self.y + 5))
            ventana.blit(h_text, (self.x + 5, self.y + 25))
            ventana.blit(f_text, (self.x + 5, self.y + 45))

def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

# Distancia Manhattan (solo horizontal/vertical) multiplicada por 10
def distancia(nodo1, nodo2):
    return (abs(nodo1.fila - nodo2.fila) + abs(nodo1.col - nodo2.col)) * 10

# Reconstrucción del camino
def reconstruir_camino(came_from, current, fin):
    while current in came_from:
        current = came_from[current]
        if current != fin:  # No cambiar el color del nodo final
            current.color = VERDE  # Marcar camino encontrado

# Algoritmo A*
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
            reconstruir_camino(came_from, fin, fin)  # Pasar 'fin' como argumento
            return True

        for vecino in obtener_vecinos(current, grid):
            # Coste de movimiento: 14 para diagonales, 10 para horizontales/verticales
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

                # Marcar nodos explorados
                if vecino != fin and vecino != inicio:
                    vecino.color = AZUL

        dibujar(VENTANA, grid, len(grid), ANCHO_VENTANA)

    return False  # No se encontró camino

def obtener_vecinos(nodo, grid):
    vecinos = []
    filas = len(grid)

    # Movimientos en todas las direcciones (incluyendo diagonales)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue  # Saltar el nodo actual
            x, y = nodo.fila + dx, nodo.col + dy
            if 0 <= x < filas and 0 <= y < filas and not grid[x][y].es_pared():
                vecinos.append(grid[x][y])

    return vecinos

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

            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
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

            elif pygame.mouse.get_pressed()[2]:  # Click derecho (borrar)
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

main(VENTANA, ANCHO_VENTANA)