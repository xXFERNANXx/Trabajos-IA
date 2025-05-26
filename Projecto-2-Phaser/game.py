import pygame
import random
import numpy as np
import os
# -------------------------------------------------------------------
# Uso de joblib para guardar y cargar los modelo
from joblib import dump, load
# Uso de pandas para manejar los datos
import pandas as pd
# Uso de subprocess para ejecutar comandos en la terminal
import subprocess
# -------------------------------------------------------------------
# Modelo 1: Red Neuronal
from sklearn.neural_network import MLPClassifier
# -------------------------------------------------------------------
# Modelo 2: Árbol de Decisiones
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import tree
import matplotlib.pyplot as plt
import graphviz
# -------------------------------------------------------------------
# Modelo 3:
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.multioutput import MultiOutputRegressor
from sklearn.pipeline import make_pipeline
# -------------------------------------------------------------------
# Modelo 4:
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputClassifier
# -------------------------------------------------------------------

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
w, h = 1400, 720
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Mona China Haciendo de Mario Bros")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, bala, nave, fondo, etc.
jugador = None
bala = None
fondo = None
nave = None
nave2 = None
menu = None
posicion_original_x = 90
posicion_original_y = h - 100

# Variables de salto
salto = False
en_suelo = True
salto_altura = 15  # Velocidad inicial de salto
gravedad = 3

# Variables de desplazamiento lateral
izquierda = False
ida = False
vuelta = False
sin_movimiento = True
desplazamiento = 46
velocidad_dezplazamiento = 6

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 48)
menu_activo = True
modo_auto = False  # Indica si el modo de juego es automático

# Lista para guardar los datos de velocidad, distancia y salto (target)
datos_modelo = []

# Variables Extras
titulo = pygame.font.SysFont('Arial', 64)
modelo = 0;

# Variables para los modelos 
nnNetwork = None
decisionTree = None
regresionLineal = None

#---------------------------------------------------------------------------------------------------------------------------------
# Cargar música
pygame.mixer.music.load('assets/audio/julijuliwa.mp3')              # Música de fondo
sonido_muerte = pygame.mixer.Sound('assets/audio/game_over.wav')    # Sonido al morir

# Cargar imagen de la bala
bala_img = pygame.transform.scale(pygame.image.load(f'assets/sprites/balamario.png').convert_alpha(), (20, 15))
bala2_img = pygame.transform.rotate(
    pygame.transform.scale(
        pygame.image.load('assets/sprites/balamario.png').convert_alpha(), 
        (30, 15)
    ), 
    90
)

# Cargar frames de mona chichona
jugador_frames = [
    pygame.transform.scale(pygame.image.load(f'assets/jugadora/Jugadora-Frame-{i}.png').convert_alpha(), (27, 42))
    for i in range(7)
]

# Variables para la animación de la mona china
current_frame = 0
frame_speed = 3
frame_count = 0

# Cargar frames de la nave animada
nave_frames = [
    pygame.transform.scale(pygame.image.load(f'assets/gun/frame_{i}_delay-0.03s.png').convert_alpha(), (90, 120))
    for i in range(17)
]

navey = pygame.transform.scale(pygame.image.load("./assets/game/ufo.png").convert_alpha(), (100, 60))

# Variables para la animación de la nave
current_frame_nave = 0
frame_speed_nave = 0.5
frame_count_nave = 0

# Cargar frames del fondo
fondo_frames = [
    pygame.transform.scale(pygame.image.load(f'assets/AI-Frames/frame_{i}_delay-0.04s.gif').convert(), (w, h))
    for i in range(39)
]

# Variables para la animación del fondo
current_frame_fondo = 0
frame_speed_fondo = 0.5
frame_count_fondo = 0
#--------------------------------------------------------------------------------------------------------------------------------
# Crear el rectángulo del jugador y de la bala
jugador = pygame.Rect(posicion_original_x, posicion_original_y, 27, 42)
bala = pygame.Rect(w - 30, h - 78, 30, 15)
bala2 = pygame.Rect(100, 5, 15, 30)
nave = pygame.Rect(w - 90, h - 130, 90, 120)
nave2 = pygame.Rect(60, 10, 100, 60)

