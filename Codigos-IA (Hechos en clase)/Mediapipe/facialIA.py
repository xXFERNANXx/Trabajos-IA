import cv2
import mediapipe as mp
import numpy as np
import os
import json
from collections import defaultdict

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=2, 
                                min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Captura de video
cap = cv2.VideoCapture(0)

# Lista de índices de landmarks específicos
eyebrow_points_izq_sup = [70, 63, 105, 66, 107]
eyebrow_points_izq_inf = [46, 53, 52, 65, 55]
eyebrow_points_der_sup = [336, 296, 334, 293, 300]
eyebrow_points_der_inf = [285, 295, 282, 283, 276]
eye_points_izq_ext = [33, 246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 7]
eye_points_der_ext = [362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382]
mouth_points_sup = [0, 267, 269, 270, 409, 291, 375, 321, 405, 314, 17, 84, 181, 91, 146, 61, 185, 40, 39, 37]
mouth_points_inf = [13, 312, 311, 310, 415, 306, 324, 318, 402, 317, 14, 87, 178, 88, 95, 78, 191, 80, 81, 82]
face_points = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]

# Archivo para guardar los rostros conocidos
DATABASE_FILE = "facial_database.json"

# Variable global para almacenar los puntos del rostro a registrar
rostro_a_registrar = None

def distancia(p1, p2):
    """Calcula la distancia euclidiana entre dos puntos."""
    return np.linalg.norm(np.array(p1) - np.array(p2))

