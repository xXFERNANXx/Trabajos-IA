import cv2 as cv
import numpy as np

# Cargar la Imagen
img = cv.imread("./Manzanos.jpg", 1)
# Convertir a HSV (Hue, Saturation, Value)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# Umbrales para detectar el color rojo Valores altos significa Puros
# Umbrales Bajos
ub = np.array([0, 40, 40])
# Umbrales Altos
ua = np.array([10, 255, 255])
# Umbrales Bajos 2
ua1 = np.array([170, 40, 40])
# Umbrales Altos 2
ub1 = np.array([180, 255, 255])

# Crear la mascaras
mask1 = cv.inRange(hsv, ub, ua)
mask2 = cv.inRange(hsv, ub1, ua1)

# Unir las mascaras
mask = mask1 + mask2

# Aplicar la mascara a la imagen original
res = cv.bitwise_and(img, img, mask=mask)

#Mostrar las imagen
cv.imshow("RES", res)
cv.imshow("HSV", hsv)
cv.imshow("Mask", mask)
cv.imshow("Original", img)

cv.waitKey(0)
cv.destroyAllWindows()