# Variables para la bala
velocidad_bala = -18
bala_disparada = False

# Variables para la bala2
velocidad_bala2 = 5
bala2_disparada = False

# ------------------------------------------------------------------------------------------------------------------------------
# Balas
# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-20, -18)  # Velocidad aleatoria negativa para la bala
        bala_disparada = True

# Función para disparar la bala2
def disparar_bala2():
    global bala2_disparada, velocidad_bala2
    if not bala2_disparada:
        bala2_disparada = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 30  # Reiniciar la posición de la bala
    bala_disparada = False

# Función para reiniciar la posición de la bala2
def reset_bala2():
    global bala2, bala2_disparada
    bala2.y = 15
    bala2_disparada = False

# ------------------------------------------------------------------------------------------------------------------------------
# Salto y Desplazamiento
# Función para manejar salto
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura  # Mover al jugador hacia arriba
        salto_altura -= gravedad  # Aplicar gravedad (reduce la velocidad del salto)

        # Si el jugador llega al suelo, detener el salto
        if jugador.y >= posicion_original_y:
            jugador.y = posicion_original_y
            salto = False
            salto_altura = 18  # Restablecer la velocidad de salto
            en_suelo = True

# Función para manejar el desplazamiento lateral
def manejar_desplazamiento():
    global jugador, izquierda, desplazamiento, velocidad_dezplazamiento, posicion_original_x, sin_movimiento, ida, vuelta, salto
    
    if izquierda:
        if ida and jugador.x > posicion_original_x - desplazamiento:
            jugador.x -= velocidad_dezplazamiento
            if jugador.x <= posicion_original_x - desplazamiento:
                ida = False
                vuelta = True
        elif vuelta and jugador.x < posicion_original_x:
            
            jugador.x += velocidad_dezplazamiento
            
            if jugador.x >= posicion_original_x:
                jugador.x = posicion_original_x
                izquierda = False
                sin_movimiento = True
                ida = False
                vuelta = False

# ------------------------------------------------------------------------------------------------------------------------------
# Funciones del juego principal (Pausa, menu, reiniciar, captura de datos)
# Función para pausar el juego
def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        pygame.mixer.music.pause()
        # print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
    else:
        pygame.mixer.music.unpause()
        print("Juego reanudado.")

# Función para mostrar el menú y seleccionar el modo de juego
def mostrar_menu():
    global menu_activo, modo_auto, nnNetwork
    pantalla.fill(NEGRO)
    
    # Textos a mostrar
    textos = [
        "PyGames: Mona China Tetona Haciendo de Mario Bros",
        "M: Modo Manual",
        "A: Modo Automático con Diferentes Modelos",
        "G: Gráfica del Dataset de entrenamiento de los modelos",
        "Q: Salir del Juego"
    ]
    
    # Renderizar y centrar cada línea de texto
    y_offset = h // 2 - 160
    for texto in textos:
        if texto == "PyGames: Mona China Tetona Haciendo de Mario Bros":
            texto_renderizado = titulo.render(texto, True, BLANCO)
        else:
            texto_renderizado = fuente.render(texto, True, BLANCO)
        texto_ancho = texto_renderizado.get_width()  # Obtener el ancho del texto
        texto_x = (w - texto_ancho) // 2  # Calcular la posición X para centrar
        pantalla.blit(texto_renderizado, (texto_x, y_offset))  # Dibujar el texto
        if texto == "PyGames: Mona China Tetona Haciendo de Mario Bros":
            y_offset += 150  # Espacio entre líneas
        else:
            y_offset += 50  # Espacio entre líneas
    
    pygame.display.flip()
    
    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:        # Modo Automático
                    modo_auto = True
                    menu_activo = False
                    seleccionar_modelo()           # Mostrar pantalla de selección de modelo
                elif evento.key == pygame.K_m:      # Modo Manual
                    modo_auto = False
                    menu_activo = False
                elif evento.key == pygame.K_g:      # Modo Gráfica
                    menu_activo = False
                    graficar()
                elif evento.key == pygame.K_q:      # Salir
                    pygame.quit()
                    exit()

