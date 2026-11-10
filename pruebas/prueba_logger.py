"""Pruebas del módulo logger."""

from software_fj.logger import ARCHIVO_LOG, registrar_evento, registrar_error


def prueba_registra_evento():
    registrar_evento("PRUEBA evento normal")
    texto = ARCHIVO_LOG.read_text(encoding="utf-8")
    assert "INFO | PRUEBA evento normal" in texto
    print("OK  registra eventos")


def prueba_registra_error():
    registrar_error("PRUEBA error controlado")
    texto = ARCHIVO_LOG.read_text(encoding="utf-8")
    assert "ERROR | PRUEBA error controlado" in texto
    print("OK  registra errores")


def prueba_no_duplica_handlers():
    from software_fj.logger import configurar_logger
    configurar_logger()
    configurar_logger()
    assert len(configurar_logger().handlers) == 1
    print("OK  no duplica handlers")


if __name__ == "__main__":
    prueba_registra_evento()
    prueba_registra_error()
    prueba_no_duplica_handlers()
    print("\nTodas las pruebas pasaron.")