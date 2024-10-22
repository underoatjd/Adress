import os
import cv2
import numpy as np

def mejorar_imagen(input_path, output_path):
    # Cargar la imagen en escala de grises
    imagen = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    # Aplicar un filtro de mediana para reducir el ruido
    imagen_filtrada = cv2.medianBlur(imagen, 3)

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

    # Invertir colores (si necesario)
    resultado = cv2.bitwise_not(mascara)

    # Guardar la imagen procesada
    cv2.imwrite(output_path, resultado)


def procesar_imagenes(carpeta_input, carpeta_output):
    # Asegurarse de que la carpeta de salida existe
    if not os.path.exists(carpeta_output):
        os.makedirs(carpeta_output)

    # Recorrer todas las imágenes en la carpeta de entrada
    for nombre_imagen in os.listdir(carpeta_input):
        # Crear la ruta completa de la imagen de entrada
        input_path = os.path.join(carpeta_input, nombre_imagen)

        # Crear la ruta completa de la imagen de salida con el mismo nombre
        output_path = os.path.join(carpeta_output, nombre_imagen)

        # Procesar la imagen
        mejorar_imagen(input_path, output_path)

        print(f"Imagen {nombre_imagen} procesada y guardada en {output_path}")


# Uso del script
carpeta_input = "C:/python/RENOVAR FINANCIERA SELENIUM/ADRES/images"
carpeta_output = "C:/python/RENOVAR FINANCIERA SELENIUM/ADRES/images prepro"

procesar_imagenes(carpeta_input, carpeta_output)