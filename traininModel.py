import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model  # type: ignore
from tensorflow.keras import layers, models  # type: ignore
from tensorflow.keras.utils import to_categorical  # type: ignore
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator  # type: ignore
from tensorflow.keras.callbacks import EarlyStopping  # type: ignore

# Configurar EarlyStopping
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# Verificar si el modelo ya está guardado
if os.path.exists('modelo_ocr.h5'):
    # Cargar el modelo guardado
    model = load_model('modelo_ocr.h5')
    print("Modelo cargado desde 'modelo_ocr.h5'")
else:
    # Si el modelo no existe, crear uno nuevo
    def create_model():
        model = models.Sequential()
        
        # Primera capa convolucional + max pooling
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 128, 1)))
        model.add(layers.MaxPooling2D((2, 2)))
        
        # Segunda capa convolucional + max pooling
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        
        # Tercera capa convolucional + max pooling
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        
        # Aplanar las capas convolucionales
        model.add(layers.Flatten())
        
        # Capa densa intermedia
        model.add(layers.Dense(128, activation='relu'))
        
        # Salida: 5 neuronas, una por cada dígito del captcha
        model.add(layers.Dense(5 * 10, activation='softmax'))  # 10 clases (0-9) para cada uno de los 5 dígitos
        
        # Ajustar la arquitectura para salida de 5 dígitos (10 clases cada uno)
        model.add(layers.Reshape((5, 10)))
        
        return model

    model = create_model()
    print("Nuevo modelo creado")

    # Compilar el modelo (solo si es nuevo)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Ruta a la carpeta de imágenes
image_folder = 'C:/python/RENOVAR FINANCIERA SELENIUM/ADRES/images prepro'

# Obtener una lista de todos los archivos en la carpeta
image_files = os.listdir(image_folder)

# Función para cargar una imagen dado su nombre de archivo
def load_image(filename):
    img_path = os.path.join(image_folder, filename)
    return cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Cargar en escala de grises

# Probar cargando la primera imagen y obteniendo su etiqueta desde el nombre de archivo
first_image_filename = image_files[0]
first_image = load_image(first_image_filename)

# Extraer la etiqueta desde el nombre del archivo (eliminando la extensión)
first_label = os.path.splitext(first_image_filename)[0]

# Mostrar la primera imagen para verificar que esté correcta
plt.imshow(first_image, cmap='gray')
plt.title(f'Label: {first_label}')
plt.show()

# Definir el tamaño al que redimensionaremos todas las imágenes
IMG_WIDTH = 128
IMG_HEIGHT = 64

# Función para preprocesar una imagen
def preprocess_image(image):
    # Redimensionar la imagen
    image_resized = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
    # Normalizar la imagen
    image_normalized = image_resized / 255.0
    return image_normalized

# Preprocesar todas las imágenes y etiquetas
images = []
labels = []

for filename in image_files:
    # Cargar y preprocesar la imagen
    image = load_image(filename)
    image_preprocessed = preprocess_image(image)
    
    # Añadir la imagen preprocesada a la lista
    images.append(image_preprocessed)
    
    # Extraer la etiqueta y convertirla a one-hot encoding
    label = list(filename.split('.')[0])  # Separar los dígitos del captcha
    labels.append(label)

# Convertir las listas a arrays de NumPy
images = np.array(images)
labels = np.array(labels)

# Ver resumen del modelo
model.summary()

# Convertir etiquetas a one-hot encoding
def labels_to_one_hot(labels):
    one_hot_labels = []
    for label in labels:
        one_hot = to_categorical([int(digit) for digit in label], num_classes=10)  # 10 clases para 0-9
        one_hot_labels.append(one_hot)
    return np.array(one_hot_labels)

one_hot_labels = labels_to_one_hot(labels)

# Dividir en conjuntos de entrenamiento y validación
X_train, X_val, y_train, y_val = train_test_split(images, one_hot_labels, test_size=0.2, random_state=42)

# Ajustar la forma de X_train y X_val para que tengan el canal de color
X_train = X_train.reshape(-1, IMG_HEIGHT, IMG_WIDTH, 1)
X_val = X_val.reshape(-1, IMG_HEIGHT, IMG_WIDTH, 1)

# Crear un generador de datos con aumentación
datagen = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=False,
    fill_mode='nearest'
)

# Ajustar el modelo con el generador y EarlyStopping
model.fit(datagen.flow(X_train, y_train, batch_size=32),
          validation_data=(X_val, y_val),
          epochs=100,
          callbacks=[early_stopping])

# Guardar el modelo
model.save('modelo_ocr.keras')

