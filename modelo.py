import cv2
import matplotlib.pyplot as plt

# Cargar la imagen desde la ruta absoluta
img_path = 'C:/python/RENOVAR FINANCIERA SELENIUM/ADRES/images/00084.png'
img = cv2.imread(img_path)

# Convertir a escala de grises
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Mostrar la imagen en escala de grises
plt.imshow(gray, cmap='gray')
plt.title('Escala de Grises')
plt.show()

# Aplicar filtro de desenfoque mediano
blurred = cv2.medianBlur(gray, 3)

# Mostrar la imagen suavizada
plt.imshow(blurred, cmap='gray')
plt.title('Imagen Suavizada')
plt.show()

# Umbralización binaria inversa
_, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY_INV)

# Mostrar la imagen umbralizada
plt.imshow(thresh, cmap='gray')
plt.title('Umbralización Binaria')
plt.show()

# Crear un kernel para operaciones morfológicas
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

# Aplicar operación de cierre para eliminar ruido
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# Mostrar la imagen con el ruido eliminado
plt.imshow(morph, cmap='gray')
plt.title('Morfología: Eliminación de Ruido')
plt.show()
