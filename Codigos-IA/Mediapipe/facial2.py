import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.7)

# Cargar la máscara con transparencia (debe ser un PNG con canal alpha)
mask = cv2.imread("./Mascara-PNG-Isolated-Photos.png", cv2.IMREAD_UNCHANGED)

# Función para superponer la máscara en la cara
def overlay_mask(frame, mask, x, y, w, h):
    # Redimensionar la máscara al tamaño de la cara detectada
    mask_resized = cv2.resize(mask, (w, h))

    # Extraer los canales de la máscara (RGBA)
    mask_rgb = mask_resized[:, :, :3]  # Canales de color
    mask_alpha = mask_resized[:, :, 3] / 255.0  # Canal de transparencia

    # Obtener la región donde se colocará la máscara
    roi = frame[y:y+h, x:x+w]

    # Mezclar la máscara con el frame
    for c in range(3):  # Aplicar a cada canal de color (BGR)
        roi[:, :, c] = (1 - mask_alpha) * roi[:, :, c] + mask_alpha * mask_rgb[:, :, c]

    frame[y:y+h, x:x+w] = roi  # Colocar la máscara en el frame

# Captura de video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Espejo para mejor experiencia
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)

    if results.detections:
        for detection in results.detections:
            # Obtener la caja delimitadora del rostro
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape  # Alto y ancho del frame

            # Convertir a coordenadas de píxeles
            x = int(bboxC.xmin * iw) - 20
            y = int(bboxC.ymin * ih) - 80
            w = int(bboxC.width * iw) + 40
            h = int(bboxC.height * ih) + 40

            # Superponer la máscara en la imagen
            overlay_mask(frame, mask, x, y, w, h)

    cv2.imshow("Mascara Animada", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()