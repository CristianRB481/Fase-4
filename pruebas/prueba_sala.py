"""Pruebas de ReservaSala."""

from software_fj.sala import ReservaSala
from software_fj.excepciones import ParametroFaltanteError, ServicioInvalidoError


def prueba_sala_valida():
    s = ReservaSala("SAL-1", "Ejecutiva", 50000, capacidad=10)
    assert s.capacidad == 10 and s.disponible
    print("OK  sala válida")


def prueba_costo_sin_extras():
    s = ReservaSala("SAL-1", "Ejecutiva", 50000, capacidad=10)
    assert s.calcular_costo(2) == 100000
    assert s.calcular_costo_total(2) == 119000.0   # con IVA 19 %
    print("OK  costo sin extras")


def prueba_costo_con_extras():
    s = ReservaSala("SAL-2", "Taller", 50000, 8, extras=["proyector"])
    assert s.calcular_costo(2) == 130000           # (50000+15000)*2
    assert s.calcular_costo_total(2) == 154700.0
    print("OK  costo con extras")


def prueba_con_descuento():
    s = ReservaSala("SAL-2", "Taller", 50000, 8, extras=["proyector"])
    assert s.calcular_costo_total(2, descuento=0.1) == 139230.0
    print("OK  costo con descuento")


def prueba_capacidad_negativa():
    try:
        ReservaSala("SAL-3", "Mala", 50000, capacidad=-5)
        print("FALLO")
    except ServicioInvalidoError:
        print("OK  capacidad negativa rechazada")


def prueba_capacidad_faltante():
    try:
        ReservaSala("SAL-4", "Mala", 50000, capacidad=None)
        print("FALLO")
    except ParametroFaltanteError:
        print("OK  capacidad faltante rechazada")


def prueba_extra_inexistente():
    try:
        ReservaSala("SAL-5", "Mala", 50000, 5, extras=["piscina"])
        print("FALLO")
    except ServicioInvalidoError:
        print("OK  extra inexistente rechazado")


def prueba_tarifa_invalida():
    try:
        ReservaSala("SAL-6", "Mala", -100, 5)
        print("FALLO")
    except ServicioInvalidoError:
        print("OK  tarifa negativa rechazada")


def prueba_informacion_y_disponibilidad():
    s = ReservaSala("SAL-7", "Mini", 30000, 4)
    assert "Capacidad: 4" in s.mostrar_informacion()
    s.disponible = False
    assert "no disponible" in s.mostrar_informacion()
    print("OK  información y disponibilidad")


if __name__ == "__main__":
    prueba_sala_valida()
    prueba_costo_sin_extras()
    prueba_costo_con_extras()
    prueba_con_descuento()
    prueba_capacidad_negativa()
    prueba_capacidad_faltante()
    prueba_extra_inexistente()
    prueba_tarifa_invalida()
    prueba_informacion_y_disponibilidad()
    print("\nTodas las pruebas pasaron.")