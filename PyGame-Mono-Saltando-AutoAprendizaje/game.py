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
# -------------------------------------------------------------------
# Modelo 4:
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
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

# Variables de salto
salto = False
en_suelo = True
salto_altura = 20  # Velocidad inicial de salto
gravedad = 2.5

# Variables de desplazamiento lateral
izquierda = False
ida = False
vuelta = False
sin_movimiento = True
desplazamiento = 120
velocidad_dezplazamiento = 10

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

#---------------------------------------------------------------------------------------------------------------------------------
# Cargar música
pygame.mixer.music.load('assets/audio/julijuliwa.mp3')              # Música de fondo
sonido_muerte = pygame.mixer.Sound('assets/audio/game_over.wav')    # Sonido al morir

# Cargar imagen de la bala
bala_img = pygame.transform.scale(pygame.image.load(f'assets/sprites/balamario.png').convert_alpha(), (40, 30))
bala2_img = pygame.transform.rotate(
    pygame.transform.scale(
        pygame.image.load('assets/sprites/balamario.png').convert_alpha(), 
        (40, 30)
    ), 
    90
)

# Cargar frames de mona chichona
jugador_frames = [
    pygame.transform.scale(pygame.image.load(f'assets/jugadora/Jugadora-Frame-{i}.png').convert_alpha(), (54, 84))
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
jugador = pygame.Rect(posicion_original_x, h - 120, 54, 84)
bala = pygame.Rect(w - 30, h - 100, 40, 30)
bala2 = pygame.Rect(100, 5, 30, 40)
nave = pygame.Rect(w - 90, h - 150, 90, 120)
nave2 = pygame.Rect(75, 10, 100, 60)

# Variables para la bala
velocidad_bala = -20
bala_disparada = False

# Variables para la bala2
velocidad_bala2 = 18
bala2_disparada = False

# ------------------------------------------------------------------------------------------------------------------------------
# Balas
# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-25, -20)  # Velocidad aleatoria negativa para la bala
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
    bala2.y = -5
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
        if jugador.y >= h - 120:
            jugador.y = h - 120
            salto = False
            salto_altura = 20  # Restablecer la velocidad de salto
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
            if salto:
                jugador.x += velocidad_dezplazamiento//2
            else:
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
                    seleccionar_modelo(1)           # Mostrar pantalla de selección de modelo
                elif evento.key == pygame.K_m:      # Modo Manual
                    modo_auto = False
                    menu_activo = False
                elif evento.key == pygame.K_g:      # Modo Gráfica
                    menu_activo = False
                    seleccionar_modelo(2)
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
def seleccionar_modelo(num_option):
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
                    if num_option == 1:
                        enRedNeural()               # Iniciar Modelo 1: Red Neuronal
                        modelo = 1                  # Actualizar la variable modelo
                        seleccionando = False       # Salir del bucle
                        menu_activo = False         # Cerrar el menú
                    elif num_option == 2:
                        graficar(1)                 # Graficar Modelo 1: Red Neuronal
                        seleccionando = False       # Salir del bucle
                        menu_activo = False         # Cerrar el menú
                elif evento.key == pygame.K_2:
                    if num_option == 1:
                        decision_tree()                  # Iniciar Modelo 2:
                        modelo = 2                  # Actualizar la variable modelo
                        seleccionando = False       # Salir del bucle
                        menu_activo = False         # Cerrar el menú
                    elif num_option == 2:
                        graficar(2)                 # Graficar Modelo 2
                        seleccionando = False       # Salir del bucle
                        menu_activo = False         # Cerrar el menú
                elif evento.key == pygame.K_3:
                    if num_option == 1:
                        regrecionLineal()                   # Iniciar Modelo 3:
                        modelo = 3                  # Actualizar la variable modelo
                        seleccionando = False       # Salir del bucle
                        menu_activo = False         # Cerrar el menú
                    elif num_option == 2:
                        graficar(3)                 # Graficar Modelo 3
                        seleccionando = False       # Salir del bucle
                        menu_activo = False         # Cerrar el menú
                elif evento.key == pygame.K_4:
                    if num_option == 1:
                        kNearestNeighbor()                   # Iniciar Modelo 4:
                        modelo = 4                  # Actualizar la variable modelo
                        seleccionando = False       # Salir del bucle
                        menu_activo = False         # Cerrar el menú
                    elif num_option == 2:
                        graficar(4)                 # Graficar Modelo 4
                        seleccionando = False       # Salir del bucle
                        menu_activo = False         # Cerrar el menú                       # Volver al menú principal después de seleccionar

# Función para preguntar si se desea sobrescribir un modelo existente
def preguntar_sobrescribir_modelo():
    global datos_modelo
    pantalla.fill(NEGRO)
    
    # Textos a mostrar
    textos = [
        "¿Quieres sobrescribir algún modelo?",
        "1: Red Neural",
        "2: Árbol de Decisiones",
        "3: Regreción Lineal",
        "4: K Nearest Neighbor",
        "5: No sobrescribir"
    ]
    
    y_offset = h // 2 - 160
    for texto in textos:
        if texto == "¿Quieres sobrescribir algún modelo?":
            texto_renderizado = titulo.render(texto, True, BLANCO)
        else:
            texto_renderizado = fuente.render(texto, True, BLANCO)
        texto_ancho = texto_renderizado.get_width()  # Obtener el ancho del texto
        texto_x = (w - texto_ancho) // 2  # Calcular la posición X para centrar
        pantalla.blit(texto_renderizado, (texto_x, y_offset))  # Dibujar el texto
        if texto == "¿Quieres sobrescribir algún modelo?":
            y_offset += 150  # Espacio entre líneas
        else:
            y_offset += 50  # Espacio entre líneas
    
    pygame.display.flip()

    seleccionando = True
    while seleccionando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:    # Sobrescribir Modelo 1
                    sobrescribir_modelo(1)
                    seleccionando = False
                elif evento.key == pygame.K_2:  # Sobrescribir Modelo 2
                    sobrescribir_modelo(2)
                    seleccionando = False
                elif evento.key == pygame.K_3:  # Sobrescribir Modelo 3
                    sobrescribir_modelo(3)
                    seleccionando = False
                elif evento.key == pygame.K_4:  # Sobrescribir Modelo 4
                    sobrescribir_modelo(4)
                    seleccionando = False
                elif evento.key == pygame.K_5:  # No sobrescribir
                    datos_modelo.clear()        # Limpiar los datos sin sobrescribir           # Limpiar los datos sin sobrescribir
                    seleccionando = False
    mostrar_menu()                              # Volver al menú principal después de seleccionar

# Función para sobrescribir un modelo existente si lo desea el usuario
def sobrescribir_modelo(modelo_num):
    global datos_modelo
    
    switcher = {
        1: 'RedNeural',
        2: 'DecisionTree',
        3: 'RegrecionLineal',
        4: 'KNearestNeighbor'
    }
    
    modelo_nombre = switcher.get(modelo_num, 'ModeloDesconocido')
    base_path = f'./Models/{modelo_nombre}'
    data_path = f'./Models/Data/{modelo_nombre}'
    images_path = f'./Models/Images/{modelo_nombre}'
    
    # Eliminar todos los archivos relacionados
    for path, extensions in [
        (base_path, ['.joblib']),
        (data_path, ['.csv']),
        (images_path, ['.dot', '.pdf', '.png'])
    ]:
        for ext in extensions:
            file_path = f"{path}{ext}"
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Archivo eliminado: {file_path}")
    
    # Entrenar nuevo modelo según el tipo
    match modelo_num:
        case 1:
            enRedNeural()
        case 2:
            decision_tree()
        case 3:
            regrecionLineal()
        case 4:
            kNearestNeighbor()
        case _:
            print("Modelo Desconocido")
    
    datos_modelo.clear()

# Función para graficar el dataset de entrenamiento almacenado en un archivo CSV
def graficar(num_modelo):
    switcher = {
        1: 'RedNeural',
        2: 'DecisionTree',
        3: 'RegrecionLineal',
        4: 'KNearestNeighbor'
    }

    modelo_nombre = switcher.get(num_modelo, 'ModeloDesconocido')
    data_filename = f'./Models/Data/{modelo_nombre}.csv'
    
    if not os.path.exists(data_filename):
        print(f"No existe archivo de datos para {modelo_nombre}")
        mostrar_menu()
        return
    
    python_path = '../.venv/Scripts/python.exe'
    
    # Ejecutar grafica.py con argumentos adicionales para manejar las nuevas columnas
    subprocess.run([
        python_path, 
        './grafica.py', 
        data_filename,
        '--features', 'Distancia_Bala', 'Velocidad_Bala', 'Distancia_Bala2',
        '--targets', 'Salto', 'Derecha', 'Izquierda'
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
    asegurar_directorios()
    model_filename = './Models/RedNeural.joblib'
    data_filename = './Models/Data/RedNeural.csv'
    
    if os.path.exists(model_filename):
        nnNetwork = load(model_filename)
        print("Modelo de Red Neuronal cargado.")
        return
    
    if len(datos_modelo) < 50:
        print("⚠️ Advertencia: Insuficientes datos para entrenar. Necesitas al menos 50 ejemplos.")
        return
    
    try:
        X = []
        y_salto = []
        y_izquierda = []
        
        for dato in datos_modelo:
            input_data = dato['input']
            X.append([input_data[0], input_data[1], input_data[2]])
            
            output = dato['output']
            y_salto.append(output[0])
            y_izquierda.append(output[1])
        
        X = np.array(X)
        y = np.column_stack((y_salto, y_izquierda))
        
        nnNetwork = MLPClassifier(
            hidden_layer_sizes=(64, 32),
            activation='relu',
            solver='adam',
            alpha=0.0001,
            learning_rate_init=0.001,
            max_iter=500,
            early_stopping=True,
            validation_fraction=0.15,
            n_iter_no_change=20,
            tol=0.0005,
            random_state=42,
            verbose=False
        )

        print("\nEntrenando Red Neuronal...")
        nnNetwork.fit(X, y)
        
        if nnNetwork.n_iter_ == nnNetwork.max_iter:
            print("⚠️ Advertencia: El modelo no convergió completamente")
        
        dump(nnNetwork, model_filename)
        
        datos_csv = {
            'Distancia_Bala': [d[0] for d in X],
            'Velocidad_Bala': [d[1] for d in X],
            'Distancia_Bala2': [d[2] for d in X],
            'Salto': y_salto,
            'Izquierda': y_izquierda
        }
        pd.DataFrame(datos_csv).to_csv(data_filename, index=False)
        print("✅ Red Neuronal entrenada y guardada exitosamente")
        
    except Exception as e:
        print(f"❌ Error crítico durante el entrenamiento: {str(e)}")
        for f in [model_filename, data_filename]:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except:
                    pass
        raise

def predecirConRedNeuronal(param_entrada):
    global nnNetwork
    if nnNetwork is None:
        print("Modelo de Red Neuronal no cargado")
        return False, False
    
    try:
        entrada = param_entrada[:3] if len(param_entrada) > 3 else param_entrada
        if len(entrada) < 3:
            entrada = list(entrada) + [0] * (3 - len(entrada))
        
        proba = nnNetwork.predict_proba([entrada])
        
        if isinstance(proba, list):
            prob_salto = proba[0][0][1] if len(proba[0][0]) > 1 else 0
            prob_izquierda = proba[1][0][1] if len(proba[1][0]) > 1 else 0
        else:
            prob_salto = prob_izquierda = proba[0][1] if len(proba[0]) > 1 else 0
        
        print("\n--- Predicción Red Neuronal ---")
        print(f"Input: {entrada}")
        print(f"Probabilidad de Saltar: {prob_salto:.2f}")
        print(f"Probabilidad de Izquierda: {prob_izquierda:.2f}")
        
        return (
            prob_salto > 0.65,
            prob_izquierda > 0.55
        )
        
    except Exception as e:
        print(f"Error en predicción Red Neuronal: {str(e)}")
        return False, False

# --------------------------------------------------------------------------------------------------------------------------------
# Modelo 2: Árbol de Decisiones
def decision_tree():
    global decisionTree, modelo
    
    asegurar_directorios()
    model_filename = os.path.abspath('./Models/DecisionTree.joblib')
    data_filename = os.path.abspath('./Models/Data/DecisionTree.csv')
    tree_filename_base = os.path.abspath('./Models/PDF/DecisionTree')
    
    if os.path.exists(model_filename):
        decisionTree = load(model_filename)
        print("Modelo de Árbol de Decisiones cargado.")
    else:
        for ext in ['.joblib', '.csv', '.dot', '.pdf', '.png']:
            file_path = f"{tree_filename_base}{ext}" if ext in ['.dot', '.pdf', '.png'] else model_filename if ext == '.joblib' else data_filename
            if os.path.exists(file_path):
                os.remove(file_path)
    
        X = []
        y_salto = []
        y_izquierda = []
        
        for dato in datos_modelo:
            X.append(dato['input'])
            output = dato['output']
            y_salto.append(output[0])
            y_izquierda.append(output[1])
        
        X = np.array(X)
        
        decisionTree = {
            'salto': DecisionTreeClassifier(
                max_depth=5,
                min_samples_split=10,
                random_state=42
            ),
            'izquierda': DecisionTreeClassifier(
                max_depth=5,
                min_samples_split=10,
                random_state=42
            )
        }
        
        print("\nEntrenando Árboles de Decisión...")
        decisionTree['salto'].fit(X, y_salto)
        decisionTree['izquierda'].fit(X, y_izquierda)
        
        dump(decisionTree, model_filename)
        
        datos_csv = {
            'Distancia_Bala': [d[0] for d in X],
            'Velocidad_Bala': [d[1] for d in X],
            'Distancia_Bala2': [d[2] for d in X],
            'Salto': y_salto,
            'Izquierda': y_izquierda
        }
        pd.DataFrame(datos_csv).to_csv(data_filename, index=False)

        for accion in ['salto', 'izquierda']:
            generar_pdf_arbol(decisionTree[accion], f"{tree_filename_base}_{accion}", accion)
        
        print("Modelo de Árbol de Decisiones entrenado y guardado.")

def predecirConArbolDecisiones(param_entrada):
    global decisionTree
    if decisionTree is None or not isinstance(decisionTree, dict):
        return False, False
    
    try:
        saltar = decisionTree['salto'].predict([param_entrada])[0] == 1
        izquierda = decisionTree['izquierda'].predict([param_entrada])[0] == 1
        
        print("\n--- Predicción Árbol Decisiones ---")
        print(f"Input: {param_entrada}")
        print(f"Saltar: {'Sí' if saltar else 'No'}")
        print(f"Izquierda: {'Sí' if izquierda else 'No'}")
        print("----------------------------------")
        
        return saltar, izquierda
    except Exception as e:
        print(f"Error en predicción Árbol Decisiones: {str(e)}")
        return False, False

def generar_pdf_arbol(arbol, filename_base, accion):
    try:
        # Asegurar que el directorio existe
        os.makedirs(os.path.dirname(filename_base), exist_ok=True)
        
        # Verificar que graphviz esté instalado correctamente
        if not hasattr(graphviz, 'Source'):
            raise ImportError("Graphviz no está instalado correctamente")
        
        # Nombres de archivo temporales
        dot_file = f"{filename_base}.dot"
        pdf_file = f"{filename_base}.pdf"
        png_file = f"{filename_base}.png"
        
        # Limpiar archivos existentes
        for f in [dot_file, pdf_file, png_file]:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except PermissionError:
                    print(f"Error: No se pudo eliminar {f} - Permiso denegado")
                    continue
        
        # Exportar a formato DOT
        tree.export_graphviz(
            arbol,
            out_file=dot_file,
            feature_names=['Distancia_Bala', 'Velocidad_Bala', 'Distancia_Bala2'],
            class_names=['No_'+accion.capitalize(), accion.capitalize()],
            filled=True,
            rounded=True,
            special_characters=True,
            proportion=True
        )
        
        # Verificar que el archivo DOT se creó
        if not os.path.exists(dot_file):
            raise FileNotFoundError(f"No se pudo crear el archivo DOT: {dot_file}")
        
        # Generar gráficos
        graph = graphviz.Source.from_file(dot_file)
        
        # Renderizar a PDF
        try:
            pdf_path = graph.render(
                filename=filename_base,
                format='pdf',
                cleanup=True,
                quiet=True
            )
            if not os.path.exists(pdf_path):
                raise RuntimeError(f"El archivo PDF no se generó: {pdf_path}")
            print(f"✓ PDF generado: {pdf_path}")
        except Exception as pdf_error:
            print(f"Error al generar PDF: {str(pdf_error)}")
        
        # Renderizar a PNG
        try:
            png_path = graph.render(
                filename=filename_base,
                format='png',
                cleanup=True,
                quiet=True
            )
            if not os.path.exists(png_path):
                raise RuntimeError(f"El archivo PNG no se generó: {png_path}")
            print(f"✓ PNG generado: {png_path}")
        except Exception as png_error:
            print(f"Error al generar PNG: {str(png_error)}")
        
    except Exception as e:
        print(f"❌ Error crítico al generar árbol para {accion}: {str(e)}")
        # Intenta limpiar archivos temporales en caso de error
        for f in [dot_file, pdf_file, png_file]:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except:
                    pass

# --------------------------------------------------------------------------------------------------------------------------------
# Modelo 3: Regresión Lineal
def regrecionLineal():
    global modelo3_regression, modelo
    asegurar_directorios()
    model_filename = './Models/RegrecionLineal.joblib'
    data_filename = './Models/Data/RegrecionLineal.csv'
    
    if os.path.exists(model_filename):
        modelo3_regression = load(model_filename)
        print("Modelo de Regresión Lineal cargado.")
    else:
        X = np.array([dato['input'][:3] for dato in datos_modelo])
        y = np.array([dato['output'] for dato in datos_modelo])
        
        from sklearn.multioutput import MultiOutputRegressor
        modelo3_regression = MultiOutputRegressor(
            LinearRegression(normalize=True)
        )
        
        print("\nEntrenando Regresión Lineal...")
        modelo3_regression.fit(X, y)
        dump(modelo3_regression, model_filename)
        
        datos_csv = {
            'Distancia_Bala': [d[0] for d in X],
            'Velocidad_Bala': [d[1] for d in X],
            'Distancia_Bala2': [d[2] for d in X],
            'Salto': [o[0] for o in y],
            'Izquierda': [o[1] for o in y]
        }
        pd.DataFrame(datos_csv).to_csv(data_filename, index=False)
        print("✅ Regresión Lineal entrenada y guardada")

def predecirConRegresionLineal(param_entrada):
    global modelo3_regression
    if modelo3_regression is None:
        return False, False
    
    try:
        entrada = param_entrada[:3] if len(param_entrada) > 3 else param_entrada
        prediccion = modelo3_regression.predict([entrada])[0]
        
        from scipy.special import expit
        return (
            expit(prediccion[0]) > 0.55,
            expit(prediccion[1]) > 0.5
        )
    except Exception as e:
        print(f"Error en predicción Regresión Lineal: {str(e)}")
        return False, False

# --------------------------------------------------------------------------------------------------------------------------------
# Modelo 4:
def kNearestNeighbor():
    global knnModel, modelo
    asegurar_directorios()
    model_filename = './Models/KNearestNeighbor.joblib'
    data_filename = './Models/Data/KNearestNeighbor.csv'
    
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
        
        datos_csv = {
            'Distancia_Bala': [d[0] for d in X],
            'Velocidad_Bala': [d[1] for d in X],
            'Distancia_Bala2': [d[2] for d in X],
            'Salto': [o[0] for o in y],
            'Izquierda': [o[1] for o in y]
        }
        pd.DataFrame(datos_csv).to_csv(data_filename, index=False)
        print("✅ KNN entrenado y guardado")

def predecirConKNN(param_entrada):
    global knnModel
    if knnModel is None:
        return False, False
    
    try:
        entrada = param_entrada[:3] if len(param_entrada) > 3 else param_entrada
        prediccion = knnModel.predict([entrada])[0]
        return (
            prediccion[0] == 1,
            prediccion[1] == 1
        )
    except Exception as e:
        print(f"Error en predicción KNN: {str(e)}")
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
    if bala2.y > h:
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
