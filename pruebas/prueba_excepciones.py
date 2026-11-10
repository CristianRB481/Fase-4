"""Pruebas del módulo excepciones."""

from software_fj.excepciones import (
    SoftwareFJerror,
    DatoInvalidoError,
    ClienteInvalidoError,
    DuracionInvalidaError,
    ClienteDuplicadoError,
    OperacionNoPermitidaError,
)


def prueba_herencia():
    """Verifica que las excepciones respeten la jerarquía diseñada."""
    assert issubclass(ClienteInvalidoError, DatoInvalidoError)
    assert issubclass(DuracionInvalidaError, DatoInvalidoError)
    assert issubclass(DatoInvalidoError, SoftwareFJerror)
    assert issubclass(ClienteDuplicadoError, SoftwareFJerror)
    print("OK  herencia")


def prueba_captura_por_base():
    """Una excepción hija debe poder capturarse con su clase base."""
    try:
        raise ClienteInvalidoError("Correo inválido")
    except DatoInvalidoError as e:
        assert str(e) == "Correo inválido"
        print("OK  captura por clase base")


def prueba_mensaje_por_defecto():
    """Sin mensaje, la excepción usa el texto por defecto."""
    try:
        raise SoftwareFJerror()
    except SoftwareFJerror as e:
        assert "Software_fj" in str(e)
        print("OK  mensaje por defecto")


def prueba_encadenamiento():
    """raise ... from e conserva el error original en __cause__."""
    try:
        try:
            int("abc")
        except ValueError as e:
            raise DuracionInvalidaError("Duración no numérica") from e
    except DuracionInvalidaError as error:
        assert isinstance(error.__cause__, ValueError)
        print("OK  encadenamiento")


def prueba_excepciones_independientes():
    """Una excepción no debe capturarse con una clase que no es su ancestro."""
    try:
        try:
            raise OperacionNoPermitidaError("Ya cancelada")
        except DatoInvalidoError:
            print("FALLO: no debió capturarse aquí")
    except OperacionNoPermitidaError:
        print("OK  excepciones independientes")


if __name__ == "__main__":
    prueba_herencia()
    prueba_captura_por_base()
    prueba_mensaje_por_defecto()
    prueba_encadenamiento()
    prueba_excepciones_independientes()
    print("\nTodas las pruebas pasaron.")