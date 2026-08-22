from analyzer import (
    analizar_documento,
    analizar_secciones,
    analizar_metricas_secciones,
    contar_referencias
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
from stats import (
    preparar_series_temporales,
    obtener_metricas_capitulo,
    obtener_estado_tesis,
    obtener_estado_por_capitulo,
    calcular_ritmo_versiones
    )
from visualization import (
    mostrar_grafico_evolucion,
    graficar_ritmo_versiones
    )


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
    

    print()
    print("Versión guardada correctamente:")

    print()
    print("Métricas totales:")
    for metrica, info in METRICAS.items():
        
        print(f"{info['nombre']}: {resultado[metrica]}")
    

def mostrar_historial():

    print()
    print("============================================")
    print("           HISTORIAL DE ESCRITURA")
    print("============================================")

    historial = obtener_historial()
    
    if not historial:
        
        print()
        print("Todavía no hay versiones registradas.")
        return
    
    ultimas_versiones = 3
    
    total_versiones = len(historial)
    
    print()
    print(total_versiones, "versiones registradas")
    
    primera = version_a_diccionario(historial[0])
    
    print()
    print("Primera versión:")
    print(
        f"Versión {primera['id']} | "
        f"{primera['fecha']}"
    )
    
    ultima = version_a_diccionario(historial[-1])

    print()
    print("Última versión:")
    print(
        f"Versión {ultima['id']} | "
        f"{ultima['fecha']}"
    )
    
        
    versiones_mostrar = historial[-ultimas_versiones:]
    
    
    print()
    print("---------------------------------")
    print()
    print("Últimas versiones:")

    for version in versiones_mostrar:
        
        version = version_a_diccionario(version)

        print()
        
        print(
            f"Versión: {version['id']} | "
            f"Fecha: {version['fecha']}"
        )
        
        for metrica, info in METRICAS.items():
            
            cambio = version["cambio_" + metrica]
            
            if cambio != 0:
                
                print(
                    f"{info['nombre']}: "
                    f"{cambio:+}"
                )


def mostrar_ritmo_versiones():

    evolucion = obtener_evolucion()

    ritmo = calcular_ritmo_versiones(evolucion)

    if ritmo is None:

        print()
        print("No hay suficientes versiones para calcular el ritmo.")
        return


    print()
    print("========================================")
    print("        RITMO ENTRE VERSIONES")
    print("========================================")


    print()
    print(
        "Promedio de palabras por versión:",
        f"{ritmo['promedio']:+.0f}"
    )


    mayor = ritmo["mayor"]

    print()
    print("Mayor aumento:")
    print(
        f"Versión {mayor['version_anterior']} → "
        f"{mayor['version']}"
    )
    print(
        f"{mayor['cambio_palabras']:+} palabras"
    )


    menor = ritmo["menor"]

    print()
    print("Menor aumento:")
    print(
        f"Versión {menor['version_anterior']} → "
        f"{menor['version']}"
    )
    print(
        f"{menor['cambio_palabras']:+} palabras"
    )


    print()
    graficar_ritmo_versiones(ritmo)



def mostrar_evolucion():
    
           
    evolucion = obtener_evolucion()

    if not evolucion:

        print()
        print("Todavía no hay versiones registradas.")
        return

    
    while True:
        
        print()
        print("========================================")
        print("          EVOLUCIÓN DEL PROYECTO")
        print("========================================")

        print()
        print("1 - Evolución temporal")
        print("2 - Ritmo de escritura")
        print("3 - Actividad reciente")
        print("4 - Actividad por período")
        print("0 - Volver")
        
        
        print()
        
        opcion = input("Selecciones una opción: ")
        
        
        if opcion == "1":
            
            series = preparar_series_temporales(evolucion)
    
            mostrar_grafico_evolucion(series)
            
            
        elif opcion == "2":
            
            mostrar_ritmo_versiones()
            
            
        elif opcion == "3":
            
            print()
            print("Esta función todavía esta en desarrollo.")
            
            
        elif opcion == "4":
            
            print()
            print("Esta función todavía esta en desarrollo.")
        
        
        elif opcion == "0":
            
            break
        
        else:
            
            print()
            print("Opción no válida.")
            


def mostrar_resumen_tesis():

    estado = obtener_estado_tesis()

    if estado is None:

        print()
        print("Todavía no hay versiones registradas.")
        return


    print()
    print("========================================")
    print("           RESUMEN DE LA TESIS")
    print("========================================")

    print()
    print("Versión:", estado["version_id"])
    print("Fecha:", estado["fecha"])


    print()
    print()
    print("Estructura")
    print("----------------------------------------")

    print(
        "Capítulos:",
        estado["estadisticas"]["capitulos"]
    )

    print(
        "Secciones:",
        estado["estadisticas"]["secciones"]
    )

    print(
        "Subsecciones:",
        estado["estadisticas"]["subsecciones"]
    )
    
    print()
    print()
    print("Contenido")
    print("----------------------------------------")
    
    ultima = obtener_ultima_version()
    ultima = version_a_diccionario(ultima)
    
    for metrica, info in METRICAS.items():
        
        print(
            f"{info['nombre']}: "
            f"{ultima[metrica]}"
        )



def mostrar_estado_por_capitulo():
 
    estado = obtener_estado_tesis()

    if estado is None:

        print()
        print("Todavía no hay versiones registradas.")
        return


    print()
    print("========================================")
    print("           ESTADO POR CAPÍTULO")
    print("========================================")


    for capitulo in estado["capitulos"]:

        print()
        print(
            capitulo["id"],
            "|",
            capitulo["titulo"]
        )

        for metrica, info in METRICAS.items():

            print(
                f"{info['nombre']}: "
                f"{capitulo['metricas'][metrica]}"
            )
            

def mostrar_progreso_escritura():
    
    estado = obtener_estado_tesis()

    if estado is None:

        print()
        print("Todavía no hay versiones registradas.")
        return

    print()
    print("========================================")
    print("          PROGRESO DE ESCRITURA")
    print("========================================")

    
    mas = estado["estadisticas"]["mas_trabajada"]

    if mas:

        print()
        print("Más trabajada:")

        print(
            mas["capitulo_id"],
            "|",
            mas["capitulo"]
        )

        print(
            mas["seccion_id"],
            "|",
            mas["seccion"],
            "-",
            mas["palabras"],
            "palabras"
        )


    menos = estado["estadisticas"]["menos_trabajada"]

    if menos:

        print()
        print("Menos trabajada:")

        print(
            menos["capitulo_id"],
            "|",
            menos["capitulo"]
        )

        print(
            menos["seccion_id"],
            "|",
            menos["seccion"],
            "-",
            menos["palabras"],
            "palabras"
        )


def mostrar_estado_tesis():

    while True:

        print()
        print("========================================")
        print("          ESTADO DE LA TESIS")
        print("========================================")

        print()
        print("1 - Resumen de la tesis")
        print("2 - Estado por capítulo")
        print("3 - Progreso de escritura")
        print("0 - Volver")

        print()

        opcion = input("Seleccione una opción: ")


        if opcion == "1":

            mostrar_resumen_tesis()


        elif opcion == "2":

            mostrar_estado_por_capitulo()


        elif opcion == "3":

            mostrar_progreso_escritura()


        elif opcion == "0":

            break


        else:

            print()
            print("Opción no válida.")


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
        print("2 - Estado de la tesis")
        print("3 - Evolucion del proyecto")
        print("4 - Historial de versiones")
        print("5 - Salir de", NOMBRE_APP)


        opcion = input("Elegí una opción: ")


        if opcion == "1":

            analizar_nueva_version()
            

        elif opcion == "2":

            mostrar_estado_tesis()
            
            
        elif opcion == "3":
            
            mostrar_evolucion()
            
        
        elif opcion == "4":
            
            mostrar_historial()
        

        elif opcion == "5":

            print("Cerrando", NOMBRE_APP, "...")
            break


        else:

            print()
            print("* Opción no válida *")


abrir_proyecto()

crear_tabla()
        
mostrar_menu()
