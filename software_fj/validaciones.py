import re


def validar_identificacion(identificacion):
    """Verifica que la identificación contenga entre 5 y 15 dígitos."""

    identificacion = str(identificacion).strip()

    if not identificacion.isdigit():
        return False

    if not (5 <= len(identificacion) <= 15):
        return False

    return True


def validar_nombre(nombre):
    """Verifica que el nombre no esté vacío y contenga solo letras y espacios."""

    if not isinstance(nombre, str):
        return False

    nombre = nombre.strip()

    if len(nombre) < 2:
        return False

    if not all(letra.isalpha() or letra.isspace() for letra in nombre):
        return False

    return True


def validar_correo(correo):
    """Verifica que el correo tenga un formato válido."""

    if not isinstance(correo, str):
        return False

    patron = r'^[\w.+-]+@[\w-]+\.[\w.-]+$'

    return re.match(patron, correo) is not None
