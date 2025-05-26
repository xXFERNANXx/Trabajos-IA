import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=2, 
                                min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Captura de video
cap = cv2.VideoCapture(0)

# Lista de índices de landmarks específicos (ojos y boca)
# Ceja izquierda (superior e inferior)
eyebrow_points_izq_sup = [70, 63, 105, 66, 107]
eyebrow_points_izq_inf = [46, 53, 52, 65, 55]
# Ceja derecha (superior e inferior)
eyebrow_points_der_sup = [336, 296, 334, 293, 300]
eyebrow_points_der_inf = [285, 295, 282, 283, 276]
# Ojo izquierdo (contorno exterior e interior)
eye_points_izq_ext = [33, 246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 7]
eye_points_izq_int = [362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382]
# Ojo derecho (contorno exterior e interior)
eye_points_der_ext = [362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382]
eye_points_der_int = [33, 246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 7]
# Boca (contorno superior e inferior)
mouth_points_sup = [0, 267, 269, 270, 409, 291, 375, 321, 405, 314, 17, 84, 181, 91, 146, 61, 185, 40, 39, 37]
mouth_points_inf = [13, 312, 311, 310, 415, 306, 324, 318, 402, 317, 14, 87, 178, 88, 95, 78, 191, 80, 81, 82]
# Cara (contorno principal)
face_points = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]

def distancia(p1, p2):
    """Calcula la distancia euclidiana entre dos puntos."""
    return np.linalg.norm(np.array(p1) - np.array(p2))

def dibujar_lineas_y_calcular_distancias(frame, puntos, color, cerrar_contorno=True):
    """Dibuja líneas entre puntos y calcula distancias."""
    distancias = []
    n = len(puntos)
    
    if n < 2:
        return distancias
    
    # Dibujar líneas entre puntos consecutivos
    for i in range(n - 1):
        cv2.line(frame, puntos[i][1], puntos[i+1][1], color, 1)
        dist = distancia(puntos[i][1], puntos[i+1][1])
        distancias.append(dist)
        # Mostrar distancia en el punto medio
        punto_medio = ((puntos[i][1][0] + puntos[i+1][1][0]) // 2, 
                       (puntos[i][1][1] + puntos[i+1][1][1]) // 2)
        cv2.putText(frame, f"{dist:.1f}", punto_medio, 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, color, 1)
    
    # Cerrar el contorno si es necesario
    if cerrar_contorno and n > 2:
        cv2.line(frame, puntos[-1][1], puntos[0][1], color, 1)
        dist = distancia(puntos[-1][1], puntos[0][1])
        distancias.append(dist)
        punto_medio = ((puntos[-1][1][0] + puntos[0][1][0]) // 2, 
                       (puntos[-1][1][1] + puntos[0][1][1]) // 2)
        cv2.putText(frame, f"{dist:.1f}", punto_medio, 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, color, 1)
    
    return distancias

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Espejo para mayor naturalidad
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Diccionarios para almacenar puntos
            puntos = {
                'ceja_izq_sup': [],
                'ceja_izq_inf': [],
                'ceja_der_sup': [],
                'ceja_der_inf': [],
                'ojo_izq_ext': [],
                'ojo_izq_int': [],
                'ojo_der_ext': [],
                'ojo_der_int': [],
                'boca_sup': [],
                'boca_inf': [],
                'cara': []
            }
            
            # Recopilar puntos para cada sección
            for idx in eyebrow_points_izq_sup:
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos['ceja_izq_sup'].append((idx, (x, y)))
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            for idx in eyebrow_points_izq_inf:
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos['ceja_izq_inf'].append((idx, (x, y)))
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            for idx in eyebrow_points_der_sup:
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos['ceja_der_sup'].append((idx, (x, y)))
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            for idx in eyebrow_points_der_inf:
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos['ceja_der_inf'].append((idx, (x, y)))
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            for idx in eye_points_izq_ext:
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos['ojo_izq_ext'].append((idx, (x, y)))
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            for idx in eye_points_izq_int:
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos['ojo_izq_int'].append((idx, (x, y)))
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            for idx in eye_points_der_ext:
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos['ojo_der_ext'].append((idx, (x, y)))
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            for idx in eye_points_der_int:
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos['ojo_der_int'].append((idx, (x, y)))
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            for idx in mouth_points_sup:
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos['boca_sup'].append((idx, (x, y)))
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            for idx in mouth_points_inf:
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos['boca_inf'].append((idx, (x, y)))
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            for idx in face_points:
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos['cara'].append((idx, (x, y)))
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # Dibujar líneas y calcular distancias para cada sección
            distancias = {}
            
            # Cejas (color azul)
            distancias['ceja_izq_sup'] = dibujar_lineas_y_calcular_distancias(frame, puntos['ceja_izq_sup'], (255, 0, 0))
            distancias['ceja_izq_inf'] = dibujar_lineas_y_calcular_distancias(frame, puntos['ceja_izq_inf'], (255, 0, 0))
            distancias['ceja_der_sup'] = dibujar_lineas_y_calcular_distancias(frame, puntos['ceja_der_sup'], (255, 0, 0))
            distancias['ceja_der_inf'] = dibujar_lineas_y_calcular_distancias(frame, puntos['ceja_der_inf'], (255, 0, 0))
            
            # Ojos (color amarillo)
            distancias['ojo_izq_ext'] = dibujar_lineas_y_calcular_distancias(frame, puntos['ojo_izq_ext'], (0, 255, 255), True)
            distancias['ojo_izq_int'] = dibujar_lineas_y_calcular_distancias(frame, puntos['ojo_izq_int'], (0, 255, 255), True)
            distancias['ojo_der_ext'] = dibujar_lineas_y_calcular_distancias(frame, puntos['ojo_der_ext'], (0, 255, 255), True)
            distancias['ojo_der_int'] = dibujar_lineas_y_calcular_distancias(frame, puntos['ojo_der_int'], (0, 255, 255), True)
            
            # Boca (color rojo)
            distancias['boca_sup'] = dibujar_lineas_y_calcular_distancias(frame, puntos['boca_sup'], (0, 0, 255))
            distancias['boca_inf'] = dibujar_lineas_y_calcular_distancias(frame, puntos['boca_inf'], (0, 0, 255))
            
            # Cara (color verde)
            distancias['cara'] = dibujar_lineas_y_calcular_distancias(frame, puntos['cara'], (0, 255, 0))
            
            # Mostrar algunas distancias clave en la pantalla
            cv2.putText(frame, f"Distancia entre ojos: {distancia(puntos['ojo_izq_ext'][0][1], puntos['ojo_der_ext'][0][1]):.1f}", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Aquí puedes guardar las distancias en un archivo o base de datos para análisis posterior
            # print(distancias)

    cv2.imshow('Analisis Facial con MediaPipe', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()