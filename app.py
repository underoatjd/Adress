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
from limpiezaImagen import mejorar_imagen
from predicciones import ocr_predict


cedulas = pd.read_csv("datos.csv")
# Cargar el modelo entrenado
model = load_model("modelo_ocr.keras")


service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.adres.gov.co/consulte-su-eps")
time.sleep(1)
driver.maximize_window()

iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"MSOPageViewerWebPart_WebPartWPQ3")))
# Cambia el contexto de Selenium al iframe
driver.switch_to.frame(iframe)
elemento = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//div[@id='content']//div[@align='center']")))
driver.execute_script("arguments[0].scrollIntoView();", elemento)


# Ruta donde se guardarán las imágenes
ruta_carpeta = "/imagenTemporal"
if not os.path.exists(ruta_carpeta):
    os.makedirs(ruta_carpeta)

input_pathM = "/imagenTemporal/ImagenTemporal.png"
output_pathM = "/imagenTemporal/ImagenTemporal.png"
modeloEntrenado = "modelo_ocr.keras"

def iteraciones(dataframe):
    for index, row in dataframe.iterrows():
        captcha = driver.find_element(By.XPATH, "//img[@id='Capcha_CaptchaImageUP']")
        inputCaptcha = driver.find_element(By.XPATH, "//input[@id='Capcha_CaptchaTextBox']")
        inputCedula = driver.find_element(By.XPATH, "//input[@id='txtNumDoc']")
        cedulaIterada = row["CEDULA"]
        ruta_imagen = os.path.join(ruta_carpeta, "ImagenTemporal.png")
        captcha.screenshot(ruta_imagen)
        try:
            mejorar_imagen(input_pathM,output_pathM)
            
            
        except:
            print("Error en procesameinto de imagen")
        
        try:
            resultado = ocr_predict(input_pathM,modeloEntrenado)
            print(resultado)
            input("Aqui vamos")
            
        except:
            print("Error inesperado")
                        
        
             
                



iteraciones(cedulas)
    