# Función para reiniciar el juego tras la colisión
def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo, datos_modelo, bala2, bala2_disparada, izquierda, derecha , sin_movimiento, ida, vuelta
    
    jugador.x, jugador.y = posicion_original_x, h - 120
    bala.x, bala.y = w - 30, h - 100
    nave.x, nave.y = w - 90, h - 150
    bala2.x, bala2.y = nave2.x + nave2.width//2 - 15, nave2.y + nave2.height
    bala_disparada = False
    bala2_disparada = False
    salto = False
    en_suelo = True
    izquierda = False
    derecha = False
    sin_movimiento = True
    ida = False
    vuelta = False
    menu_activo = True
    
    # Reproducir sonido de muerte
    sonido_muerte.play()
    
    # Si hay datos en datos_modelo, preguntar si se desea sobrescribir un modelo
    if datos_modelo:
        preguntar_sobrescribir_modelo()
        datos_modelo.clear()  # Limpiar los datos después de sobrescribir
    else:
        mostrar_menu()  # Mostrar el menú de nuevo para seleccionar modo
    pygame.mixer.music.unpause()  # Pausar la música

# Función para guardar datos del modelo
def guardar_datos():
    global jugador, bala, bala2, velocidad_bala, velocidad_bala2, salto, izquierda
    
    # Distancias a las balas
    distancia_bala = abs(jugador.x - bala.x)
    distancia_bala2 = abs(jugador.y - bala2.y)
    
    # Estados actuales
    salto_hecho = 1 if salto else 0
    izquierda_hecho = 1 if izquierda else 0
    
    # Trampa para el ruido de los datos
    if distancia_bala > 1100:
        salto_hecho = 0
    
    if distancia_bala2 > 400:
        izquierda_hecho = 0
    
    # Guardar todos los datos relevantes (ahora con 2 salidas)
    datos_modelo.append({
        'input': [
            distancia_bala, 
            velocidad_bala,
            distancia_bala2
        ],
        'output': [
            salto_hecho,
            izquierda_hecho
        ]
    })

# ------------------------------------------------------------------------------------------------------------------------------
# Funciones para los modelo + grafciar
# Función para seleccionar el modelo en modo automático
def seleccionar_modelo():
    global modelo, menu_activo
    pantalla.fill(NEGRO)
    
    textos = [
        "Seleccione el modelo (1-4):",
        "1: Red Neural",
        "2: Árbol de Decisiones",
        "3: Regresion Lineal",
        "4: K Nearest Neighbor"
    ]
    
    y_offset = h // 2 - 160
    for texto in textos:
        if texto == "Seleccione el modelo (1-4):":
            texto_renderizado = titulo.render(texto, True, BLANCO)
        else:
            texto_renderizado = fuente.render(texto, True, BLANCO)
        texto_ancho = texto_renderizado.get_width()
        texto_x = (w - texto_ancho) // 2
        pantalla.blit(texto_renderizado, (texto_x, y_offset))
        if texto == "Seleccione el modelo (1-4):":
            y_offset += 150
        else:
            y_offset += 50

    pygame.display.flip()

    seleccionando = True
    while seleccionando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    enRedNeural()               # Iniciar Modelo 1: Red Neuronal
                    modelo = 1                  # Actualizar la variable modelo
                    seleccionando = False       # Salir del bucle
                    menu_activo = False         # Cerrar el menú
                elif evento.key == pygame.K_2:
                    decision_tree()                  # Iniciar Modelo 2:
                    modelo = 2                  # Actualizar la variable modelo
                    seleccionando = False       # Salir del bucle
                    menu_activo = False         # Cerrar el menú
                elif evento.key == pygame.K_3:
                    regrecionLineal()                   # Iniciar Modelo 3:
                    modelo = 3                  # Actualizar la variable modelo
                    seleccionando = False       # Salir del bucle
                    menu_activo = False         # Cerrar el menú
                elif evento.key == pygame.K_4:
                    kNearestNeighbor()                   # Iniciar Modelo 4:
                    modelo = 4                  # Actualizar la variable modelo
                    seleccionando = False       # Salir del bucle
                    menu_activo = False         # Cerrar el menú                 # Volver al menú principal después de seleccionar

