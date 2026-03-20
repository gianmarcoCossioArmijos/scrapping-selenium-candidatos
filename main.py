from grafico import graficar
from wanted import obtener_data
from sunat import obtener_data_sunat
from db import obtener_conexion



# Constantes
QUERY_PARLAMENTARIO_PNP = """
            SELECT CONCAT(nombres,' ',paterno,' ',materno) AS nombre_completo
            FROM parlamentario;
            """
QUERY_PRESIDENTE_PNP= """
            SELECT CONCAT(nombres,' ',paterno,' ',materno) AS nombre_completo
            FROM presidente;
            """
QUERY_PRESIDENTE_SUNAT= """
            SELECT dni
            FROM presidente;
            """
QUERY_PARLAMENTARIO_SUNAT= """
            SELECT dni
            FROM parlamentario;
            """



def main():
    conexion = obtener_conexion()
    #print("******************** BUSCAR PRESIDENTES EN MAS BUSCADOS DE LA PNP ********************")
    #obtener_data(QUERY_PRESIDENTE_PNP, conexion)
    #print("******************** FIN BUSQUEDA PRESIDENTES EN MAS BUSCADOS DE LA PNP ********************")

    #print("******************** BUSCAR PARLAMENTARIOS EN MAS BUSCADOS DE LA PNP ********************")
    #obtener_data(QUERY_PARLAMENTARIO_PNP, conexion)
    #print("******************** FIN BUSQUEDA PARLAMENTARIOS EN MAS BUSCADOS DE LA PNP ********************")

    #print("******************** BUSCAR PRESIDENTES EN SUNAT ********************")
    #obtener_data_sunat(QUERY_PRESIDENTE_SUNAT, conexion)
    #print("******************** FIN BUSQUEDA PRESIDENTES EN SUNAT ********************")

    #print("******************** BUSCAR PARLAMENTARIOS EN SUNAT ********************")
    #obtener_data_sunat(QUERY_PARLAMENTARIO_SUNAT, conexion)
    #print("******************** FIN BUSQUEDA PARLAMENTARIOS EN SUNAT ********************")

    print("******************** GRAFICAR DEUDAS ********************")
    graficar(conexion)
    print("******************** FIN GRAFICAR DEUDAS ********************")

    conexion.close()



if __name__ == "__main__":
    main()