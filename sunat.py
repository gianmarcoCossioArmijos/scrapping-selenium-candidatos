from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException



def registrar_deuda_coactiva(dni, cursor, driver):
    try:
        driver.implicitly_wait(35)
        tabla_deuda_coactiva = driver.find_element(By.XPATH, "/html/body/div/div[3]/div[2]/div[2]/div/div/table/thead/tr/th[1]")
    except NoSuchElementException:
        tabla_deuda_coactiva = False

    if tabla_deuda_coactiva != False:
        print("Extrayendo deuda coactiva")
        dni_deudor = dni
        try:
            validar_tr_unico = driver.find_element(By.XPATH, "/html/body/div/div[3]/div[2]/div[2]/div/div/table/tbody/tr[2]")
        except NoSuchElementException:
            validar_tr_unico = False

        if validar_tr_unico == False:
            # Extraer datos de deuda coactiva unica
            monto_deuda_unica = (driver.find_element(By.XPATH, "/html/body/div/div[3]/div[2]/div[2]/div/div/table/tbody/tr/td[1]").text).upper()
            periodo_deuda_unica = (driver.find_element(By.XPATH, "/html/body/div/div[3]/div[2]/div[2]/div/div/table/tbody/tr/td[2]").text).upper()
            inicio_cobranza_deuda_unica = (driver.find_element(By.XPATH, "/html/body/div/div[3]/div[2]/div[2]/div/div/table/tbody/tr/td[3]").text).upper()
            entidad_deuda_unica = (driver.find_element(By.XPATH, "/html/body/div/div[3]/div[2]/div[2]/div/div/table/tbody/tr/td[4]").text).upper()

            # Ejecutar insert de deuda coactiva unica
            query = "INSERT INTO deuda (dni_deudor,monto_deuda,periodo_tributario,inicio_cobranza,entidad_deuda) VALUES (%s,%s,%s,%s,%s);"
            cursor.execute(query, (dni_deudor,monto_deuda_unica,periodo_deuda_unica,inicio_cobranza_deuda_unica,entidad_deuda_unica))
            print("Deuda coactiva unica insertada en la base de datos...")
        else:
            # Recorrer deudas coactivas
            filas = len(driver.find_elements(By.TAG_NAME, "tr")) - 1
            for i in range(filas):
                fila = i + 1
                monto_deuda_unica = (driver.find_element(By.XPATH, f"/html/body/div/div[3]/div[2]/div[2]/div/div/table/tbody/tr[{fila}]/td[1]").text).upper()
                periodo_deuda_unica = (driver.find_element(By.XPATH, f"/html/body/div/div[3]/div[2]/div[2]/div/div/table/tbody/tr[{fila}]/td[2]").text).upper()
                inicio_cobranza_deuda_unica = (driver.find_element(By.XPATH, f"/html/body/div/div[3]/div[2]/div[2]/div/div/table/tbody/tr[{fila}]/td[3]").text).upper()
                entidad_deuda_unica = (driver.find_element(By.XPATH, f"/html/body/div/div[3]/div[2]/div[2]/div/div/table/tbody/tr[{fila}]/td[4]").text).upper()

                # Ejecutar insert de deuda coactiva
                query = "INSERT INTO deuda (dni_deudor,monto_deuda,periodo_tributario,inicio_cobranza,entidad_deuda) VALUES (%s,%s,%s,%s,%s);"
                cursor.execute(query, (dni_deudor,monto_deuda_unica,periodo_deuda_unica,inicio_cobranza_deuda_unica,entidad_deuda_unica))
                print(f"Deuda coactiva numero {fila} insertada en la base de datos...")



        # salir de detale de deuda coactiva
        boton_coactiva_regresar = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[2]/button")
        driver.execute_script("arguments[0].click();", boton_coactiva_regresar)
    else:
        # salir de tabla de deuda coactiva y regresar a nueva consulta
        boton_regresar = driver.find_element(By.XPATH, "/html/body/div/div[4]/button[1]")
        driver.execute_script("arguments[0].click();", boton_regresar)
        driver.implicitly_wait(35)
        boton_nueva_consulta = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[4]/button")
        driver.execute_script("arguments[0].click();", boton_nueva_consulta)



