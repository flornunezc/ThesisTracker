from analyzer import (
    analizar_documento,
    analizar_secciones,
    analizar_metricas_secciones
    )
from config import (
    NOMBRE_APP,
    VERSION, AUTOR,
    PROJECT_DIR,
    DATABASE_PATH,
    METRICAS,
    asegurar_estructura_proyecto
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

asegurar_estructura_proyecto()

def analizar_nueva_version():

    print()
    ruta = input("Pegá la ruta del archivo Word: ").strip().strip("'\"")
    
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
        resultado,
        cambios
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
        
        version = version_a_diccionario(version)

        print()
        
        print("Versión:", version["id"])
        print("Fecha:", version["fecha"])

        print()
        print("Contenido:")
        
        for metrica, info in METRICAS.items():
            
            print(
                f"{info['nombre']}: {version[metrica]}"
            )
        
        print()
        
        if version["id"] == 1:
            
            print("* Primera versión *")
            
        else:
            
            hay_cambios = any(
                version["cambio_" + metrica] != 0
                for metrica in METRICAS
            )
            
            if not hay_cambios:
                
                print("* Sin cambios desde anterior *")

            else:

                print("* Cambios desde anterior *")
                
                for metrica, info in METRICAS.items():
                    
                    print(
                        f"{info['nombre']}: "
                        f"{version['cambio_' + metrica]:+}"
                    )


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
        print("                 ", NOMBRE_APP)
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
        print("4 - Salir de", NOMBRE_APP)

        opcion = input("Elegí una opción: ")


        if opcion == "1":

            analizar_nueva_version()
            

        elif opcion == "2":

            mostrar_historial()
            
            
        elif opcion == "3":
            
            mostrar_dashboard()
            

        elif opcion == "4":

            print("Cerrando", NOMBRE_APP, "...")
            break


        else:

            print()
            print("* Opción no válida *")


abrir_proyecto()

crear_tabla()

mostrar_menu()
