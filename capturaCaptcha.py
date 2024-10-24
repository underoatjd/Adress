import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Inicializa el driver
service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.adres.gov.co/consulte-su-eps")
time.sleep(1)
driver.maximize_window()

# Localiza el iframe usando el ID o el nombre
iframe = driver.find_element(By.ID, "MSOPageViewerWebPart_WebPartWPQ3")

# Cambia el contexto de Selenium al iframe
driver.switch_to.frame(iframe)

# Ruta donde se guardarán las imágenes
ruta_carpeta = "F:/Descargas/Descargas/SELENIUM CURSO/ADRESS/Adress/images/"
if not os.path.exists(ruta_carpeta):
    os.makedirs(ruta_carpeta)

# Número de captchas que deseas capturar
cantidad_captchas = 10

# Ciclo para capturar los captchas
for i in range(1, cantidad_captchas + 1):
    try:
        # Localiza el elemento del captcha
        captcha = driver.find_element(By.XPATH, "//img[@id='Capcha_CaptchaImageUP']")
        
        # Guarda la captura de pantalla del captcha
        ruta_imagen = os.path.join(ruta_carpeta, "ImagenTemporal.png")
        captcha.screenshot(ruta_imagen)
        print(f"Captcha {i} guardado en: {ruta_imagen}")

        # Localiza el botón para recargar el captcha y haz clic
        recargar_boton = driver.find_element(By.XPATH, "//a[@id='Capcha_CaptchaLinkButton']")
        recargar_boton.click()

        # Espera un momento para que el captcha nuevo cargue
        time.sleep(2)

    except Exception as e:
        print(f"Error en la captura del captcha {i}: {str(e)}")
        break

# Vuelve al contexto principal de la página
driver.switch_to.default_content()

# Cierra el navegador al terminar
driver.quit()