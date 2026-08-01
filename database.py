import sqlite3
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
        
        paginas INTEGER,

        tablas INTEGER,
        
        figuras INTEGER,
        
        referencias INTEGER,
        
        cambio_palabras INTEGER,

        cambio_parrafos INTEGER,
        
        cambio_paginas INTEGER,

        cambio_tablas INTEGER,
        
        cambio_figuras INTEGER,
        
        cambio_referencias INTEGER

    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS secciones (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        version_id INTEGER,

        seccion_id TEXT,
    
        titulo TEXT,

        nivel INTEGER,
    
        palabras INTEGER,

        parrafos INTEGER,

        paginas INTEGER,

        tablas INTEGER,

        figuras INTEGER,

        referencias INTEGER,

        FOREIGN KEY (version_id)
        REFERENCES versiones(id)

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
    
    valores_metricas = []
    
    for metrica in METRICAS:
        
        valores_metricas.append(metricas[metrica])
        
    
    valores_cambios = []
    
    for metrica in METRICAS:
        
        valores_cambios.append(cambios[metrica])
        

    cursor.execute("""
    INSERT INTO versiones
    (
    fecha,
    archivo,
    archivo_version,
    palabras,
    parrafos,
    paginas,
    tablas,
    figuras,
    referencias,
    cambio_palabras,
    cambio_parrafos,
    cambio_paginas,
    cambio_tablas,
    cambio_figuras,
    cambio_referencias
    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """,
    (fecha,
     archivo,
     archivo_version,
     *valores_metricas,
     *valores_cambios
     )
     )
    
    version_id = cursor.lastrowid

    conexion.commit()

    conexion.close()
    
    return version_id


def guardar_secciones_db(
    version_id,
    secciones
):

    conexion = conectar()

    cursor = conexion.cursor()


    for seccion in secciones:


        valores_metricas = []

        for metrica in METRICAS:

            valores_metricas.append(
                seccion["metricas"][metrica]
            )


        cursor.execute("""
        INSERT INTO secciones
        (

        version_id,

        seccion_id,

        titulo,

        nivel,

        palabras,

        parrafos,

        paginas,

        tablas,

        figuras,

        referencias

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """,
        (

            version_id,

            seccion["id"],

            seccion["titulo"],

            seccion["nivel"],

            *valores_metricas

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


def obtener_evolucion():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
    SELECT *
    FROM versiones
    ORDER BY id
    """)

    registros = cursor.fetchall()

    conexion.close()

    evolucion = []

    for version in registros:

        evolucion.append(
            version_a_diccionario(version)
        )

    return evolucion


"""
def obtener_secciones_version(version_id):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
#    SELECT *
#    FROM secciones
#    WHERE version_id = ?
#    """, (version_id,))
"""
    datos = cursor.fetchall()

    conexion.close()

    return datos
"""