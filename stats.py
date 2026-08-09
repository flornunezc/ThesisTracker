from config import METRICAS
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

    estado = {

        "version_id": version_id,

        "fecha": ultima[1],

        "secciones": secciones

    }

    return estado



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


    secciones_con_palabras = [
        seccion
        for seccion in secciones
        if seccion[3] > 0
    ]


    if secciones_con_palabras:

        mas_trabajada = max(
            secciones_con_palabras,
            key=lambda x: x[3]
        )

        menos_trabajada = min(
            secciones_con_palabras,
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