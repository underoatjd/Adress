import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model  # type: ignore

# Cargar el modelo entrenado
model = load_model("modelo_ocr.keras")

# Ruta a las imágenes de prueba
test_image_folder = 'C:/python/RENOVAR FINANCIERA SELENIUM/ADRES/imagentest'

# Función para mejorar la imagen (el proceso de limpieza)
def mejorar_imagen(image):
    # Aplicar un filtro de mediana para reducir el ruido
    imagen_filtrada = cv2.medianBlur(image, 3)

    # Binarización adaptativa para mejorar la detección de caracteres
    binarizada = cv2.adaptiveThreshold(
        imagen_filtrada, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 11, 2
    )

    # Crear un kernel para operaciones morfológicas
    kernel = np.ones((2, 2), np.uint8)

    # Aplicar apertura para eliminar puntos de ruido
    apertura = cv2.morphologyEx(binarizada, cv2.MORPH_OPEN, kernel, iterations=2)

    # Cierre para reforzar los caracteres
    cierre = cv2.morphologyEx(apertura, cv2.MORPH_CLOSE, kernel, iterations=1)

    # Remover pequeños componentes conectados que no sean caracteres
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(cierre, connectivity=8)
    areas_min = 50  # Ajustar según la imagen

    # Crear una máscara para mantener solo componentes más grandes que el umbral
    mascara = np.zeros(cierre.shape, dtype=np.uint8)
    for i in range(1, num_labels):  # Ignoramos el fondo (etiqueta 0)
        if stats[i, cv2.CC_STAT_AREA] >= areas_min:
            mascara[labels == i] = 255

    # Invertir colores si es necesario
    resultado = cv2.bitwise_not(mascara)

    return resultado

# Función para preprocesar imágenes antes de pasar al modelo
def preprocess_image(image):
    IMG_WIDTH = 128
    IMG_HEIGHT = 64
    image_resized = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
    image_normalized = image_resized / 255.0
    return image_normalized

# Obtener lista de archivos de imágenes de prueba
test_image_files = os.listdir(test_image_folder)

# Probar cada imagen
for filename in test_image_files:
    # Cargar la imagen en escala de grises
    test_image_path = os.path.join(test_image_folder, filename)
    test_image = cv2.imread(test_image_path, cv2.IMREAD_GRAYSCALE)
    
    # Aplicar la mejora de la imagen
    test_image_mejorada = mejorar_imagen(test_image)
    
    # Preprocesar la imagen para el modelo
    test_image_preprocessed = preprocess_image(test_image_mejorada)
    test_image_preprocessed = test_image_preprocessed.reshape(1, 64, 128, 1)  # (batch_size, height, width, channels)
    
    # Hacer la predicción
    predictions = model.predict(test_image_preprocessed)
    
    # Convertir predicciones a dígitos
    predicted_digits = [np.argmax(predictions[0][i]) for i in range(5)]
    
    print(f"Predicción para {filename}: {predicted_digits}")