# Función para preguntar si se desea sobrescribir un modelo existente
def preguntar_sobrescribir_modelo():
    global datos_modelo
    pantalla.fill(NEGRO)
    
    # Textos a mostrar
    textos = [
        "¿Deseas entrenar nuevos modelos?",
        "1: SI",
        "2: NO"
    ]
    
    y_offset = h // 2 - 160
    for texto in textos:
        if texto == "¿Deseas entrenar nuevos modelos?":
            texto_renderizado = titulo.render(texto, True, BLANCO)
        else:
            texto_renderizado = fuente.render(texto, True, BLANCO)
        texto_ancho = texto_renderizado.get_width()
        texto_x = (w - texto_ancho) // 2
        pantalla.blit(texto_renderizado, (texto_x, y_offset))
        if texto == "¿Deseas entrenar nuevos modelos?":
            y_offset += 150
        else:
            y_offset += 50
    
    pygame.display.flip()

    seleccionando = True
    while seleccionando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    datos_csv = {
                        'Distancia_Bala': [dato['input'][0] for dato in datos_modelo],
                        'Velocidad_Bala': [dato['input'][1] for dato in datos_modelo],
                        'Distancia_Bala2': [dato['input'][2] for dato in datos_modelo],
                        'Salto': [dato['output'][0] for dato in datos_modelo],
                        'Izquierda': [dato['output'][1] for dato in datos_modelo]
                    }
                    
                    df = pd.DataFrame(datos_csv)
                    df.to_csv('./Models/Data/Data_Entrenmiento.csv', index=False)
                    
                    modelos = [
                        'RedNeural', 
                        'DecisionTree', 
                        'RegrecionLineal', 
                        'KNearestNeighbor'
                    ]
                    
                    for modelo_nombre in modelos:
                        # Eliminar archivos del modelo
                        model_path = f'./Models/{modelo_nombre}.joblib'
                        if os.path.exists(model_path):
                            os.remove(model_path)
                        
                        # Eliminar archivos de imágenes (para árbol de decisiones)
                        img_paths = [
                            f'./Models/PDF/{modelo_nombre}.dot',
                            f'./Models/PDF/{modelo_nombre}.pdf',
                            f'./Models/PDF/{modelo_nombre}.png'
                        ]
                        for path in img_paths:
                            if os.path.exists(path):
                                os.remove(path)

                    enRedNeural()
                    decision_tree()
                    regrecionLineal()
                    kNearestNeighbor()
                    
                    print("Todos los modelos han sido entrenados")
                    
                    seleccionando = False
                    
                elif evento.key == pygame.K_2:  # No - Conservar modelos actuales
                    datos_modelo.clear()
                    seleccionando = False
    
    mostrar_menu()

# Función para graficar el dataset de entrenamiento almacenado en un archivo CSV
def graficar():
    # Usar siempre el mismo archivo de datos
    data_filename = './Models/Data/Data_Entrenmiento.csv'
    
    if not os.path.exists(data_filename):
        print(f"No existe archivo de datos de entrenamiento: {data_filename}")
        mostrar_menu()
        return
    
    python_path = '../.venv/Scripts/python.exe'
    
    # Ejecutar el script de graficación
    subprocess.run([
        python_path, 
        './grafica.py', 
        data_filename,
        '--features', 'Distancia_Bala', 'Velocidad_Bala', 'Distancia_Bala2',
        '--targets', 'Salto', 'Izquierda'
    ])
    
    mostrar_menu()

# --------------------------------------------------------------------------------------------------------------------------------
# Función crear direcctorios si no existen
def asegurar_directorios():
    # Definir la ruta de los directorios
    directorios = [
        './Models',
        './Models/Data',
        './Models/PDF'
    ]
    # Crear los directorios si no existen
    for directorio in directorios:
        os.makedirs(directorio, exist_ok=True)

