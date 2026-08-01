from config import METRICAS


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