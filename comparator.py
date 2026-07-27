from config import METRICAS

def comparar_metricas(actual, anterior):

    cambios = {}

    for metrica, info in METRICAS.items():
        
        cambios[metrica] = (actual[info["db"]] - anterior[info["db"]])
    
    return cambios


def mostrar_cambios(cambios):

    print()
    print("===================================")
    print("CAMBIOS DESDE ÚLTIMA VERSIÓN")
    print("===================================")


    for metrica, info in METRICAS.items():

        print()
        print(info["nombre"],
              ":",
              f"{cambios[metrica]:+}"
        )

    print()