# --------------------------------------------------------------------------------------------------------------------------------
# Modelo 1: Red Neuronal usando SkLearn
def enRedNeural():
    global nnNetwork, modelo
    # Nombre del modelo
    model_filename = './Models/RedNeural.joblib'
    
    if os.path.exists(model_filename):
        # Cargar el modelo si ya existe
        nnNetwork = load(model_filename)
        print("Modelo cargado.")
    else:
        # Entrenar un nuevo modelo si no existe
        X = np.array([dato['input'] for dato in datos_modelo])  # Entradas
        y = np.array([dato['output'] for dato in datos_modelo])  # Salidas (ahora con dos salidas)
        
        # Crear y entrenar la red neuronal para múltiples salidas
        nnNetwork = MLPClassifier(
            hidden_layer_sizes=(10,),  # Una capa oculta con 10 neuronas
            activation='relu',         # Función de activación ReLU
            learning_rate_init=0.01,   # Tasa de aprendizaje
            max_iter=40000,            # Número máximo de iteraciones
            random_state=42            # Semilla para reproducibilidad
        )

        nnNetwork.fit(X, y)                 # Entrenar el modelo
        dump(nnNetwork, model_filename)     # Guardar el modelo entrenado
        print("Modelo entrenado y guardado.")

def predecirConRedNeuronal(param_entrada):
    global nnNetwork
    
    if nnNetwork is None:
        enRedNeural()
        print(f"Error: El modelo no está cargado.")
        return False, False

    try:
        # Primero usa predict para ver la estructura de salida
        clase_predicha = nnNetwork.predict([param_entrada])
        print("\n--- Predicción Red Neuronal ---")
        print(f"Input: {param_entrada}")
        print(f"Predicción: {clase_predicha}")
        
        saltar = clase_predicha[0][0]
        izquierda = clase_predicha[0][1]
        
        return saltar == 1, izquierda == 1
    except Exception as e:
        print(f"Error en predicción Red Neuronal: {str(e)}")
        return False, False

# --------------------------------------------------------------------------------------------------------------------------------
# Modelo 2: Árbol de Decisiones
def decision_tree():
    global decisionTree, modelo
    
    asegurar_directorios()
    model_filename = os.path.abspath('./Models/DecisionTree.joblib')
    
    if os.path.exists(model_filename):
        decisionTree = load(model_filename)
        print("Modelo de Árbol de Decisiones cargado.")
    else:
        # Preparar datos para un solo árbol con múltiples salidas
        X = []
        y = []
        
        for dato in datos_modelo:
            X.append(dato['input'])
            y.append(dato['output'])
        
        X = np.array(X)
        y = np.array(y)
        
        # Crear un solo árbol de decisiones para múltiples salidas
        decisionTree = DecisionTreeClassifier(
            max_depth=10,
            random_state=42
        )
        
        print("\nEntrenando Árbol de Decisiones único...")
        decisionTree.fit(X, y)
        
        # Guardar el modelo
        dump(decisionTree, model_filename)
        
        print("Modelo de Árbol de Decisiones único entrenado y guardado.")

def predecirConArbolDecisiones(param_entrada):
    global decisionTree
    if decisionTree is None:
        decision_tree()
        return False, False
    
    try:
        # Predecir ambas salidas con un solo árbol
        prediccion = decisionTree.predict([param_entrada])[0]
        
        print("\nPredicción Árbol Decisiones")
        print(f"Input: {param_entrada}")
        print(f"Predicción: {prediccion}")
        
        return prediccion[0] == 1, prediccion[1] == 1
    except Exception as e:
        print(f"Error en predicción Árbol Decisiones: {str(e)}")
        return False, False

# --------------------------------------------------------------------------------------------------------------------------------
# Modelo 4:
def kNearestNeighbor():
    global knnModel, modelo
    asegurar_directorios()
    model_filename = './Models/KNearestNeighbor.joblib'
    
    if os.path.exists(model_filename):
        knnModel = load(model_filename)
        print("Modelo KNN cargado.")
    else:
        X = np.array([dato['input'][:3] for dato in datos_modelo])
        y = np.array([dato['output'] for dato in datos_modelo])
        
        knnModel = Pipeline([
            ('scaler', StandardScaler()),
            ('knn', MultiOutputClassifier(
                KNeighborsClassifier(
                    n_neighbors=5,
                    weights='distance',
                    algorithm='auto',
                    leaf_size=30,
                    metric='minkowski'
                )
            ))
        ])
        
        print("\nEntrenando KNN...")
        knnModel.fit(X, y)
        dump(knnModel, model_filename)

