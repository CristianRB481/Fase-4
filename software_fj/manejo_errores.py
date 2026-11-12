"""
manejo_errores.py - Utilidades para ejecutar operaciones de forma segura.

Fase 4 - Programación (213023): estabilidad, robustez y manejo de errores.

Qué aporta este módulo:
  1. ejecutar_seguro: ejecuta una operación con try/except/else/finally,
     registra el resultado en el log y NO deja que el programa se caiga.
  2. reintentar: decorador que repite una operación si falla.
  3. ejecutar_lote: corre varias operaciones (ideal para simulacion.py)
     y entrega un resumen de cuáles salieron bien y cuáles fallaron.

Nota para el equipo: ErrorOperacion se define aquí para que el archivo
funcione solo. Si en excepciones.py ya hay una excepción base del proyecto,
se puede reemplazar por esa (ver comentario en la clase).
"""

import functools
import logging
import time

# Se usa el logging estándar. Si logger.py ya configura un logger propio,
# basta con cambiar esta línea por: from software_fj.logger import logger
logger = logging.getLogger("software_fj")


class ErrorOperacion(Exception):
    """Error que envuelve cualquier fallo inesperado de una operación.

    Si excepciones.py tiene una clase base (por ejemplo ErrorSoftwareFJ),
    esta clase puede heredar de ella en lugar de Exception.
    """


def ejecutar_seguro(operacion, *args, valor_por_defecto=None, **kwargs):
    """Ejecuta `operacion(*args, **kwargs)` sin que el programa se caiga.

    Devuelve una tupla (exito, resultado):
      - (True, resultado) si todo salió bien.
      - (False, valor_por_defecto) si hubo un error (queda registrado en el log).
    """
    nombre = getattr(operacion, "__name__", str(operacion))
    try:
        # Intento principal
        resultado = operacion(*args, **kwargs)
    except (ValueError, TypeError, KeyError) as error:
        # Errores de datos: el usuario o el sistema envió algo inválido
        logger.error("Datos inválidos en '%s': %s", nombre, error)
        return False, valor_por_defecto
    except Exception as error:
        # Cualquier otro error inesperado se registra con su traza completa
        logger.exception("Error inesperado en '%s'", nombre)
        return False, valor_por_defecto
    else:
        # Solo se ejecuta si NO hubo excepción
        logger.info("Operación '%s' completada correctamente", nombre)
        return True, resultado
    finally:
        # Se ejecuta siempre, haya o no error
        logger.debug("Fin de la operación '%s'", nombre)


def reintentar(intentos=3, espera=0.5, excepciones=(Exception,)):
    """Decorador: repite la función hasta `intentos` veces si falla.

    Si agota los intentos lanza ErrorOperacion encadenando el error original
    (raise ... from ...), así no se pierde la causa real.
    """

    def decorador(funcion):
        @functools.wraps(funcion)
        def envoltura(*args, **kwargs):
            ultimo_error = None
            for numero in range(1, intentos + 1):
                try:
                    return funcion(*args, **kwargs)
                except excepciones as error:
                    ultimo_error = error
                    logger.warning(
                        "Intento %d/%d de '%s' falló: %s",
                        numero, intentos, funcion.__name__, error,
                    )
                    if numero < intentos:
                        time.sleep(espera)
            raise ErrorOperacion(
                f"'{funcion.__name__}' falló tras {intentos} intentos"
            ) from ultimo_error

        return envoltura

    return decorador


def ejecutar_lote(operaciones):
    """Ejecuta una lista de operaciones y devuelve un resumen.

    `operaciones` es una lista de tuplas (descripcion, funcion, args, kwargs).
    Una operación que falle NO detiene a las demás.

    Devuelve un diccionario con 'exitosas', 'fallidas' y 'detalle'.
    """
    detalle = []
    for descripcion, funcion, args, kwargs in operaciones:
        exito, resultado = ejecutar_seguro(funcion, *args, **kwargs)
        detalle.append({"operacion": descripcion, "exito": exito, "resultado": resultado})

    exitosas = sum(1 for item in detalle if item["exito"])
    return {
        "exitosas": exitosas,
        "fallidas": len(detalle) - exitosas,
        "detalle": detalle,
    }
