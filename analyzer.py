from docx import Document


# ==============================
#        CONFIGURACIÓN
# ==============================


NIVELES_ESTILO = {

    "Heading 1": 0,
    "Heading 2": 1,
    "Heading 3": 2

}



def abrir_documento(ruta):
    
    return Document(ruta)

# ==============================
#  ANALISIS GRAL DEL DOCUMENTO
# ==============================


def analizar_documento(ruta):

    documento = abrir_documento(ruta)

    texto = ""

    for parrafo in documento.paragraphs:
        texto += parrafo.text + "\n"

    palabras = len(texto.split())
    parrafos = len(documento.paragraphs)
    tablas = len(documento.tables)
    figuras = len(documento.inline_shapes)

    resultado = {
        "palabras": palabras,
        "parrafos": parrafos,
        "tablas": tablas,
        "figuras": figuras
    }

    return resultado


# ==============================
#    DETECCIÓN DE ESTRUCTURA
# ==============================

def obtener_nivel_estilo(estilo):

    if estilo.name in NIVELES_ESTILO:

        return NIVELES_ESTILO[estilo.name]


    if estilo.base_style:

        if estilo.base_style.name in NIVELES_ESTILO:

            return NIVELES_ESTILO[estilo.base_style.name]


    return None



def obtener_secciones(ruta):

    documento = abrir_documento(ruta)

    secciones = []

    for parrafo in documento.paragraphs:

        nivel = obtener_nivel_estilo(parrafo.style)

        if nivel is not None and parrafo.text.strip():

            secciones.append({
                "titulo": parrafo.text,
                "nivel": nivel
            })

    return secciones



def construir_estructura(secciones):

    estructura = []

    capitulo_actual = None
    seccion_actual = None


    for item in secciones:


        if item["nivel"] == 0:

            capitulo_actual = {
                "titulo": item["titulo"],
                "nivel": 0,
                "secciones": []
            }

            estructura.append(capitulo_actual)

            seccion_actual = None


        elif item["nivel"] == 1:

            if capitulo_actual is not None:

                seccion_actual = {
                    "titulo": item["titulo"],
                    "nivel": 1,
                    "subsecciones": []
                }

                capitulo_actual["secciones"].append(
                    seccion_actual
                )


        elif item["nivel"] == 2:

            if seccion_actual is not None:

                seccion_actual["subsecciones"].append(
                    item["titulo"]
                )


    return estructura


def mostrar_estructura(estructura):

    for capitulo in estructura:

        print()
        print(capitulo["titulo"])

        for seccion in capitulo["secciones"]:

            print("   └──", seccion["titulo"])

            for subseccion in seccion["subsecciones"]:

                print("          └──", subseccion)
                

# ==============================
#    ANÁLISIS POR SECCIONES
# ==============================
                
def obtener_palabras_secciones(ruta):

    documento = abrir_documento(ruta)

    secciones = []

    seccion_actual = None

    for parrafo in documento.paragraphs:

        nivel = obtener_nivel_estilo(parrafo.style)
        
        if nivel is not None:

            seccion_actual = {

                "titulo": parrafo.text,
                "nivel": nivel,
                "palabras": 0

            }

            secciones.append(seccion_actual)
            
        else:

            if seccion_actual is not None:

                palabras = len(parrafo.text.split())

                seccion_actual["palabras"] += palabras
                
    return secciones