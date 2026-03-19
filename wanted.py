from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException



# Función para obtener datos de la base de datos
def obtener_data(query, conexion):
    # Establecer conexiones
    driver = webdriver.Chrome()
    base_url = "https://recompensas.pe/requisitoriados"
    driver.get(base_url)

    # Ejecutar consulta SQL para obtener el nombre completo del parlamentario con el DNI especificado
    cursor = conexion.cursor()
    cursor.execute(query)
    filas = cursor.fetchall()

    # Iterar resultado y llamar scraping
    for fila in filas:
        print(fila)
        buscar_data(fila, cursor, driver)
        conexion.commit()
    driver.quit()
    cursor.close()



# Función para registrar detalle de registro si es que fue encontrado
def registrar_data_encontrada(nombre_completo, cursor, driver):
    driver.implicitly_wait(30)
    driver.execute_script("window.scrollBy(0, 100);")
    
    # Ingresar al detalle del registro encontrado
    detalle = driver.find_element(
        By.XPATH, "/html/body/div/app-root/app-base-layout/main/app-requisitoriados-list/div/div[2]/div/div/div/div")
    driver.execute_script("arguments[0].click();", detalle)

    # Obetener estado de registro encontrado
    driver.implicitly_wait(30)
    encontrado2 = driver.find_element(
        By.XPATH, "/html/body/div/app-root/app-base-layout/main/app-requisitoriados-details/div/div[1]/div[2]/div[2]/div[2]/div/div/div[2]")
    estado = (encontrado2.text).upper()

    # Obetener lugar de requisitoria de registro encontrado
    driver.implicitly_wait(30)
    encontrado3 = driver.find_element(
        By.XPATH, "/html/body/div/app-root/app-base-layout/main/app-requisitoriados-details/div/div[1]/div[2]/div[2]/div[2]/div/div/div[6]")
    lugar_rq = (encontrado3.text).upper()

    # Obetener delito de registro encontrado
    driver.implicitly_wait(30)
    encontrado4 = driver.find_element(
        By.XPATH, "/html/body/div/app-root/app-base-layout/main/app-requisitoriados-details/div/div[1]/div[2]/div[2]/div[2]/div/div/div[8]/span")
    delito = (encontrado4.text).upper()

    # Obetener recompensa de registro encontrado
    driver.implicitly_wait(30)
    encontrado5 = driver.find_element(
        By.XPATH, "/html/body/div/app-root/app-base-layout/main/app-requisitoriados-details/div/div[1]/div[2]/div[2]/div[2]/div/div/div[9]")
    recompensa = (encontrado5.text).upper()

    # Ejecutar insert de registro encontrado
    query = "INSERT INTO buscado (nombres,estado,lugar_rq,delito,recompensa) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (nombres) DO NOTHING;"
    cursor.execute(query, (nombre_completo,estado,lugar_rq,delito,recompensa))
    print("Registro encontrado insertado en la base de datos...")



def validar_data(nombre_completo, cursor, driver):
    print("Buscando registro...")
    # Localizaar elemento de respuesta a busqueda
    try:
        no_encontrado = driver.find_element(By.XPATH, "/html/body/div/app-root/app-base-layout/main/app-requisitoriados-list/div/div[2]/div/h1")
    except NoSuchElementException:
        no_encontrado = False

    # Valida si el registro fue encontrado
    if no_encontrado == False:
        print("Registro encontrado")
        registrar_data_encontrada(nombre_completo, cursor, driver)
    else:
        print("Registro no encontrado")

    buscador = driver.find_element(By.LINK_TEXT, "LISTA DE BUSCADOS")
    driver.execute_script("arguments[0].click();", buscador)



def buscar_data(nombre_completo, cursor, driver):
    # Localizar el campo de búsqueda por nombre completo y enviar el nombre a buscar
    driver.implicitly_wait(30)
    WebDriverWait(driver, 35).until(EC.presence_of_element_located((By.NAME, "nombreCompleto")))
    driver.find_element(By.XPATH, "/html/body/div/app-root/app-base-layout/main/app-requisitoriados-search/div/div[2]/div/form/div[1]/div[2]/input").send_keys(nombre_completo)

    # Hacer scroll para que el botón de búsqueda sea visible
    # Localizar el botón de búsqueda y dar clic
    driver.implicitly_wait(30)
    driver.execute_script("window.scrollBy(0, 300);")
    boton = driver.find_element(By.XPATH, "/html/body/div/app-root/app-base-layout/main/app-requisitoriados-search/div/div[2]/div/form/div[1]/div[9]/button")
    driver.execute_script("arguments[0].click();", boton)

    # Llamar funcion de validacion
    validar_data(nombre_completo, cursor, driver)
    print("****************************************")