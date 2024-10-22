import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model  # type: ignore

# Definir una función para realizar todo el proceso de predicción OCR
def ocr_predict(test_image_folder: str, model_path: str = "modelo_ocr.keras") -> str:
    # Cargar el modelo entrenado
    model = load_model(model_path)

    # Función para mejorar la imagen (el proceso de limpieza)
    def mejorar_imagen(image):
        imagen_filtrada = cv2.medianBlur(image, 3)
        binarizada = cv2.adaptiveThreshold(
            imagen_filtrada, 255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        kernel = np.ones((2, 2), np.uint8)
        apertura = cv2.morphologyEx(binarizada, cv2.MORPH_OPEN, kernel, iterations=2)
        cierre = cv2.morphologyEx(apertura, cv2.MORPH_CLOSE, kernel, iterations=1)
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(cierre, connectivity=8)
        areas_min = 50
        mascara = np.zeros(cierre.shape, dtype=np.uint8)
        for i in range(1, num_labels):
            if stats[i, cv2.CC_STAT_AREA] >= areas_min:
                mascara[labels == i] = 255
        resultado = cv2.bitwise_not(mascara)
        return resultado

    # Función para preprocesar imágenes antes de pasar al modelo
    def preprocess_image(image):
        IMG_WIDTH = 128
        IMG_HEIGHT = 64
        image_resized = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
        image_normalized = image_resized / 255.0
        return image_normalized

    # Obtener el primer archivo de imagen en la carpeta
    test_image_files = os.listdir(test_image_folder)
    if len(test_image_files) > 0:
        test_image_path = os.path.join(test_image_folder, test_image_files[0])
        test_image = cv2.imread(test_image_path, cv2.IMREAD_GRAYSCALE)
        test_image_mejorada = mejorar_imagen(test_image)
        test_image_preprocessed = preprocess_image(test_image_mejorada)
        test_image_preprocessed = test_image_preprocessed.reshape(1, 64, 128, 1)

        predictions = model.predict(test_image_preprocessed)
        predicted_digits = ''.join(str(np.argmax(predictions[0][i])) for i in range(5))
        
        return predicted_digits
    else:
        return "No se encontró ninguna imagen en la carpeta."