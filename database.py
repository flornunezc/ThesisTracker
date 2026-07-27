import sqlite3
import os
from config import DATABASE_PATH


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
    palabras,
    parrafos,
    tablas,
    figuras,
    cambio_palabras,
    cambio_parrafos,
    cambio_tablas,
    cambio_figuras
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
     palabras,
     parrafos,
     tablas,
     figuras,
     cambio_palabras,
     cambio_parrafos,
     cambio_tablas,
     cambio_figuras)
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

    return {

        "id": version[0],
        "fecha": version[1],
        "archivo": version[2],
        "archivo_version": version[3],
        "palabras": version[4],
        "parrafos": version[5],
        "tablas": version[6],
        "figuras": version[7],
        "cambio_palabras": version[8],
        "cambio_parrafos": version[9],
        "cambio_tablas": version[10],
        "cambio_figuras": version[11]

    }


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