def predecirConKNN(param_entrada):
    global knnModel
    if knnModel is None:
        return False, False
    
    try:
        entrada = param_entrada[:3] if len(param_entrada) > 3 else param_entrada
        prediccion = knnModel.predict([entrada])[0]
        print("\n--- Predicción KNN ---")
        print(f"Input: {entrada}")
        print(f"Predicción: {prediccion}")
        return (
            prediccion[0] == 1,
            prediccion[1] == 1
        )
    except Exception as e:
        print(f"Error en predicción KNN: {str(e)}")
        return False, False

# --------------------------------------------------------------------------------------------------------------------------------
# Modelo 3: Regresión Lineal
def regrecionLineal():
    global regresionLineal, modelo
    asegurar_directorios()
    model_filename = './Models/RegrecionLineal.joblib'
    
    if os.path.exists(model_filename):
        regresionLineal = load(model_filename)
        print("Modelo de Regresión Lineal cargado.")
    else:
        X = np.array([dato['input'][:3] for dato in datos_modelo])
        y = np.array([dato['output'] for dato in datos_modelo])
        
        modelo3_regression = MultiOutputRegressor(
            make_pipeline(
                StandardScaler(),
                LinearRegression()
            )
        )
        
        print("\nEntrenando Regresión Lineal...")
        modelo3_regression.fit(X, y)
        dump(modelo3_regression, model_filename)

def predecirConRegresionLineal(param_entrada):
    global regresionLineal
    if regresionLineal is None:
        return False, False
    
    try:
        entrada = param_entrada[:3] if len(param_entrada) > 3 else param_entrada
        
        prediccion = regresionLineal.predict([entrada])[0]

        print("\n--- Predicción Regresión Lineal ---")
        print(f"Input: {entrada}")
        print(f"Predicción: {prediccion}")
        
        return (
            prediccion[0] > 0.55,  # Convertir a probabilidad con función sigmoide
            prediccion[1] > 0.50
        )
    except Exception as e:
        print(f"Error en predicción Regresión Lineal: {str(e)}")
        return False, False

# --------------------------------------------------------------------------------------------------------------------------------
# Función para actualizar la pantalla y manejar la lógica del juego
def update():
    global bala, velocidad_bala, current_frame, frame_count, current_frame_fondo, frame_count_fondo, current_frame_nave, frame_count_nave, bala2

    # Limpiar la pantalla (o dibujar el fondo completo)
    pantalla.blit(fondo_frames[current_frame_fondo], (0, 0))  # Dibujar el fondo primero

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    # Animación del fondo
    frame_count_fondo += 1
    if frame_count_fondo >= frame_speed_fondo:
        current_frame_fondo = (current_frame_fondo + 1) % len(fondo_frames)
        frame_count_fondo = 0

    # Animación de la nave
    frame_count_nave += 1
    if frame_count_nave >= frame_speed_nave:
        current_frame_nave = (current_frame_nave + 1) % len(nave_frames)
        frame_count_nave = 0

    # Mover y dibujar la bala (ENCIMA DEL FONDO)
    if bala_disparada:
        bala.x += velocidad_bala
        
    if bala2_disparada:
        bala2.y += velocidad_bala2

    # Si la bala sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()

    # Si la bala2 sale de la pantalla, reiniciar su posición
    if bala2.y >= h-20:
        reset_bala2()

    # Dibujar el jugador con la animación (ENCIMA DEL FONDO)
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))
    pygame.draw.rect(pantalla, (0, 255, 0), jugador, 2)                 # Dibujar hitbox del jugador en verde
    
    # Dibujar la bala (ENCIMA DEL FONDO)
    pantalla.blit(bala_img, (bala.x, bala.y))
    pygame.draw.rect(pantalla, (0, 255, 0), bala, 2)
    
    # Dibujar la bala2 (ENCIMA DEL FONDO)
    pantalla.blit(bala2_img, (bala2.x, bala2.y))
    pygame.draw.rect(pantalla, (255, 0, 0), bala2, 2)
    
    # Dibujar la nave con la animación (ENCIMA DEL FONDO)
    pantalla.blit(nave_frames[current_frame_nave], (nave.x, nave.y))
    pygame.draw.rect(pantalla, (0, 255, 0), nave, 2)                    # Dibujar hitbox de la nave en verde

    # Dibujar la nave con la animación (ENCIMA DEL FONDO)
    pantalla.blit(navey, (nave2.x, nave2.y))
    pygame.draw.rect(pantalla, (0, 255, 0), nave2, 2)   
    
    # Colisión entre la bala y el jugador
    if jugador.colliderect(bala):
        pygame.mixer.music.pause()      # Pausar la música
        print("Colisión detectada!")
        reiniciar_juego()               # Terminar el juego y mostrar el menú

    # Colisión entre la bala2 y el jugador
    if jugador.colliderect(bala2):
        pygame.mixer.music.pause()
        print("Colisión con bala2 detectada!")
        reiniciar_juego()

