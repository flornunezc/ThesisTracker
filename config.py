NOMBRE_APP = "ThesisTracker"

VERSION = "0.8"

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

METRICAS = {

    "palabras": {
        "nombre": "Palabras",
        "db": "palabras"
    },

    "parrafos": {
        "nombre": "Párrafos",
        "db": "parrafos"
    },

    "tablas": {
        "nombre": "Tablas",
        "db": "tablas"
    },

    "figuras": {
        "nombre": "Figuras",
        "db": "figuras"
    }

}


from pathlib import Path

def asegurar_estructura_proyecto():
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
    Path(VERSIONS_DIR).mkdir(parents=True, exist_ok=True)
    Path(REPORTS_DIR).mkdir(parents=True, exist_ok=True)    