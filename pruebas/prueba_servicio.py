"""Pruebas de la clase abstracta Servicio."""

from software_fj.servicio import Servicio
from software_fj.excepciones import (
    CalculoInconsistenteError,
    DuracionInvalidaError,
    ParametroFaltanteError,
)


class ServicioPrueba(Servicio):
    """Hija mínima solo para probar (costo = tarifa * duración)."""

    def calcular_costo(self, duracion):
        return self.tarifa_base * duracion

    def mostrar_informacion(self):
        return f"Prueba: {self.nombre}"

    def validar_parametros(self):
        pass


def prueba_no_se_instancia():
    try:
        Servicio("S1", "X", 100)  # pyright: ignore[reportAbstractUsage]
        print("FALLO: no debió crearse")
    except TypeError:
        print("OK  Servicio es abstracta")


def prueba_costo_con_iva():
    s = ServicioPrueba("S1", "Sala", 100)
    assert s.calcular_costo_total(2) == 238.0   # 200 * 1.19
    print("OK  costo con IVA")


def prueba_descuento():
    s = ServicioPrueba("S1", "Sala", 100)
    assert s.calcular_costo_total(2, descuento=0.5) == 119.0
    print("OK  descuento")


def prueba_sin_impuesto():
    s = ServicioPrueba("S1", "Sala", 100)
    assert s.calcular_costo_total(2, impuesto=0) == 200.0
    print("OK  sin impuesto")


def prueba_descuento_invalido():
    s = ServicioPrueba("S1", "Sala", 100)
    try:
        s.calcular_costo_total(2, descuento=1.5)
        print("FALLO")
    except CalculoInconsistenteError:
        print("OK  descuento 150 % rechazado")


def prueba_duracion_invalida():
    s = ServicioPrueba("S1", "Sala", 100)
    try:
        s.calcular_costo_total(0)
        print("FALLO")
    except DuracionInvalidaError:
        print("OK  duración 0 rechazada")


def prueba_parametro_faltante():
    try:
        ServicioPrueba("S1", "", 100)
        print("FALLO")
    except ParametroFaltanteError:
        print("OK  nombre vacío rechazado")


if __name__ == "__main__":
    prueba_no_se_instancia()
    prueba_costo_con_iva()
    prueba_descuento()
    prueba_sin_impuesto()
    prueba_descuento_invalido()
    prueba_duracion_invalida()
    prueba_parametro_faltante()
    print("\nTodas las pruebas pasaron.")