def calcular_distancias_faciales(puntos, normalizar=True):
    """Calcula todas las distancias relevantes entre puntos faciales."""
    distancias = {}
    
    # Distancia base para normalización (distancia entre ojos)
    if len(puntos['ojo_izq_ext']) > 0 and len(puntos['ojo_der_ext']) > 0:
        dist_base = distancia(puntos['ojo_izq_ext'][0][1], puntos['ojo_der_ext'][0][1])
        distancias['dist_entre_ojos'] = dist_base
    else:
        dist_base = 1  # Evitar división por cero
    
    # Distancias en cejas (normalizadas)
    for i in range(len(puntos['ceja_izq_sup']) - 1):
        dist = distancia(puntos['ceja_izq_sup'][i][1], puntos['ceja_izq_sup'][i+1][1])
        distancias[f'ceja_izq_sup_{i}'] = dist / dist_base if normalizar else dist
    
    for i in range(len(puntos['ceja_der_sup']) - 1):
        dist = distancia(puntos['ceja_der_sup'][i][1], puntos['ceja_der_sup'][i+1][1])
        distancias[f'ceja_der_sup_{i}'] = dist / dist_base if normalizar else dist
    
    # Distancias en boca (normalizadas)
    if len(puntos['boca_sup']) > 1 and len(puntos['boca_inf']) > 1:
        ancho_boca = distancia(puntos['boca_sup'][0][1], puntos['boca_sup'][-1][1])
        altura_boca = distancia(puntos['boca_sup'][len(puntos['boca_sup'])//2][1], 
                                puntos['boca_inf'][len(puntos['boca_inf'])//2][1])
        distancias['ancho_boca'] = ancho_boca / dist_base if normalizar else ancho_boca
        distancias['altura_boca'] = altura_boca / dist_base if normalizar else altura_boca
    
    # Distancias en cara (normalizadas)
    if len(puntos['cara']) > 3:
        ancho_cara = distancia(puntos['cara'][0][1], puntos['cara'][1][1])
        largo_cara = distancia(puntos['cara'][2][1], puntos['cara'][3][1])
        distancias['ancho_cara'] = ancho_cara / dist_base if normalizar else ancho_cara
        distancias['largo_cara'] = largo_cara / dist_base if normalizar else largo_cara
    
    return distancias

def cargar_database():
    """Carga la base de datos de rostros conocidos."""
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as f:
            return json.load(f)
    return {}

def guardar_database(database):
    """Guarda la base de datos de rostros conocidos."""
    with open(DATABASE_FILE, 'w') as f:
        json.dump(database, f, indent=4)

def comparar_rostro(distancias_actual, database, umbral=0.15):
    """Compara un rostro con la base de datos y devuelve (nombre, diferencia) si coincide."""
    mejor_coincidencia = None
    mejor_diferencia = float('inf')
    
    for nombre, datos in database.items():
        diferencia_total = 0
        coincidencias = 0
        
        for clave, valor in distancias_actual.items():
            if clave in datos['distancias']:
                # Usamos diferencia porcentual normalizada
                diferencia = abs(valor - datos['distancias'][clave]) / datos['distancias'][clave]
                diferencia_total += diferencia
                coincidencias += 1
        
        if coincidencias > 0:
            diferencia_promedio = diferencia_total / coincidencias
            if diferencia_promedio < mejor_diferencia and diferencia_promedio < umbral:
                mejor_diferencia = diferencia_promedio
                mejor_coincidencia = (nombre, diferencia_promedio)
    
    return mejor_coincidencia if mejor_coincidencia else ("Desconocido", 1.0)

# Cargar base de datos al inicio
facial_database = cargar_database()
modo_registro = False
nombre_nuevo_rostro = ""

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    # Lista para almacenar información de cada rostro detectado
    rostros_detectados = []
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            puntos = defaultdict(list)
            
            # Recopilar puntos para cada sección
            secciones = {
                'ceja_izq_sup': eyebrow_points_izq_sup,
                'ceja_izq_inf': eyebrow_points_izq_inf,
                'ceja_der_sup': eyebrow_points_der_sup,
                'ceja_der_inf': eyebrow_points_der_inf,
                'ojo_izq_ext': eye_points_izq_ext,
                'ojo_der_ext': eye_points_der_ext,
                'boca_sup': mouth_points_sup,
                'boca_inf': mouth_points_inf,
                'cara': face_points
            }
            
            # Calcular el centro del rostro para posicionar el nombre
            puntos_cara = []
            for idx in face_points:
                landmark = face_landmarks.landmark[idx]
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                puntos_cara.append((x, y))
            
            # Calcular el rectángulo del rostro
            if puntos_cara:
                x_coords = [p[0] for p in puntos_cara]
                y_coords = [p[1] for p in puntos_cara]
                x_min, x_max = min(x_coords), max(x_coords)
                y_min, y_max = min(y_coords), max(y_coords)
                centro_x = (x_min + x_max) // 2
                centro_y = y_min - 20  # 20 píxeles arriba del rostro
                
                for seccion, indices in secciones.items():
                    for idx in indices:
                        try:
                            x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                            y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                            puntos[seccion].append((idx, (x, y)))
                            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
                        except:
                            continue
                
                # Calcular distancias faciales normalizadas
                if len(puntos['ojo_izq_ext']) > 0 and len(puntos['ojo_der_ext']) > 0:
                    distancias_actual = calcular_distancias_faciales(puntos)
                    
                    # Comparar con la base de datos
                    if not modo_registro:
                        nombre_persona, diferencia = comparar_rostro(distancias_actual, facial_database)
                        confianza = (1 - diferencia) * 100
                        rostros_detectados.append((nombre_persona, confianza, (centro_x, centro_y)))
                
                # Dibujar líneas entre puntos
                for seccion in puntos:
                    color = (0, 255, 0)  # Verde por defecto
                    if 'ceja' in seccion: color = (255, 0, 0)
                    elif 'ojo' in seccion: color = (0, 255, 255)
                    elif 'boca' in seccion: color = (0, 0, 255)
                    
                    for i in range(len(puntos[seccion]) - 1):
                        cv2.line(frame, puntos[seccion][i][1], puntos[seccion][i+1][1], color, 1)
                
                # Si estamos en modo registro, guardamos los puntos del primer rostro detectado
                if modo_registro and rostro_a_registrar is None:
                    rostro_a_registrar = puntos
    
    # Mostrar nombres sobre los rostros detectados (máximo 2)
    for i, (nombre, confianza, (x, y)) in enumerate(rostros_detectados[:2]):
        color = (0, 255, 0) if nombre != "Desconocido" else (0, 0, 255)
        cv2.putText(frame, nombre, (x - 50, y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        if nombre != "Desconocido":
            cv2.putText(frame, f"{confianza:.1f}%", (x - 30, y + 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    
    # Modo registro de nuevo rostro
    if modo_registro:
        if rostros_detectados:
            centro_x, centro_y = rostros_detectados[0][2]
            cv2.putText(frame, f"Registrando: {nombre_nuevo_rostro}", 
                        (centro_x - 100, centro_y - 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "ENTER: Confirmar  ESC: Cancelar", 
                        (centro_x - 100, centro_y - 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
        else:
            cv2.putText(frame, "No se detectó rostro para registrar", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    cv2.imshow('Reconocimiento Facial', frame)
    
    key = cv2.waitKey(1)
    
    if key == ord('q'):
        break
    elif key == 32:  # Tecla ESPACIO para registrar nuevo rostro
        modo_registro = True
        nombre_nuevo_rostro = input("Ingrese el nombre de la persona: ")
        # Reiniciamos la variable de rostro a registrar
        rostro_a_registrar = None
    elif key == 13 and modo_registro and rostro_a_registrar is not None:  # ENTER para confirmar
        # Guardar el rostro detectado previamente
        distancias_actual = calcular_distancias_faciales(rostro_a_registrar)
        facial_database[nombre_nuevo_rostro] = {
            'distancias': distancias_actual,
            'timestamp': str(np.datetime64('now'))
        }
        guardar_database(facial_database)
        modo_registro = False
        rostro_a_registrar = None
        print(f"Rostro de {nombre_nuevo_rostro} registrado exitosamente!")
    elif key == 27:  # ESC para cancelar registro
        modo_registro = False
        rostro_a_registrar = None

cap.release()
cv2.destroyAllWindows()