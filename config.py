NOMBRE_PROYECTO = "ThesisTracker"

VERSION = "0.7"

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

DATABASE_PATH = os.path.join(PROJECT_DIR, "data", "thesis_tracker.db")

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