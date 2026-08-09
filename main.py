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
    obtener_estado_por_capitulo
    )
from visualization import mostrar_grafico_evolucion


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

    series = preparar_series_temporales(evolucion)
    
    mostrar_grafico_evolucion(series)



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
        print("6 - Probar estado de la tesis")


        opcion = input("Elegí una opción: ")


        if opcion == "1":

            analizar_nueva_version()
            

        elif opcion == "2":

            mostrar_ultima_version()
            
            
        elif opcion == "3":
            
            mostrar_historial()
            
        
        elif opcion == "4":
            
            mostrar_evolucion()
        
        
        elif opcion == "6":

            estado = obtener_estado_tesis()

            if estado is None:

                print()
                print("Todavía no hay versiones registradas.")

            else:

                print()
                print("========================================")
                print("           ESTADO DE LA TESIS")
                print("========================================")

                print()
                print("Versión:", estado["version_id"])
                print("Fecha:", estado["fecha"])

                print()
                print("Estadísticas:")
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


                print()
                print("Estado por capítulo:")

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
                

        elif opcion == "5":

            print("Cerrando", NOMBRE_APP, "...")
            break


        else:

            print()
            print("* Opción no válida *")


abrir_proyecto()

"""
estado = obtener_estado_tesis()

if estado:

    estadisticas = calcular_estadisticas_secciones(
        estado["secciones"]
    )

    print()
    print("========================================")
    print("        ESTADO DE LA TESIS")
    print("========================================")

    print()
    print("Última versión:", estado["version_id"])
    print("Fecha:", estado["fecha"])

    print()
    print("Capítulos:", estadisticas["capitulos"])
    print("Secciones:", estadisticas["secciones"])
    print("Subsecciones:", estadisticas["subsecciones"])

    print()

    mas = estadisticas["mas_trabajada"]

    if mas:
        print(
            "Más trabajada:",
            mas[1],
            "-",
            mas[3],
            "palabras"
        )

    menos = estadisticas["menos_trabajada"]

    if menos:
        print(
            "Menos trabajada:",
            menos[1],
            "-",
            menos[3],
            "palabras"
        )


capitulos = obtener_estado_por_capitulo(estado)

print()
print("========================================")
print("          ESTADO POR CAPÍTULO")
print("========================================")

for capitulo in capitulos:

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
"""
"""
from database import conectar, obtener_ultima_version

ultima = obtener_ultima_version()

if ultima:

    version_id = ultima[0]

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
#    SELECT
#        seccion_id,
#        titulo,
#        nivel,
#        palabras
#    FROM secciones
#    WHERE version_id = ?
#    ORDER BY id
#    """, (version_id,))
"""
    registros = cursor.fetchall()

    conexion.close()
    

    capitulo_id = "CAP_007"

    indice = None

    for i, seccion in enumerate(registros):

        if seccion[0] == capitulo_id:

            indice = i
            break


    if indice is not None:

        print()
        print("========================================")
        print("         CONTENIDO DE", capitulo_id)
        print("========================================")

        for seccion in registros[indice:]:

            if (
                seccion[0] != capitulo_id
                and seccion[2] == 0
            ):
                break

            print(
                seccion[0],
                "| nivel:",
                seccion[2],
                "|",
                seccion[1],
                "|",
                seccion[3],
                "palabras"
            )

    else:

        print("No se encontró", capitulo_id)


from stats import describir_seccion

seccion_prueba = estadisticas["menos_trabajada"]

descripcion = describir_seccion(
    seccion_prueba,
    estado["secciones"]
)

print()
print("========================================")
print("        SECCIÓN MENOS TRABAJADA")
print("========================================")

print("Capítulo:", descripcion["capitulo_id"])
print("Título capítulo:", descripcion["capitulo"])
print("Sección:", descripcion["seccion_id"])
print("Título sección:", descripcion["seccion"])
print("Palabras:", descripcion["palabras"])
        
"""
crear_tabla()
        
mostrar_menu()
