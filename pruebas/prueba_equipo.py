"""Pruebas de AlquilerEquipo."""

from software_fj.equipo import AlquilerEquipo
from software_fj.excepciones import (
    OperacionNoPermitidaError,
    ParametroFaltanteError,
    ServicioInvalidoError,
)


def prueba_equipo_valido():
    e = AlquilerEquipo("EQ-1", "Portátil Dell", 20000, "portátil", 3)
    assert e.unidades_disponibles == 3 and e.disponible
    print("OK  equipo válido")


def prueba_costo_sin_seguro():
    e = AlquilerEquipo("EQ-1", "Portátil Dell", 20000, "portátil", 3)
    assert e.calcular_costo(2) == 40000
    assert e.calcular_costo_total(2) == 47600.0     # con IVA 19 %
    print("OK  costo sin seguro")


def prueba_costo_con_seguro():
    e = AlquilerEquipo("EQ-2", "Cámara", 20000, "cámara", 2, con_seguro=True)
    assert e.calcular_costo(2) == 44000.0           # 40000 + 10 %
    assert e.calcular_costo_total(2) == 52360.0
    print("OK  costo con seguro")


def prueba_con_descuento():
    e = AlquilerEquipo("EQ-1", "Portátil Dell", 20000, "portátil", 3)
    assert e.calcular_costo_total(2, descuento=0.5) == 23800.0
    print("OK  costo con descuento")


def prueba_reservar_hasta_agotar():
    e = AlquilerEquipo("EQ-3", "Proyector", 15000, "proyector", 1)
    e.reservar_unidad()
    assert e.unidades_disponibles == 0 and not e.disponible
    try:
        e.reservar_unidad()
        print("FALLO")
    except OperacionNoPermitidaError:
        print("OK  sin unidades: operación rechazada")


def prueba_liberar_unidad():
    e = AlquilerEquipo("EQ-3", "Proyector", 15000, "proyector", 1)
    e.reservar_unidad()
    e.liberar_unidad()
    assert e.unidades_disponibles == 1 and e.disponible
    print("OK  liberar unidad")


def prueba_unidades_negativas():
    try:
        AlquilerEquipo("EQ-4", "Malo", 15000, "proyector", -2)
        print("FALLO")
    except ServicioInvalidoError:
        print("OK  unidades negativas rechazadas")


def prueba_tipo_faltante():
    try:
        AlquilerEquipo("EQ-5", "Malo", 15000, "", 2)
        print("FALLO")
    except ParametroFaltanteError:
        print("OK  tipo de equipo faltante rechazado")


def prueba_tarifa_invalida():
    try:
        AlquilerEquipo("EQ-6", "Malo", 0, "cámara", 2)
        print("FALLO")
    except ServicioInvalidoError:
        print("OK  tarifa cero rechazada")


def prueba_informacion():
    e = AlquilerEquipo("EQ-7", "Tablet", 10000, "tablet", 5, con_seguro=True)
    texto = e.mostrar_informacion()
    assert "tablet" in texto and "con seguro" in texto
    print("OK  información")


if __name__ == "__main__":
    prueba_equipo_valido()
    prueba_costo_sin_seguro()
    prueba_costo_con_seguro()
    prueba_con_descuento()
    prueba_reservar_hasta_agotar()
    prueba_liberar_unidad()
    prueba_unidades_negativas()
    prueba_tipo_faltante()
    prueba_tarifa_invalida()
    prueba_informacion()
    print("\nTodas las pruebas pasaron.")