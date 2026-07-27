import sqlite3
import os
from config import DATABASE_PATH, METRICAS


def conectar():
    
    conexion = sqlite3.connect(DATABASE_PATH)

    return conexion


def crear_tabla():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS versiones (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        fecha TEXT,

        archivo TEXT,
        
        archivo_version TEXT,

        palabras INTEGER,

        parrafos INTEGER,

        tablas INTEGER,
        
        figuras INTEGER,
        
        cambio_palabras INTEGER,

        cambio_parrafos INTEGER,

        cambio_tablas INTEGER,
        
        cambio_figuras INTEGER

    )
    """)

    conexion.commit()

    conexion.close()
    

def guardar_version_db(
    fecha,
    archivo,
    archivo_version,
    metricas,
    cambios
):
    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO versiones
    (
    fecha,
    archivo,
    archivo_version,
    palabras,
    parrafos,
    tablas,
    figuras,
    cambio_palabras,
    cambio_parrafos,
    cambio_tablas,
    cambio_figuras
    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """,
    (fecha,
     archivo,
     archivo_version,
     
     metricas["palabras"],
     metricas["parrafos"],
     metricas["tablas"],
     metricas["figuras"],
     
     cambios["palabras"],
     cambios["parrafos"],
     cambios["tablas"],
     cambios["figuras"],
    )
    )

    conexion.commit()

    conexion.close()


def obtener_historial():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
    SELECT *
    FROM versiones
    ORDER BY id
    """)

    registros = cursor.fetchall()

    conexion.close()

    return registros


def obtener_ultima_version():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
    SELECT *
    FROM versiones
    ORDER BY id DESC
    LIMIT 1
    """)

    version = cursor.fetchone()

    conexion.close()

    return version


def version_a_diccionario(version):

    datos = {

        "id": version[0],
        "fecha": version[1],
        "archivo": version[2],
        "archivo_version": version[3],
    }
    
    inicio_metricas = 4
    
    inicio_cambios = inicio_metricas + len(METRICAS)
    
    for i, metrica in enumerate(METRICAS):
        
        datos[metrica] = version[inicio_metricas + i]
        
        datos["cambio_"+metrica] = version[inicio_cambios + i]
        
    
    return datos



def contar_versiones():
    
    conexion = conectar()
    
    cursor = conexion.cursor()
    
    cursor.execute("""
    SELECT COUNT (*)
    FROM versiones
    """)
    
    cantidad = cursor.fetchone()[0]
    
    conexion.close()
    
    return cantidad

