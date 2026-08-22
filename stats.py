from config import METRICAS, TITULOS_REFERENCIAS, SECCIONES_EXCLUIDAS_ESTADISTICAS, MIN_PALABRAS_PROGRESO
from database import conectar, obtener_ultima_version


def preparar_series_temporales(evolucion):

    series = {

        "versiones": [],
        "fechas": []

    }

    for metrica in METRICAS:

        series[metrica] = []


    for version in evolucion:

        series["versiones"].append(
            version["id"]
        )

        series["fechas"].append(
            version["fecha"]
        )


        for metrica in METRICAS:

            series[metrica].append(
                version[metrica]
            )


    return series



def obtener_estado_tesis():

    ultima = obtener_ultima_version()

    if not ultima:
        return None

    version_id = ultima[0]

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
    SELECT
        seccion_id,
        titulo,
        nivel,
        palabras,
        parrafos,
        paginas,
        tablas,
        figuras,
        referencias
    FROM secciones
    WHERE version_id = ?
    ORDER BY id
    """, (version_id,))

    secciones = cursor.fetchall()

    conexion.close()
    
    
    # ESTADISTICAS DE LAS SECCIONES
    
    estadisticas = calcular_estadisticas_secciones(
        secciones
    )
    
    
    # DESCRIBIR MAS Y MENOS TRABAJADAS
    
    if estadisticas["mas_trabajada"] is not None:
        
        estadisticas["mas_trabajada"] = describir_seccion(
            estadisticas["mas_trabajada"],
            secciones
        )
        
    
    if estadisticas["menos_trabajada"] is not None:
        
        estadisticas["menos_trabajada"] = describir_seccion(
            estadisticas["menos_trabajada"],
            secciones
        )
        
        
    # ESTADO POR CAPITULO
    
    estado_por_capitulo = obtener_estado_por_capitulo({
        "version_id": version_id,
        "secciones": secciones
    })
    
    
    # RESULTADO FINAL

    estado = {

        "version_id": version_id,

        "fecha": ultima[1],

        "secciones": secciones,
        
        "estadisticas": estadisticas,
        
        "capitulos": estado_por_capitulo

    }

    return estado



def es_seccion_relevante(seccion):

    titulo = seccion[1].strip().lower()
    nivel = seccion[2]
    palabras = seccion[3]

    if nivel == 0:
        return False

    if palabras <= MIN_PALABRAS_PROGRESO:
        return False
    
    for titulo_referencia in TITULOS_REFERENCIAS:
        
        if titulo_referencia.lower() in titulo:
            return False
    
    for seccion_excluida in SECCIONES_EXCLUIDAS_ESTADISTICAS:
        
        if seccion_excluida.lower() in titulo:
            return False
    
    return True




def calcular_estadisticas_secciones(secciones):

    capitulos = 0
    secciones_normales = 0
    subsecciones = 0

    for seccion in secciones:

        nivel = seccion[2]

        if nivel == 0:
            capitulos += 1

        elif nivel == 1:
            secciones_normales += 1

        elif nivel == 2:
            subsecciones += 1


    secciones_relevantes = [
        seccion
        for seccion in secciones
        if es_seccion_relevante(seccion)
    ]


    if secciones_relevantes:

        mas_trabajada = max(
            secciones_relevantes,
            key=lambda x: x[3]
        )

        menos_trabajada = min(
            secciones_relevantes,
            key=lambda x: x[3]
        )

    else:

        mas_trabajada = None
        menos_trabajada = None


    return {

        "capitulos": capitulos,

        "secciones": secciones_normales,

        "subsecciones": subsecciones,

        "mas_trabajada": mas_trabajada,

        "menos_trabajada": menos_trabajada

    }



def calcular_ritmo_versiones(evolucion):

    cambios = []

    for i in range(1, len(evolucion)):

        anterior = evolucion[i - 1]
        actual = evolucion[i]

        cambio = (
            actual["palabras"]
            - anterior["palabras"]
        )

        cambios.append({
            "version_anterior": anterior["id"],
            "version": actual["id"],
            "cambio_palabras": cambio
        })


    if not cambios:

        return None


    promedio = (
        sum(cambio["cambio_palabras"] for cambio in cambios)
        / len(cambios)
    )


    mayor = max(
        cambios,
        key=lambda x: x["cambio_palabras"]
    )

    menor = min(
        cambios,
        key=lambda x: x["cambio_palabras"]
    )


    return {
        "cambios": cambios,
        "promedio": promedio,
        "mayor": mayor,
        "menor": menor
    }



def obtener_metricas_capitulo(version_id, capitulo_id):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
    SELECT
        seccion_id,
        titulo,
        nivel,
        palabras,
        parrafos,
        paginas,
        tablas,
        figuras,
        referencias
    FROM secciones
    WHERE version_id = ?
    ORDER BY id
    """, (version_id,))

    registros = cursor.fetchall()

    conexion.close()


    # --------------------------------
    # ENCONTRAR EL CAPÍTULO
    # --------------------------------

    indice_capitulo = None

    for i, seccion in enumerate(registros):

        if seccion[0] == capitulo_id:

            indice_capitulo = i
            break


    if indice_capitulo is None:

        return None


    # --------------------------------
    # OBTENER LAS SECCIONES
    # DEL CAPÍTULO
    # --------------------------------

    contenido_capitulo = []

    for seccion in registros[indice_capitulo:]:

        # Si encontramos otro capítulo,
        # terminó el capítulo actual.

        if (
            seccion[0] != capitulo_id
            and seccion[2] == 0
        ):
            break

        contenido_capitulo.append(seccion)


    # --------------------------------
    # IDENTIFICAR LAS HOJAS
    # --------------------------------

    hojas = []

    for i, seccion in enumerate(contenido_capitulo):

        nivel = seccion[2]

        # Buscamos si existe una sección
        # inmediatamente posterior con
        # un nivel mayor.

        tiene_hijas = False

        for siguiente in contenido_capitulo[i + 1:]:

            nivel_siguiente = siguiente[2]

            # Si vuelve a un nivel igual o menor,
            # ya no estamos dentro de esta sección.

            if nivel_siguiente <= nivel:
                break

            if nivel_siguiente > nivel:

                tiene_hijas = True
                break


        if not tiene_hijas:

            hojas.append(seccion)


    # --------------------------------
    # SUMAR MÉTRICAS DE LAS HOJAS
    # --------------------------------

    metricas = {}

    for metrica in METRICAS:

        metricas[metrica] = 0


    for hoja in hojas:

        for i, metrica in enumerate(METRICAS, start=3):

            metricas[metrica] += hoja[i]


    return metricas



def obtener_estado_por_capitulo(estado):

    version_id = estado["version_id"]
    secciones = estado["secciones"]

    capitulos = []

    for seccion in secciones:

        # Solo nos interesan los capítulos
        if seccion[2] != 0:
            continue

        capitulo_id = seccion[0]
        titulo = seccion[1]

        metricas = obtener_metricas_capitulo(
            version_id,
            capitulo_id
        )

        capitulos.append({
            "id": capitulo_id,
            "titulo": titulo,
            "metricas": metricas
        })

    return capitulos



def obtener_capitulo_de_seccion(secciones, seccion):

    indice_seccion = secciones.index(seccion)

    capitulo = None

    for item in secciones[:indice_seccion + 1]:

        if item[2] == 0:

            capitulo = item

    return capitulo



def describir_seccion(seccion, secciones):

    if seccion is None:
        return None

    capitulo = obtener_capitulo_de_seccion(
        secciones,
        seccion
    )

    return {

        "capitulo_id": capitulo[0] if capitulo else None,

        "capitulo": capitulo[1] if capitulo else None,

        "seccion_id": seccion[0],

        "seccion": seccion[1],

        "palabras": seccion[3]

    }