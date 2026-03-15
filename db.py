import psycopg2

def obtener_conexion():
    conexion = psycopg2.connect(
        host="localhost",
        port="5433",
        database="most-wanted",
        user="postgres",
        password="123456"
    )
    return conexion
