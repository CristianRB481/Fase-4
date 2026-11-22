"""
Simulación de 13 operaciones de Software FJ (éxitos y fallos).

Cada operación se ejecuta dentro de ejecutar(): si falla, el error se
muestra y se registra, y el programa CONTINÚA con la siguiente.
"""

from software_fj.gestor import GestorSoftwareFJ
from software_fj.sala import ReservaSala
from software_fj.equipo import AlquilerEquipo
from software_fj.asesoria import AsesoriaEspecializada
from software_fj.excepciones import SoftwareFJError
from software_fj.logger import registrar_evento, registrar_error


def ejecutar(numero, descripcion, accion):
    """Corre una operación sin dejar que un error detenga el programa."""
    print(f"\n[{numero:02d}] {descripcion}")
    try:
        resultado = accion()
    except SoftwareFJError as error:
        print(f"     ERROR CONTROLADO ({type(error).__name__}): {error}")
        if error.__cause__ is not None:
            print(f"     causa original: {error.__cause__!r}")
        return None
    except Exception as error:  # error inesperado: se registra y se sigue
        registrar_error(f"Error inesperado en operación {numero}: {error!r}")
        print(f"     ERROR INESPERADO: {error!r}")
        return None
    print(f"     OK: {resultado}")
    return resultado


def ejecutar_simulacion():
    gestor = GestorSoftwareFJ()
    registrar_evento("=== Inicio de la simulación ===")

    ejecutar(1, "Registrar cliente válido",
             lambda: gestor.registrar_cliente(
                 "1001", "Juan Pérez", "juan@correo.com", "3001234567", "Calle 10 #5-20"
             ).nombre)
    ejecutar(2, "Registrar cliente con correo inválido",
             lambda: gestor.registrar_cliente(
                 "1002", "Ana Gómez", "ana.correo", "3007654321", "Carrera 7 #1-10"))
    ejecutar(3, "Registrar cliente con documento duplicado",
             lambda: gestor.registrar_cliente(
                 "1001", "Otro Nombre", "otro@correo.com", "3009998888", "Calle 1 #1-1"))

    ejecutar(4, "Crear sala válida",
             lambda: gestor.agregar_servicio(
                 ReservaSala("SAL-1", "Sala Ejecutiva", 50000, 10, extras=["proyector"]))
             .mostrar_informacion())
    ejecutar(5, "Crear sala con capacidad negativa",
             lambda: gestor.agregar_servicio(ReservaSala("SAL-2", "Sala Mala", 50000, -5)))

    ejecutar(6, "Crear equipo y asesoría válidos",
             lambda: (gestor.agregar_servicio(
                          AlquilerEquipo("EQ-1", "Portátil Dell", 20000, "portátil", 2)).nombre,
                      gestor.agregar_servicio(
                          AsesoriaEspecializada("ASE-1", "Python", 40000, "Ana Pérez")).nombre))
    ejecutar(7, "Crear asesoría sin especialista",
             lambda: gestor.agregar_servicio(
                 AsesoriaEspecializada("ASE-2", "Redes", 40000, "")))

    num = ejecutar(8, "Reserva exitosa con IVA y descuento del 10 %",
                   lambda: gestor.crear_reserva("1001", "SAL-1", 2))
    if num:
        ejecutar(8, "   Total de la reserva (descuento 10 %)",
                 lambda: gestor.calcular_total(num, descuento=0.1))

    ejecutar(9, "Reserva con duración 0",
             lambda: gestor.crear_reserva("1001", "SAL-1", 0))

    gestor.agregar_servicio(
        ReservaSala("SAL-3", "Sala en mantenimiento", 40000, 6, disponible=False))
    ejecutar(10, "Reserva de un servicio no disponible",
             lambda: gestor.crear_reserva("1001", "SAL-3", 1))

    num2 = ejecutar(11, "Crear, confirmar y cancelar una reserva",
                    lambda: gestor.crear_reserva("1001", "EQ-1", 3))
    if num2:
        ejecutar(11, "   Confirmar", lambda: gestor.confirmar_reserva(num2))
        ejecutar(11, "   Cancelar", lambda: gestor.cancelar_reserva(num2, "Cliente desistió"))
        ejecutar(12, "Cancelar una reserva ya cancelada",
                 lambda: gestor.cancelar_reserva(num2))

    if num:
        ejecutar(13, "Descuento del 150 %",
                 lambda: gestor.calcular_total(num, descuento=1.5))

    registrar_evento("=== Fin de la simulación ===")
    print("\nSimulación terminada. Revisa logs/software_fj.log")