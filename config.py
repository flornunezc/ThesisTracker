NOMBRE_APP = "ThesisTracker"

VERSION = "0.9"

AUTOR = "Florencia Nunez C"


import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ACTIVE_PROJECT = "ProyectoActual"

PROJECT_DIR = os.path.join(
    BASE_DIR,
    "projects",
    ACTIVE_PROJECT
)

VERSIONS_DIR = os.path.join(PROJECT_DIR, "versions")

REPORTS_DIR = os.path.join(PROJECT_DIR, "reports")

DATA_DIR = os.path.join(PROJECT_DIR, "data")

DATABASE_PATH = os.path.join(DATA_DIR, "thesis_tracker.db")

PALABRAS_POR_PAGINA = 450

METRICAS = {

    "palabras": {
        "nombre": "Palabras",
        "db": "palabras"
    },

    "parrafos": {
        "nombre": "Párrafos",
        "db": "parrafos"
    },
    
    "paginas": {
        "nombre": "Páginas",
        "db": "paginas"
    },

    "tablas": {
        "nombre": "Tablas",
        "db": "tablas"
    },

    "figuras": {
        "nombre": "Figuras",
        "db": "figuras"
    },
    
    "referencias": {
        "nombre": "Referencias",
        "db": "referencias"
    }

}


TITULOS_REFERENCIAS = [
    "referencias",
    "referencias bibliográficas",
    "bibliografía",
    "bibliografia",
    "references",
    "literature cited",
    "works cited"
]


SECCIONES_EXCLUIDAS_ESTADISTICAS = [
    TITULOS_REFERENCIAS,
    "anexos",
    "anexo"
]

from pathlib import Path

def asegurar_estructura_proyecto():
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
    Path(VERSIONS_DIR).mkdir(parents=True, exist_ok=True)
    Path(REPORTS_DIR).mkdir(parents=True, exist_ok=True)    