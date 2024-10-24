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

workHome = "renovar"
# Ruta donde se guardarán las imágenes
if workHome == "renovar":
    ruta_carpeta = "C:/python/RENOVAR FINANCIERA SELENIUM/ADRES/imagenTemporal"
    input_pathM = "C:/python/RENOVAR FINANCIERA SELENIUM/ADRES/imagenTemporal/ImagenTemporal.png"
    output_pathM = "C:/python/RENOVAR FINANCIERA SELENIUM/ADRES/imagenTemporal/ImagenTemporal.png"
else:
    ruta_carpeta = "F:/Descargas/Descargas/SELENIUM CURSO/ADRESS/Adress/imagenTemporal/"
    input_pathM = "F:/Descargas/Descargas/SELENIUM CURSO/ADRESS/Adress/imagenTemporal/ImagenTemporal.png"
    output_pathM = "F:/Descargas/Descargas/SELENIUM CURSO/ADRESS/Adress/imagenTemporal/ImagenTemporal.png"






def iteraciones(dataframe):
    for index, row in dataframe.iterrows():
        # Encuentra los elementos de la cédula y el botón para recargar captcha
        inputCedula = driver.find_element(By.XPATH, "//input[@id='txtNumDoc']")
        btnConsultar = driver.find_element(By.XPATH, "//input[@id='btnConsultar']")
        btnRecargarCaptcha = driver.find_element(By.XPATH, "//a[@id='Capcha_CaptchaLinkButton']")
        
        # Captura la cédula actual del dataframe
        cedulaIterada = row["CEDULA"]
        
        # Ingresa la cédula
        inputCedula.clear()
        inputCedula.send_keys(str(cedulaIterada))
        
        captcha_resuelto = False  # Indicador para salir del bucle cuando el captcha sea resuelto
        
        while not captcha_resuelto:
            try:
                # Encuentra el elemento del captcha
                captcha = driver.find_element(By.XPATH, "//img[@id='Capcha_CaptchaImageUP']")
                inputCaptcha = driver.find_element(By.XPATH, "//input[@id='Capcha_CaptchaTextBox']")
                
                # Toma un screenshot del captcha
                ruta_imagen = os.path.join(ruta_carpeta, "ImagenTemporal.png")
                captcha.screenshot(ruta_imagen)
                
                # Limpia la imagen del captcha
                mejorar_imagen(input_pathM, output_pathM)
                
                # Predicción del captcha usando el modelo OCR
                resultado_captcha = ocr_predict(ruta_imagen)
                print(f"Predicción del captcha: {resultado_captcha}")
                
                # Ingresa la predicción del captcha
                inputCaptcha.clear()
                inputCaptcha.send_keys(resultado_captcha)
                
                # Hacer clic en el botón de consultar
                btnConsultar.click()

                # Espera para ver si la consulta fue exitosa
                time.sleep(2)  # Ajustar según la velocidad de la página

                # Verificación si el captcha fue incorrecto
                mensaje_error = driver.find_elements(By.XPATH, "//span[@id='Capcha_ctl00']")
                if not mensaje_error:
                    print(f"Consulta exitosa para cédula: {cedulaIterada}")
                    captcha_resuelto = True  # Sale del bucle si el captcha fue correcto
                else:
                    print(f"Captcha incorrecto, recargando y reintentando...")
                    btnRecargarCaptcha.click()  # Recarga el captcha
                    time.sleep(1)  # Espera a que el nuevo captcha cargue antes de volver a intentar

            except Exception as e:
                print(f"Error en la predicción o en el proceso de automatización: {e}")
                btnRecargarCaptcha.click()  # Recarga el captcha en caso de error
                time.sleep(1)

iteraciones(cedulas)


print("""

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
            resultado = ocr_predict(ruta_imagen)
            print(resultado)
            input("Revisa la prediccion y la imagen en la carpeta ImagenTemporal")
        except:
            print("Error inesperado en el modelo")

iteraciones(cedulas)
    """)