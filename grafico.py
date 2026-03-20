import matplotlib.pyplot as plt
import pandas as pd



# Función para extraer deudas coactivas de la base de datos
def extraer_deudas_db(cursor):
    query = """
            SELECT 	CONCAT(p.nombres,' ',p.paterno) AS nombre_completo,d.deuda
            FROM presidente p
            INNER JOIN (SELECT dni_deudor,SUM(monto_deuda) AS deuda
                        FROM deuda
                        GROUP BY dni_deudor)d
                ON	p.dni = d.dni_deudor
            ORDER BY d.deuda DESC
            LIMIT 5;
            """
    cursor.execute(query)
    deudas = cursor.fetchall()
    return deudas


# Función para graficar deudas coactivas
def graficar_deudas(cursor):
    select = extraer_deudas_db(cursor)
    df = pd.DataFrame(select, columns=['nombre_completo', 'deuda'])
    nombres = df['nombre_completo'].tolist()
    deudas = df['deuda'].tolist()
    colores = ['orange', 'brown', 'green', 'pink', 'purple']

    plt.rcParams.update({'font.size': 5})
    plt.bar(nombres,deudas,width=0.8,label='Candidatos presidenciales con mayor deuda coactiva',edgecolor='gray',color=colores)
    plt.ylabel('Monto de Deuda Coactiva',fontsize=10)
    plt.xlabel('Candidatos',fontsize=10)
    plt.title('Deudas Coactivas de Candidatos Presidenciales',fontsize=16,fontname='Arial', fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.show()



# Función para extraer candidatos buscados de la base de datos
def extraer_buscados_db(cursor):
    query = """
            SELECT	COALESCE(candidato_buscado, 0) AS buscado,
                    pp.partido_politico
            FROM partido pp
            LEFT JOIN (SELECT COUNT(p.id_partido) AS candidato_buscado,id_partido
                        FROM buscado b
                        INNER JOIN (SELECT 	id_partido,
                                            CONCAT(nombres,' ',paterno,' ',materno) AS nombre_completo
                                    FROM presidente) p
                            ON b.nombres = p.nombre_completo
                        GROUP BY p.id_partido)t
            ON pp.id_partido = t.id_partido
            ORDER BY buscado DESC;
            """
    cursor.execute(query)
    buscados = cursor.fetchall()
    return buscados



# Función para graficar candidatos buscados
def graficar_buscados(cursor):
    select = extraer_buscados_db(cursor)
    df = pd.DataFrame(select, columns=['buscado', 'partido_politico'])
    buscados = df['buscado'].tolist()
    partidos = df['partido_politico'].tolist()

    plt.rcParams.update({'font.size': 5})
    plt.barh(partidos,buscados,label='Cantidad de candidatos con recompensa y buscados por la PNP',edgecolor='gray',color='orange')
    plt.ylabel('Partidos Politicos',fontsize=10)
    plt.xlabel('Cantidad de Candidatos Buscados',fontsize=10)
    plt.title('Candidatos Presidenciales con Recompensa y Orden de Captura',fontsize=16,fontname='Arial', fontweight='bold')
    plt.legend()
    plt.show()



# Función que llama a funciones de graficar deudas coactivas y candidatos buscados
def graficar(conexion):
    cursor = conexion.cursor()
    graficar_deudas(cursor)
    graficar_buscados(cursor)
    cursor.close()