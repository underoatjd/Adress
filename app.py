import time
import os
import cv2
import numpy as np
import pandas as pd
from PIL import Image  # Pillow para manipular imágenes
import io
from io import BytesIO  # Para almacenar la imagen en memoria
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tensorflow.keras.models import load_model  # type: ignore #

# Cargar el modelo entrenado
model = load_model("modelo_ocr.keras")
cedulas = pd.read_csv("datos.csv")
cedula = cedulas["CEDULA"]


service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.adres.gov.co/consulte-su-eps")
time.sleep(1)
driver.maximize_window()

iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"MSOPageViewerWebPart_WebPartWPQ3")))
# Cambia el contexto de Selenium al iframe
driver.switch_to.frame(iframe)

try:
    
    
    
    pass
except:
    pass



# Localiza el campo de entrada y envía la cédula
input_cedula = driver.find_element(By.XPATH, "//input[@id='txtNumDoc']")
input_cedula.clear()  # Limpiar el campo antes de ingresar un nuevo valor
input_cedula.send_keys(cedula)  # Enviar la cédula al campo de entrada
input("Aqui vamos")
time.sleep(10)
    