def extraer_data_sunat(dni, cursor, driver):
    # Ingresar al detalle del registro
    card = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[3]/div[2]/a")
    driver.execute_script("arguments[0].click();", card)
    driver.implicitly_wait(35)

    # Localizar botón de deuda coactiva y dar clic
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        boton_deuda_coactiva = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[5]/div[1]/div[2]/form/button")
    except NoSuchElementException:
        boton_deuda_coactiva = False

    if boton_deuda_coactiva != False:
        driver.execute_script("arguments[0].click();", boton_deuda_coactiva)
        driver.implicitly_wait(35)
        print("Ingresando al boton deuda coactiva")
        # Validar si se encontro informacion de deuda coactiva disponible
        try:
            resultado_buqueda_coactiva = driver.find_element(By.XPATH, "/html/body/div/div[3]/div[1]")
        except NoSuchElementException:
            resultado_buqueda_coactiva = False

        if resultado_buqueda_coactiva != False:
            print("Resultado de busqueda deuda coactiva positivo")
            # Llamar funcion para registrar deuda coactiva en base de datos
            registrar_deuda_coactiva(dni, cursor, driver)
        else:
            print("Error en resultado de busqueda deuda de coactiva")
            # Regresamos antes del detalle de deuda coactiva y luego a nueva consulta
            driver.back()
            boton_nueva_consulta = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[4]/button")
            driver.execute_script("arguments[0].click();", boton_nueva_consulta)
    else:
        driver.back()
        boton_nueva_consulta = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[4]/button")
        driver.execute_script("arguments[0].click();", boton_nueva_consulta)


def validar_data_sunat(dni, cursor, driver):
    print("Ingresa a validar resultado de consulta RUC")
    # Implementar lógica de validación de datos
    driver.implicitly_wait(35)
    try:
        card = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[3]/div[2]/a/h4[1]")
    except NoSuchElementException:
        card = False

    # Validar si se encontro detalles en el card de deuda coactiva
    if card != False:
        print("Resultado de consulta RUC positivo")
        extraer_data_sunat(dni, cursor, driver)
    else:
        # Regresar a nueva consulta
        print("Resultado de consulta RUC negativo")
        boton_nueva_consulta = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[2]/button")
        driver.execute_script("arguments[0].click();", boton_nueva_consulta)



# Validar longitud de DNI y completar con ceros a la izquierda si es necesario
def validar_dni(dni):
    dni_completo = dni
    if len(str(dni)) < 8:
        longitud_faltante = 8 - len(str(dni))
        str_faltante = "0" * longitud_faltante
        dni_completo = str_faltante + str(dni)
    print(f"DNI completo: {dni_completo}")
    return dni_completo



def ingresar_dni_buscardor(dni, cursor, driver):
    print("Ingresa al buscador de consulta RUC por DNI")
    driver.get("https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp")
    # Localizar boton de busqueda por dni, dar click e ingresar el DNI a buscar
    WebDriverWait(driver, 35).until(EC.presence_of_element_located((By.ID, "btnPorDocumento")))
    boton_por_documento = driver.find_element(By.ID, "btnPorDocumento")
    driver.execute_script("arguments[0].click();", boton_por_documento)

    # Localizar el campo de búsqueda e ingresar el DNI a buscar
    WebDriverWait(driver, 35).until(EC.presence_of_element_located((By.ID, "txtNumeroDocumento")))
    campo_dni = driver.find_element(By.ID, "txtNumeroDocumento")
    driver.execute_script("arguments[0].click();", campo_dni)
    campo_dni.send_keys(dni)

    # Localizar el botón de búsqueda y dar clic
    WebDriverWait(driver, 35).until(EC.presence_of_element_located((By.ID, "btnAceptar")))
    boton_busqueda = driver.find_element(By.ID, "btnAceptar")
    driver.execute_script("arguments[0].click();", boton_busqueda)
    driver.implicitly_wait(35)
    try:
        error_buscador = driver.find_element(By.CLASS_NAME, "error")
    except NoSuchElementException:
        error_buscador = False

    # Llamar funcion de validacion de consulta
    if error_buscador != False:
        print("Error en el buscador de consulta RUC")
        driver.back()
    else:
        validar_data_sunat(dni, cursor, driver)



def buscar_data(dni, cursor, driver):
    # Llamar funcion longitud de DNI y buscar dni
    print("****************************************")
    dni = validar_dni(dni)
    ingresar_dni_buscardor(dni, cursor, driver)



# Función para obtener datos de la base de datos
def obtener_data_sunat(query, conexion):
    driver = webdriver.Chrome()
    driver.get("https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp")
    cursor = conexion.cursor()
    cursor.execute(query)
    filas = cursor.fetchall()

    # Iterar resultado y llamar scraping
    for fila in filas:
        buscar_data(fila[0], cursor, driver)
        conexion.commit()
    driver.quit()
    cursor.close()