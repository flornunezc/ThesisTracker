from analyzer import (
    analizar_documento,
    obtener_secciones,
    construir_estructura,
    mostrar_estructura,
    obtener_palabras_secciones
    )
from config import (
    NOMBRE_PROYECTO,
    VERSION, AUTOR,
    PROJECT_DIR,
    DATABASE_PATH,
    METRICAS
    )
from file_manager import guardar_version
from database import (
    crear_tabla,
    guardar_version_db,
    obtener_historial,
    obtener_ultima_version,
    version_a_diccionario,
    contar_versiones
    )
from datetime import datetime
from comparator import comparar_metricas, mostrar_cambios
import os
from project_manager import abrir_proyecto

def analizar_nueva_version():

    print()
    ruta = input("Pegá la ruta del archivo Word: ")

    resultado = analizar_documento(ruta)
    
    ultima = obtener_ultima_version()
    
    if ultima:
        
        ultima = version_a_diccionario(ultima)
        
        cambios = comparar_metricas(
            resultado,
            ultima
        )
        
        mostrar_cambios(cambios)
        
    else:
        
        cambios = {}
        
        for metrica in METRICAS:
            cambios[metrica] = 0
           
        
        print()
        print("Esta es la primera version del documento.")

    copia = guardar_version(ruta)
    
    archivo_version = os.path.basename(copia)

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    archivo = os.path.basename(ruta)

    guardar_version_db(
        fecha,
        archivo,
        archivo_version,
        resultado["palabras"],
        resultado["parrafos"],
        resultado["tablas"],
        resultado["figuras"],
        cambios["palabras"],
        cambios["parrafos"],
        cambios["tablas"],
        cambios["figuras"]
    )

    print()
    print("Versión guardada correctamente:")
    print(copia)

    print()
    print("Métricas totales:")
    for metrica, info in METRICAS.items():
        
        print(f"{info['nombre']}: {resultado[metrica]}")
    

def mostrar_historial():

    print()
    print("======================")
    print("Historial de escritura")
    print("======================")

    historial = obtener_historial()

    for version in historial:

        print()
        
        print("Versión:", version[0])
        print("Fecha:", version[1])

        print()
        print("Contenido:")
        print("Palabras:", version[4])
        print("Párrafos:", version[5])
        print("Tablas:", version[6])
        print("Figuras:", version[7])

        print()
        
        if version[0] == 1:
            
            print("* Primera versión *")
        
        elif version[8] == 0 and version[9] == 0 and version[10] == 0 and version[11] == 0:

            print("* Sin cambios desde anterior *")

        else:

            print("* Cambios desde anterior *")
            print("Palabras:", f"{version[8]:+}")
            print("Párrafos:", f"{version[9]:+}")
            print("Tablas:", f"{version[10]:+}")
            print("Figuras:", f"{version[11]:+}")


        print()
        print("-----------------------------------")


def mostrar_dashboard():

    ultima = obtener_ultima_version()


    if ultima:

        ultima = version_a_diccionario(ultima)

        print()
        print("--------------------------------------------------")
        print("Última versión del proyecto -", ultima["fecha"])
        print("--------------------------------------------------")
        for metrica, info in METRICAS.items():
            
            print(f"{info['nombre']:<10}: {ultima[metrica]}")

        print("Versiones:", contar_versiones())
        
        
        print()
        print("          Últimos cambios en el proyecto")
        print("--------------------------------------------------")


        for metrica, info in METRICAS.items():
            
            print(
                f"{ultima['cambio_' + metrica]:+} {info['nombre'].lower()}"
                )
        
    
    
    else:

        print()
        print("Todavía no hay versiones.")
        
        

def mostrar_menu():

    while True:
        
        
        print()
        print("==================================================")
        print("                 ", NOMBRE_PROYECTO)
        print("==================================================")
        print("Autora:", AUTOR)
        print("Versión:", VERSION)

        
        print()
        print("--------------------------------------------------")
        print("                       MENU")
        print("--------------------------------------------------")

        print()
        print("1 - Analizar nueva versión")
        print("2 - Ver historial")
        print("3 - Mostrar último análisis")
        print("4 - Salir")

        opcion = input("Elegí una opción: ")


        if opcion == "1":

            analizar_nueva_version()
            

        elif opcion == "2":

            mostrar_historial()
            
            
        elif opcion == "3":
            
            mostrar_dashboard()
            

        elif opcion == "4":

            print("Cerrando", NOMBRE_PROYECTO, "...")
            break


        else:

            print()
            print("* Opción no válida *")


abrir_proyecto()

#ruta_prueba = input("Word para analizar secciones: ")

#resultado = obtener_palabras_secciones(ruta_prueba)

#for seccion in resultado:
#    print(
#        seccion["titulo"],
#        "-",
#        seccion["palabras"],
#        "palabras"
#        )
    

crear_tabla()

mostrar_menu()
