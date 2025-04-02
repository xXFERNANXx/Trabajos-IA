import cv2
import numpy as np

#Cargar imagen de la forma tradicional
img = cv2.imread("./Manzanos.jpg", 1) #ruta de la imagen
# imgn = np.zeros(img.shape[:2], np.uint8) #imagen
imgn = np.ones(img.shape[:2], np.uint8) #imagen

#division de la imagen en los 3 canales de color
print(img.shape)
b,g,r= cv2.split(img)
imgb = cv2.merge([b, imgn, imgn])
imgg = cv2.merge([imgn, b, imgn])
imgr = cv2.merge([imgn, imgn, r])
imgnn = cv2.merge([g, b, r])
# #Quitar color de la imagen y mostrar en escala de grises
# img2=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow('gris', img2)
# img3=cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #Se muestra en RGB
# cv2.imshow('RGB', img3)
# img4=cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #Se muestra en formato HSV
# cv2.imshow('HSV', img4)

cv2.imshow('salida1', b)
cv2.imshow('salida2', g)
cv2.imshow('salida3', r)
cv2.imshow('salida4', imgn)
cv2.imshow('salida5', imgnn)



cv2.waitKey(0)
cv2.destroyAllWindows()