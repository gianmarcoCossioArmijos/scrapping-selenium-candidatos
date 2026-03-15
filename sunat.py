from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException



def extraer_data_sunat(cursor, driver):
    # Ingresar al detalle del registro
    card = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[3]/div[2]/a")
    driver.execute_script("arguments[0].click();", card)

    # Localizar botón de deuda coactiva y dar clic
    driver.implicitly_wait(30)
    driver.execute_script("window.scrollBy(0, 500);")
    WebDriverWait(driver, 35).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div/div[5]/div[1]/div[2]/form/button")))
    boton_deuda_coactiva = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[5]/div[1]/div[2]/form/button")
    driver.execute_script("arguments[0].click();", boton_deuda_coactiva)

    # Validar si se encontro informacion de deuda coactiva disponible
    try:
        driver.implicitly_wait(35)
        info_coactiva = driver.find_element(By.XPATH, "/html/body/div/div[3]/div[1]")
    except NoSuchElementException:
        info_coactiva = False

    if info_coactiva != False:
        print("Registro con deuda coactiva encontrado")
        boton_coactiva_regresar = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[2]/button")
        driver.execute_script("arguments[0].click();", boton_coactiva_regresar)

        driver.implicitly_wait(35)
        nueva_consulta = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[4]/button")
        driver.execute_script("arguments[0].click();", nueva_consulta)
    else:
        # Si no se encontro informacion de deuda coactiva disponible se retorna a nueva consulta
        print("Registro de deuda coactiva no disponible (error de pagina)")
        boton_error_coactiva_regresar = driver.find_element(By.XPATH, "/html/body/a")
        driver.execute_script("arguments[0].click();", boton_error_coactiva_regresar)

        driver.implicitly_wait(35)
        nueva_consulta = driver.find_element(By.CLASS_NAME, "/html/body/div/div[2]/div/div[4]/button")
        driver.execute_script("arguments[0].click();", nueva_consulta)
    


def validar_data_sunat(cursor, driver):
    # Implementar lógica de validación de datos
    driver.implicitly_wait(30)
    try:
        driver.implicitly_wait(35)
        card = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[3]/div[2]/a")
    except NoSuchElementException:
        card = False

    if card != False:
        print("Registro en sunat encontrado")
        extraer_data_sunat(cursor, driver)
    else:
        print("Registro en sunat no encontrado")
        boton_nueva_consulta = driver.find_element(By.ID, "btnNuevaConsulta")
        driver.execute_script("arguments[0].click();", boton_nueva_consulta)



def buscar_data(dni, cursor, driver):
    # Localizar boton de busqueda por dni y dar clic
    driver.implicitly_wait(30)
    WebDriverWait(driver, 35).until(EC.presence_of_element_located((By.ID, "btnPorDocumento")))
    boton_por_documento = driver.find_element(By.ID, "btnPorDocumento")
    driver.execute_script("arguments[0].click();", boton_por_documento)

    # Localizar el campo de búsqueda e ingresar el DNI a buscar
    driver.implicitly_wait(30)
    WebDriverWait(driver, 35).until(EC.presence_of_element_located((By.ID, "txtNumeroDocumento")))
    campo_dni = driver.find_element(By.ID, "txtNumeroDocumento")
    driver.execute_script("arguments[0].click();", campo_dni)
    campo_dni.send_keys(dni)

    # Localizar el botón de búsqueda y dar clic
    driver.implicitly_wait(30)
    boton_busqueda = driver.find_element(By.ID, "btnAceptar")
    driver.execute_script("arguments[0].click();", boton_busqueda)

    # Llamar funcion de validacion de consulta
    validar_data_sunat(cursor, driver)
    print("****************************************")



def validar_dni(dni):
    if len(str(dni)) < 8:
        longitud_faltante = 8 - len(str(dni))
        str_faltante = "0" * longitud_faltante
        dni_completo = str_faltante + str(dni)
        print(f"DNI completo: {dni_completo}")
        return dni_completo
    else:
        dni_completo = dni
        print(f"DNI completo: {dni_completo}")
        return dni_completo



# Función para obtener datos de la base de datos
def obtener_data_sunat(query, conexion):
    # Establecer conexiones
    driver = webdriver.Chrome()
    base_url = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp"
    driver.get(base_url)

    # Ejecutar consulta SQL para obtener el nombre completo del parlamentario con el DNI especificado
    cursor = conexion.cursor()
    cursor.execute(query)
    filas = cursor.fetchall()

    # Iterar resultado y llamar scraping
    for fila in filas:
        print(fila[0])
        dni = validar_dni(fila[0])
        buscar_data(dni, cursor, driver)
        conexion.commit()
    driver.quit()
    cursor.close()