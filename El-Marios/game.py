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
# Modelo 1: Red Neuronal con SkLearn
from sklearn.neural_network import MLPClassifier
# -------------------------------------------------------------------
# Modelo 2:

# -------------------------------------------------------------------
# Modelo 3:

# -------------------------------------------------------------------
# Modelo 4:

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
menu = None

# Variables de salto
salto = False
salto_altura = 30  # Velocidad inicial de salto
gravedad = 2
en_suelo = True

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
nnNetwork = None

#---------------------------------------------------------------------------------------------------------------------------------
# Cargar música
pygame.mixer.music.load('assets/audio/julijuliwa.mp3')              # Música de fondo
sonido_muerte = pygame.mixer.Sound('assets/audio/game_over.wav')    # Sonido al morir

# Cargar imagen de la bala
bala_img = pygame.transform.scale(pygame.image.load(f'assets/sprites/balamario.png').convert_alpha(), (130, 100))

# Cargar frames de mona chichona
jugador_frames = [
    pygame.transform.scale(pygame.image.load(f'assets/jugadora/Jugadora-Frame-{i}.png').convert_alpha(), (180, 384))
    for i in range(7)
]

# Variables para la animación de la mona china
current_frame = 0
frame_speed = 3
frame_count = 0

# Cargar frames de la nave animada
nave_frames = [
    pygame.transform.scale(pygame.image.load(f'assets/gun/frame_{i}_delay-0.03s.png').convert_alpha(), (250, 360))
    for i in range(17)
]

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
jugador = pygame.Rect(50, h - 400, 160, 330)
bala = pygame.Rect(w - 200, h - 220, 130, 100)
nave = pygame.Rect(w - 300, h - 380, 250, 360)

# Variables para la bala
velocidad_bala = -50  # Velocidad de la bala hacia la izquierda
bala_disparada = False

# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-25, -20)  # Velocidad aleatoria negativa para la bala
        bala_disparada = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 200  # Reiniciar la posición de la bala
    bala_disparada = False

def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura  # Mover al jugador hacia arriba
        salto_altura -= gravedad  # Aplicar gravedad (reduce la velocidad del salto)

        # Si el jugador llega al suelo, detener el salto
        if jugador.y >= h - 400:
            jugador.y = h - 400
            salto = False
            salto_altura = 30  # Restablecer la velocidad de salto
            en_suelo = True

# Función para pausar el juego y guardar los datos
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
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo, datos_modelo
    
    menu_activo = True  # Activar de nuevo el menú
    jugador.x, jugador.y = 50, h - 400  # Reiniciar posición del jugador
    bala.x = w - 200  # Reiniciar posición de la bala
    nave.x, nave.y = w - 300, h - 380  # Reiniciar posición de la nave
    bala_disparada = False
    salto = False
    en_suelo = True
    
    # Reproducir sonido de muerte
    sonido_muerte.play()
    
    # Si hay datos en datos_modelo, preguntar si se desea sobrescribir un modelo
    if datos_modelo:
        preguntar_sobrescribir_modelo()
        datos_modelo.clear()  # Limpiar los datos después de sobrescribir
    else:
        mostrar_menu()  # Mostrar el menú de nuevo para seleccionar modo
    pygame.mixer.music.unpause()  # Pausar la música

# Función para guardar datos del modelo en modo manual
def guardar_datos():
    global jugador, bala, velocidad_bala, salto
    distancia = abs(jugador.x - bala.x)
    salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
    
    # No guardar datos si la distancia es mayor a 800 y ya se hizo un salto
    if  distancia > 800 and salto_hecho == 1:
        return
    
    # Guardar distancia al jugador,  velocidad de la bala y si saltó o no
    datos_modelo.append({'input': [distancia, velocidad_bala], 'output': [salto_hecho]}) # Salida: (0 = suelo, 1 = aire)
