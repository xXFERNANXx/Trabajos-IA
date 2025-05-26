import cv2
import mediapipe as mp
import numpy as np
import os
import json
from collections import defaultdict
from scipy.spatial import distance
from sklearn.metrics.pairwise import cosine_similarity

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=2,
    refine_landmarks=True,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Captura de video
cap = cv2.VideoCapture(0)

# Puntos clave optimizados
KEY_POINTS = {
    'frente': [10, 151, 9, 8],
    'ojos_izq': [33, 133, 144, 145, 153, 154],
    'ojos_der': [362, 263, 373, 374, 380, 381],
    'nariz': [1, 4, 5, 6],
    'boca': [61, 185, 40, 39, 37, 267, 269, 270, 291, 409],
    'mandibula': [172, 136, 150, 149, 176, 148, 152]
}

DATABASE_FILE = "facial_database_v4.json"

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def extraer_caracteristicas(landmarks, frame_shape):
    """Extrae características faciales optimizadas."""
    puntos = {}
    for region, indices in KEY_POINTS.items():
        puntos[region] = []
        for idx in indices:
            landmark = landmarks.landmark[idx]
            puntos[region].append([landmark.x * frame_shape[1], 
                                 landmark.y * frame_shape[0], 
                                 landmark.z])
        puntos[region] = np.array(puntos[region])
    
    # Calcular distancias clave
    distancias = {}
    
    # Distancia entre ojos (normalizador)
    centro_ojo_izq = np.mean(puntos['ojos_izq'], axis=0)
    centro_ojo_der = np.mean(puntos['ojos_der'], axis=0)
    dist_ojos = distance.euclidean(centro_ojo_izq[:2], centro_ojo_der[:2])
    
    # Proporciones faciales
    frente = np.mean(puntos['frente'], axis=0)
    barbilla = np.mean(puntos['mandibula'][-3:], axis=0)
    distancias['altura_facial'] = distance.euclidean(frente[:2], barbilla[:2]) / dist_ojos
    
    # Ancho facial
    distancias['ancho_facial'] = distance.euclidean(
        puntos['ojos_izq'][0][:2], puntos['ojos_der'][0][:2]) / dist_ojos
    
    # Relación ojos-boca
    centro_boca = np.mean(puntos['boca'][:8], axis=0)
    distancias['ojos_boca'] = distance.euclidean(centro_ojo_izq[:2], centro_boca[:2]) / dist_ojos
    
    # Ángulo facial
    vec_nariz = np.mean(puntos['nariz'][:2], axis=0) - np.mean(puntos['nariz'][2:], axis=0)
    vec_frente_barbilla = frente - barbilla
    distancias['angulo_nariz'] = np.degrees(np.arccos(
        np.dot(vec_nariz[:2], vec_frente_barbilla[:2]) / 
        (np.linalg.norm(vec_nariz[:2]) * np.linalg.norm(vec_frente_barbilla[:2]))))
    
    # Crear vector de características
    vector_caracteristicas = {
        'distancias': np.array(list(distancias.values())),
        'puntos_clave': {k: v[:, :2].tolist() for k, v in puntos.items()},  # Solo coordenadas x,y
        'dist_normalizacion': dist_ojos
    }
    
    return vector_caracteristicas

def calcular_similitud(vec1, vec2):
    """Calcula similitud entre vectores de características."""
    # Comparar distancias normalizadas
    sim_distancias = 1 - distance.cosine(
        vec1['distancias'], 
        vec2['distancias']
    )
    
    # Comparar puntos clave
    puntos1 = np.array([p for region in ['ojos_izq', 'ojos_der', 'boca'] 
                       for p in vec1['puntos_clave'][region]]).flatten()
    puntos2 = np.array([p for region in ['ojos_izq', 'ojos_der', 'boca'] 
                       for p in vec2['puntos_clave'][region]]).flatten()
    
    sim_puntos = 1 - distance.cosine(puntos1, puntos2)
    
    return 0.7 * sim_distancias + 0.3 * sim_puntos

def cargar_database():
    """Carga la base de datos de rostros conocidos."""
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as f:
            return json.load(f)
    return {}

def guardar_database(database):
    """Guarda la base de datos de rostros conocidos."""
    with open(DATABASE_FILE, 'w') as f:
        json.dump(database, f, indent=4, cls=NumpyEncoder)

def comparar_rostro(vec_actual, database, umbral=0.85):
    """Compara un rostro con la base de datos."""
    mejor_coincidencia = None
    mejor_similitud = -1
    
    for nombre, datos in database.items():
        similitud = calcular_similitud(vec_actual, datos['vector'])
        
        if similitud > mejor_similitud and similitud > umbral:
            mejor_similitud = similitud
            mejor_coincidencia = (nombre, mejor_similitud)
    
    return mejor_coincidencia if mejor_coincidencia else ("Desconocido", 0)

# Cargar base de datos
facial_database = cargar_database()
modo_registro = False
nombre_nuevo_rostro = ""
rostro_a_registrar = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    rostros_detectados = []
    
    if results.multi_face_landmarks:
        for face_id, face_landmarks in enumerate(results.multi_face_landmarks):
            # Extraer características
            vec_caracteristicas = extraer_caracteristicas(face_landmarks, frame.shape)
            
            # Calcular posición para mostrar nombre (CORRECCIÓN DEL ERROR)
            puntos = vec_caracteristicas['puntos_clave']
            puntos_combined = puntos['frente'] + puntos['mandibula']
            centro_x = int(np.mean([p[0] for p in puntos_combined]))
            centro_y = int(np.min([p[1] for p in puntos['frente']])) - 30
            
            # Comparar con base de datos
            if not modo_registro:
                nombre, confianza = comparar_rostro(vec_caracteristicas, facial_database)
                rostros_detectados.append((nombre, confianza, (centro_x, centro_y), face_id))
            
            # Guardar para registro si es necesario
            if modo_registro and rostro_a_registrar is None and face_id == 0:
                rostro_a_registrar = vec_caracteristicas
            
            # Visualización
            for region in ['ojos_izq', 'ojos_der', 'boca']:
                for punto in puntos[region]:
                    cv2.circle(frame, (int(punto[0]), int(punto[1])), 2, (0, 255, 0), -1)
    
    # Mostrar resultados
    for nombre, confianza, (x, y), _ in rostros_detectados[:2]:
        color = (0, 255, 0) if nombre != "Desconocido" else (0, 0, 255)
        cv2.putText(frame, f"{nombre} ({confianza*100:.1f}%)", (x-100, y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    # Interfaz de registro
    if modo_registro:
        if rostros_detectados:
            x, y = rostros_detectados[0][2]
            cv2.putText(frame, f"Registrando: {nombre_nuevo_rostro}", (x-100, y-50),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "ENTER: Confirmar  ESC: Cancelar", (x-100, y-80),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
        else:
            cv2.putText(frame, "No se detectó rostro para registrar", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    cv2.imshow('Reconocimiento Facial Avanzado', frame)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == 32:  # Espacio para registrar
        modo_registro = True
        nombre_nuevo_rostro = input("Ingrese el nombre de la persona: ")
        rostro_a_registrar = None
    elif key == 13 and modo_registro and rostro_a_registrar:  # Enter para confirmar
        facial_database[nombre_nuevo_rostro] = {
            'vector': rostro_a_registrar,
            'timestamp': str(np.datetime64('now'))
        }
        guardar_database(facial_database)
        modo_registro = False
        print(f"Rostro de {nombre_nuevo_rostro} registrado exitosamente!")
    elif key == 27:  # ESC para cancelar
        modo_registro = False

cap.release()
cv2.destroyAllWindows()