# ------------------------------------------------------------------------------------------------------------------------------
# Función principal del juego
def main():
    global salto, en_suelo, bala_disparada, bala2_disparada, modelo, derecha, sin_movimiento, ida, izquierda
    reloj = pygame.time.Clock()
    mostrar_menu()                  # Mostrar el menú al inicio
    pygame.mixer.music.play(-1)     # Reproducir música de fondo en bucle
    correr = True

    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa:
                    salto = True
                    en_suelo = False
                elif evento.key == pygame.K_LEFT and sin_movimiento and not pausa:
                    ida = True
                    izquierda = True
                    sin_movimiento = False
                elif evento.key == pygame.K_p:
                    pausa_juego()
                elif evento.key == pygame.K_q:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    exit()

        if not pausa:
            # Modo manual: el jugador controla el salto
            if not modo_auto:
                if salto:
                    manejar_salto()
                if izquierda:
                    manejar_desplazamiento()
                guardar_datos()
            # Modo automático: el modelo decide si saltar o no
            if modo_auto:
                match modelo:
                    case 1:
                        # Red Neuronal
                        entrada = [abs(jugador.x - bala.x), velocidad_bala, abs(jugador.y - bala2.y)]
                        saltar, mover_izquierda = predecirConRedNeuronal(entrada)[:2]
                        
                        if saltar and not salto and en_suelo:
                            salto = True
                            en_suelo = False
                        
                        if mover_izquierda and sin_movimiento:
                            izquierda = True
                            ida = True
                            sin_movimiento = False

                    case 2:
                        # Árbol de Decisiones
                        entrada = [abs(jugador.x - bala.x), velocidad_bala, abs(jugador.y - bala2.y)]

                        saltar, mover_izquierda = predecirConArbolDecisiones(entrada)[:2]

                        if saltar and not salto and en_suelo:
                            salto = True
                            en_suelo = False
                        
                        if mover_izquierda and sin_movimiento:
                            izquierda = True
                            ida = True
                            sin_movimiento = False

                    case 3:
                        # Regresión Lineal
                        entrada = [abs(jugador.x - bala.x), velocidad_bala, abs(jugador.y - bala2.y), velocidad_bala2]

                        saltar, mover_izquierda = predecirConRegresionLineal(entrada)[:2]
                        
                        if saltar and not salto and en_suelo:
                            salto = True
                            en_suelo = False
                        
                        if mover_izquierda and sin_movimiento:
                            izquierda = True
                            ida = True
                            sin_movimiento = False

                    case 4:
                        # K-Nearest Neighbors
                        entrada = [abs(jugador.x - bala.x), velocidad_bala, abs(jugador.y - bala2.y)]
                        
                        saltar, mover_izquierda = predecirConKNN(entrada)[:2]
                        
                        if saltar and not salto and en_suelo:
                            salto = True
                            en_suelo = False
                        
                        if mover_izquierda and sin_movimiento:
                            izquierda = True
                            ida = True
                            sin_movimiento = False

                if salto:
                    manejar_salto()
                if izquierda:
                    manejar_desplazamiento()

            # Actualizar el juego
            if not bala_disparada:
                disparar_bala()

            if not bala2_disparada:
                disparar_bala2()
            update()
        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(30)  # Limitar el juego a 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