# ------------------------------------------------------------------------------------------------------------------------------
# Función para seleccionar el modelo en modo automático
def seleccionar_modelo(num_option):
    global modelo, menu_activo
    pantalla.fill(NEGRO)
    
    textos = [
        "Seleccione el modelo (1-4):",
        "1: Red Neural: SkLearn",
        "2: Modelo 2",
        "3: Modelo 3",
        "4: Modelo 4"
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
                        modelo2()                   # Iniciar Modelo 2:
                        modelo = 2                  # Actualizar la variable modelo
                        seleccionando = False       # Salir del bucle
                        menu_activo = False         # Cerrar el menú
                    elif num_option == 2:
                        graficar(2)                 # Graficar Modelo 2
                        seleccionando = False       # Salir del bucle
                        menu_activo = False         # Cerrar el menú
                elif evento.key == pygame.K_3:
                    if num_option == 1:
                        modelo3()                   # Iniciar Modelo 3:
                        modelo = 3                  # Actualizar la variable modelo
                        seleccionando = False       # Salir del bucle
                        menu_activo = False         # Cerrar el menú
                    elif num_option == 2:
                        graficar(3)                 # Graficar Modelo 3
                        seleccionando = False       # Salir del bucle
                        menu_activo = False         # Cerrar el menú
                elif evento.key == pygame.K_4:
                    if num_option == 1:
                        modelo4()                   # Iniciar Modelo 4:
                        modelo = 4                  # Actualizar la variable modelo
                        seleccionando = False       # Salir del bucle
                        menu_activo = False         # Cerrar el menú
                    elif num_option == 2:
                        graficar(4)                 # Graficar Modelo 4
                        seleccionando = False       # Salir del bucle
                        menu_activo = False         # Cerrar el menú                       # Volver al menú principal después de seleccionar

def preguntar_sobrescribir_modelo():
    global datos_modelo
    pantalla.fill(NEGRO)
    
    # Textos a mostrar
    textos = [
        "¿Quieres sobrescribir algún modelo?",
        "1: Red Neural: SkLearn",
        "2: Modelo 2",
        "3: Modelo 3",
        "4: Modelo 4",
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

def sobrescribir_modelo(modelo_num):
    global datos_modelo
    
    switcher = {
        1: 'RedNeural',
        2: 'Modelo2',
        3: 'Modelo3',
        4: 'Modelo4'
    }
    
    modelo = switcher.get(modelo_num, 'Modelo Desconocido')
    model_filename = f'./Models/{modelo}.joblib'
    data_filename = f'./Models/Data/{modelo}.csv'
    
    # El archivo existe? borralo
    if os.path.exists(model_filename):
        os.remove(model_filename)
        print(f"Modelo {modelo} borrado.")
    
    # El archivo existe? borralo
    if os.path.exists(data_filename):
        os.remove(data_filename)
        print(f"DataSet {modelo} borrado.")

    match modelo_num:
        case 1:
            # Modelo 1: Red Neuronal SkLearn
            enRedNeural()
            datos_modelo.clear()  # Limpiar los datos después de sobrescribir
        case 2:
            # Modelo 2:
            modelo2()
            print("Modelo 2: No implementado")
            datos_modelo.clear()  # Limpiar los datos después de sobrescribir
        case 3:
            # Modelo 3:
            modelo3()
            print("Modelo 3: No implementado")
            datos_modelo.clear()  # Limpiar los datos después de sobrescribir
        case 4:
            # Modelo 4:
            modelo4()
            print("Modelo 4: No implementado")
            datos_modelo.clear()  # Limpiar los datos después de sobrescribir
        case _:  
            # Default
            print("Modelo Desconocido")
            datos_modelo.clear()  # Limpiar los datos después de sobrescribir

def graficar(num_modelo):
    switcher = {
        1: 'RedNeural',
        2: 'Modelo2',
        3: 'Modelo3',
        4: 'Modelo4'
    }

    modelo = switcher.get(num_modelo, 'Modelo Desconocido')
    data_filename = f'./Models/Data/{modelo}.csv'
    
    python_path = '../.venv/Scripts/python.exe'

    # Ejecutar grafica.py con la ruta del archivo como argumento
    subprocess.run([python_path, './grafica.py', data_filename])
    mostrar_menu() # Volver al menu principal después de graficar

# --------------------------------------------------------------------------------------------------------------------------------
# Modelo 1: Red Neuronal usando SkLearn
def enRedNeural():
    global nnNetwork, modelo
    # Nombre del  modelo
    model_filename = './Models/RedNeural.joblib'
    # Nombre del archivo CSV
    data_filename = './Models/Data/RedNeural.csv'
    
    if os.path.exists(model_filename):
        # Cargar el modelo si ya existe
        nnNetwork = load(model_filename)
        print("Modelo cargado.")
    else:
        # Entrenar un nuevo modelo si no existe
        X = np.array([dato['input'] for dato in datos_modelo])  # Entradas
        y = np.array([dato['output'] for dato in datos_modelo])  # Salidas
        
        # Crear y entrenar la red neuronal
        nnNetwork = MLPClassifier(
            hidden_layer_sizes=(10,),  # Una capa oculta con 15 neuronas
            activation='relu',         # Función de activación ReLU
            learning_rate_init=0.01,   # Tasa de aprendizaje
            max_iter=40000,            # Número máximo de iteraciones
            random_state=42            # Semilla para reproducibilidad
        )

        nnNetwork.fit(X, y)                 # Entrenar el modelo
        dump(nnNetwork, model_filename)     # Guardar el modelo entrenado
        print("Modelo entrenado y guardado.")
        # Guardar los datos de entrenamiento en un CSV
        datos_csv = {
            'Distancia': [dato['input'][0] for dato in datos_modelo],
            'Velocidad': [dato['input'][1] for dato in datos_modelo],
            'Salto': [dato['output'][0] for dato in datos_modelo]
        }
        
        df = pd.DataFrame(datos_csv)
        df.to_csv(data_filename, index=False)
        print(f"Datos de entrenamiento guardados en {data_filename}.")

def predecirConRedNeuronal(param_entrada):
    global nnNetwork
    
    if nnNetwork is None:
        print(f"Error: El modelo no está cargado.")
        return False

    nnSalida = nnNetwork.predict_proba([param_entrada])[0][1]
    salto = round(nnSalida * 100, 2)
    if nnSalida > 0.8:
        print("Entrada:", param_entrada)
        print(f"Valor de salida: {salto}%")
    return nnSalida >= 0.8  # Probabilidad mayor o igual a 80% para saltar
# --------------------------------------------------------------------------------------------------------------------------------
# Modelo 2:
def modelo2():
    print("Modelo 2: No implementado")
# --------------------------------------------------------------------------------------------------------------------------------
# Modelo 3:
def modelo3():
    print("Modelo 3: No implementado")
# --------------------------------------------------------------------------------------------------------------------------------
# Modelo 4:
def modelo4():
    print("Modelo 4: No implementado")
# --------------------------------------------------------------------------------------------------------------------------------
def update():
    global bala, velocidad_bala, current_frame, frame_count, current_frame_fondo, frame_count_fondo, current_frame_nave, frame_count_nave

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

    # Si la bala sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()

    # Dibujar el jugador con la animación (ENCIMA DEL FONDO)
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))
    # pygame.draw.rect(pantalla, (0, 255, 0), jugador, 2)                 # Dibujar hitbox del jugador en verde
    
    # Dibujar la bala (ENCIMA DEL FONDO)
    pantalla.blit(bala_img, (bala.x, bala.y))
    # pygame.draw.rect(pantalla, (0, 255, 0), bala, 2)                    # Dibujar hitbox de la bala en verde
    
    # Dibujar la nave con la animación (ENCIMA DEL FONDO)
    pantalla.blit(nave_frames[current_frame_nave], (nave.x, nave.y))
    # pygame.draw.rect(pantalla, (0, 255, 0), nave, 2)                    # Dibujar hitbox de la nave en verde

    # Colisión entre la bala y el jugador
    if jugador.colliderect(bala):
        pygame.mixer.music.pause()      # Pausar la música
        print("Colisión detectada!")
        reiniciar_juego()               # Terminar el juego y mostrar el menú

