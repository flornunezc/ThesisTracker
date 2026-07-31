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
    guardar_secciones_db,
    obtener_historial,
    obtener_ultima_version,
    version_a_diccionario,
    contar_versiones,
    obtener_evolucion
    )
from datetime import datetime
from comparator import comparar_metricas, mostrar_cambios
import os
from project_manager import abrir_proyecto

asegurar_estructura_proyecto()

def analizar_nueva_version():

    print()
    ruta = input("Pegá la ruta del archivo Word: ").strip().strip("'\"")
    
    # METRICAS GLOBALES
    
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


    # COPIA DEL WORD 

    copia = guardar_version(ruta)
    
    archivo_version = os.path.basename(copia)

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    archivo = os.path.basename(ruta)
    
    
    # GUARDAR VERSION

    version_id = guardar_version_db(
        fecha,
        archivo,
        archivo_version,
        resultado,
        cambios
    )
    
    
    # ANALISIS POR SECCIONES
    
    secciones = analizar_secciones(ruta)
    
    secciones = analizar_metricas_secciones(
        
        ruta,
        secciones
        
    )
    
    guardar_secciones_db(
        
        version_id,
        secciones
        
    )
    
  #  print()
 #   print("Secciones guardadas:")

 #   for fila in obtener_secciones_version(version_id):
  #      print(fila)
    
    
    # RESUMEN

    print()
    print("Versión guardada correctamente:")
    #print(copia)

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
    
    ultimas_versiones = 3
    
    total_versiones = len(historial)
    
    if total_versiones > ultimas_versiones + 1:
        
        versiones_mostrar = (
            [historial[0]] +
            historial[-ultimas_versiones:]
        )
        
        versiones_ocultas = total_versiones - len(versiones_mostrar)
        
    else:
        
        versiones_mostrar = historial
        versiones_ocultas = 0
        

    for version in versiones_mostrar:
        
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
        
    
    if versiones_ocultas > 0:
        
        print()
        print(
            f"({versiones_ocultas} versiones intermedias ocultas)"
        )


def mostrar_ultima_version():

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
        


def mostrar_evolucion():

    evolucion = obtener_evolucion()

    if not evolucion:

        print()
        print("Todavía no hay versiones registradas.")
        return

    print()
    print("==========================================================")
    print("              EVOLUCIÓN DEL PROYECTO")
    print("==========================================================")
    print()

    for version in evolucion:

        print(f"Versión {version['id']}")
        print(f"Fecha: {version['fecha']}")

        for metrica, info in METRICAS.items():

            print(f"{info['nombre']:<12}: {version[metrica]}")

        print("-" * 50)



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
        print("2 - Mostrar último análisis")
        print("3 - Ver historial")
        print("4 - Mostrar evolución")
        print("5 - Salir de", NOMBRE_APP)

        opcion = input("Elegí una opción: ")


        if opcion == "1":

            analizar_nueva_version()
            

        elif opcion == "2":

            mostrar_ultima_version()
            
            
        elif opcion == "3":
            
            mostrar_historial()
            
        
        elif opcion == "4":
            
            mostrar_evolucion()
            

        elif opcion == "5":

            print("Cerrando", NOMBRE_APP, "...")
            break


        else:

            print()
            print("* Opción no válida *")


abrir_proyecto()

#print("Creando tablas...")
crear_tabla()
#print("Tablas creadas")

mostrar_menu()
