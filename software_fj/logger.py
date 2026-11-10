"""
Módulo de registro (logs) de Software FJ.

Guarda eventos (INFO) y errores (ERROR) en logs/software_fj.log.
Es el único uso de archivos permitido en el proyecto.
"""

import logging
from pathlib import Path

CARPETA_LOGS = Path("logs")
ARCHIVO_LOG = CARPETA_LOGS / "software_fj.log"
NOMBRE_LOGGER = "software_fj"


def configurar_logger():
    """Crea (una sola vez) y devuelve el logger del sistema."""
    logger = logging.getLogger(NOMBRE_LOGGER)

    # Evita agregar handlers duplicados si se llama varias veces
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    try:
        CARPETA_LOGS.mkdir(exist_ok=True)
        manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
    except OSError:
        # Si no se puede escribir el archivo, el programa no se detiene
        manejador = logging.StreamHandler()

    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    manejador.setFormatter(formato)
    logger.addHandler(manejador)
    return logger


logger = configurar_logger()


def registrar_evento(mensaje):
    """Registra un evento normal del sistema (nivel INFO)."""
    logger.info(mensaje)


def registrar_error(mensaje):
    """Registra un error controlado del sistema (nivel ERROR)."""
    logger.error(mensaje)