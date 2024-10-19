import time
from variables import *
from variables import dataFrame
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys



def recor_dataFrame(dataFrame):
    for index, row in dataFrame.iterrows():
        cedula = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//input[@id='form:numeroId']")))
        obligacion = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//input[@id='form:numeroCuenta']")))
        clienteCedula = str(row["cedula"])
        clienteObligacion = str(row["obligacion"])
        cedula.clear()
        obligacion.clear()
        time.sleep(1)
        cedula.send_keys(clienteCedula)
        obligacion.send_keys(clienteObligacion)
        time.sleep(1)
        tipoIdentificacion = Select(WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//select[@id='form:tipoIdentificacion']"))))
        tipoIdentificacion.select_by_value("1")
        time.sleep(1)
        tipoCartera = Select(WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//select[@id='form:tipoCartera']"))))
        tipoCartera.select_by_index(1)
        time.sleep(1)
        motivoEliminacion = Select(WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//select[@id='form:motivoEliminacion']"))))
        motivoEliminacion.select_by_index(6)
        time.sleep(1)
        botonAceptarEliminacion = driver.find_element(By.XPATH,"//input[@name='form:_id35']")
        botonAceptarEliminacion.click()
        
        try:
                bloqueRliminar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//body[1]/form[1]/table[1]/tbody[1]/tr[3]/td[1]")))
                botonEliminar = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,"//input[@name='_id1:_id35']")))
                botonEliminar.click()
                print(f"Cedula eliminada,{clienteCedula}")
                time.sleep(5)
                botonRegresarInicio = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//input[@name='form2:_id47']")))
                botonRegresarInicio.click()
                eliminacionObligacion = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//a[normalize-space()='Eliminación de Obligación']")))
                eliminacionObligacion.click()
                
        except:
                print(f"{clienteCedula},{clienteObligacion}, ya eliminados")
        
        try:
            time.sleep(1)
            msjError = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//li[@class='textoMensajeError']")))
            errorText = msjError.text
            print(f"{clienteCedula},{errorText}")
            time.sleep(1)
        
        except:
            
            print("Error Inesperado en el segundo try")
            


service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://miportafolio.transunion.co/nidp/idff/sso?id=MiPortafolioContract&sid=0&option=credential&sid=0&target=https%3A%2F%2Fmiportafolio.transunion.co%2Fcifin")
time.sleep(1)
driver.maximize_window()

try:    
    #Autenticacion con correo electronico.
    EtransID = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//input[@id='Ecom_User_ID']")))
    EtransID.send_keys(transID)
    time.sleep(1)
    EtransPASS = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//input[@id='Ecom_Password']")))
    EtransPASS.send_keys(transPASS)
    time.sleep(1)
    loginButton = driver.find_element(By.XPATH,"//input[@id='loginButton2']")
    time.sleep(1)
    loginButton.click()
    time.sleep(3)
    botonCorreo = driver.find_element(By.XPATH,"//input[@id='Ecom_MAIL_F']")
    botonCorreo.click()
    WebDriverWait(driver,120).until(EC.presence_of_element_located((By.XPATH,"//a[normalize-space()='Actualización Sector Real']")))
    print("Terminada autenticacion con exito")
except:
    print("Inicio o autenticacion fallida")    


try:
    # terminada la autenticacion por correo continuamos al menu de la tabla de obligaciones
    ActualizacionSR = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//a[normalize-space()='Actualización Sector Real']")))
    ActualizacionSR.click()

    eliminacionObligacion = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//a[normalize-space()='Eliminación de Obligación']")))
    eliminacionObligacion.click()

    tablaEliminacion = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH,"//body[1]/form[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[4]/td[1]/table[1]/tbody[1]/tr[1]/td[1]")))
    print(tablaEliminacion)
except:
    print("No pudimos encontrar la ruta al menu de obligaciones.")
    
    
recor_dataFrame(dataFrame)
    
    
input("Programa finalizado")