def main():
    global salto, en_suelo, bala_disparada, modelo

    reloj = pygame.time.Clock()
    mostrar_menu()                  # Mostrar el menú al inicio
    pygame.mixer.music.play(-1)     # Reproducir música de fondo en bucle
    correr = True

    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                # Detectar la tecla espacio para saltar
                if evento.key == pygame.K_SPACE and en_suelo and not pausa:
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_p:    # Presiona 'p' para pausar el juego
                    pausa_juego()
                if evento.key == pygame.K_q:    # Presiona 'q' para terminar el juego
                    pygame.mixer.music.stop()   # Detener la música
                    pygame.quit()
                    exit()

        if not pausa:
            # Modo manual: el jugador controla el salto
            if not modo_auto:
                if salto:
                    manejar_salto()
                # Guardar los datos si estamos en modo manual
                guardar_datos()
            # Modo automático: el modelo decide si saltar o no
            if modo_auto:
                
                match modelo:
                    case 1:
                        # Modo automático: Red Neuronal
                        if not salto:
                            salto = predecirConRedNeuronal([abs(jugador.x - bala.x), velocidad_bala])
                        if salto:
                            manejar_salto()
                    case 2:
                        # Modo automático: Modelo 2
                        print("Modelo 2: No implementado")
                        # if not salto:
                        #     salto = 
                        # if salto:
                        #     manejar_salto()
                    case 3:
                        # Modo automático: Modelo 3
                        print("Modelo 3: No implementado")
                        # if not salto:
                        #     salto = 
                        # if salto:
                        #     manejar_salto()
                    case 4:
                        # Modo automático: Modelo 4
                        print("Modelo 4: No implementado")
                        # if not salto:
                        #     salto = 
                        # if salto:
                        #     manejar_salto()
                    case _:
                        print("Ningún modelo seleccionado.")

            # Actualizar el juego
            if not bala_disparada:
                disparar_bala()
                print(f"Velocidad Bala: {velocidad_bala}%")
            update()
        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(90)  # Limitar el juego a 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
