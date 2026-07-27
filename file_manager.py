import os
import shutil
from datetime import datetime
from config import VERSIONS_DIR


def guardar_version(ruta):

    fecha = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    nombre = os.path.basename(ruta)

    archivo_destino = os.path.join(
        VERSIONS_DIR,
        f"{fecha}_{nombre}"
    )

    os.makedirs(VERSIONS_DIR, exist_ok = True)
    
    shutil.copy(ruta, archivo_destino)

    return archivo_destino