"""
Módulo servicio de Software FJ.

Define la clase abstracta Servicio, molde común de los tres servicios
de la empresa: reserva de salas, alquiler de equipos y asesorías.
"""

from abc import abstractmethod

from software_fj.entidad import Entidad
from software_fj.excepciones import (
    CalculoInconsistenteError,
    DuracionInvalidaError,
    ParametroFaltanteError,
)

# Tasa de IVA vigente en Colombia (19 %). Se define una sola vez para
# poder cambiarla en un único lugar.
TASA_IVA = 0.19

# Correo genérico: Entidad exige un correo, pero un servicio no tiene.
# PARCHE TEMPORAL: se elimina si Entidad deja de pedir correo.
CORREO_EMPRESA = "servicios@softwarefj.com"


class Servicio(Entidad):
    """Clase abstracta que representa un servicio de Software FJ.

    No se puede instanciar directamente (Servicio() da error): solo
    sirve de molde para SalaReserva, AlquilerEquipo y Asesoria.
    """

    def __init__(self, identificacion, nombre, tarifa_base, disponible=True):
        # Validamos antes de construir el objeto: si falta el nombre
        # o la tarifa, se lanza una excepción personalizada.
        if nombre is None or not str(nombre).strip():
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        if tarifa_base is None:
            raise ParametroFaltanteError("La tarifa base es obligatoria.")

        # Encapsulamiento: atributos protegidos (un guion bajo) y
        # acceso mediante propiedades.
        super().__init__(identificacion, str(nombre).strip(), CORREO_EMPRESA)
        self._tarifa_base = tarifa_base
        self._disponible = disponible

        # Cada hija valida sus propios datos (método abstracto).
        self.validar_parametros()

    # ---------------------------------------------------------
    # Propiedades (encapsulamiento)
    # ---------------------------------------------------------
    @property
    def tarifa_base(self):
        """Tarifa por hora del servicio."""
        return self._tarifa_base

    @property
    def disponible(self):
        """Indica si el servicio se puede reservar."""
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        if not isinstance(valor, bool):
            raise ParametroFaltanteError("La disponibilidad debe ser True o False.")
        self._disponible = valor

    # ---------------------------------------------------------
    # Métodos abstractos: cada servicio hijo DEBE sobrescribirlos
    # ---------------------------------------------------------
    @abstractmethod
    def calcular_costo(self, duracion):
        """Costo base del servicio (sin impuesto ni descuento)."""

    @abstractmethod
    def mostrar_informacion(self):
        """Descripción del servicio (nombre dado por Entidad)."""

    @abstractmethod
    def validar_parametros(self):
        """Valida los datos propios de cada servicio."""

    # ---------------------------------------------------------
    # Método concreto con parámetros opcionales ("sobrecarga")
    # ---------------------------------------------------------
    def calcular_costo_total(self, duracion, descuento=0.0, impuesto=TASA_IVA):
        """Calcula el costo final: base - descuento + impuesto.

        Python no tiene sobrecarga clásica; se logra con parámetros
        opcionales:
            calcular_costo_total(2)                 -> solo IVA
            calcular_costo_total(2, descuento=0.1)  -> 10 % de descuento
            calcular_costo_total(2, impuesto=0)     -> sin impuesto
        """
        # Validamos la duración
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool):
            raise DuracionInvalidaError("La duración debe ser un número.")
        if duracion <= 0:
            raise DuracionInvalidaError("La duración debe ser mayor que cero.")

        # Validamos que el descuento y el impuesto tengan sentido
        if not 0 <= descuento <= 1:
            raise CalculoInconsistenteError(
                "El descuento debe estar entre 0 y 1 (0 % a 100 %)."
            )
        if impuesto < 0:
            raise CalculoInconsistenteError("El impuesto no puede ser negativo.")

        base = self.calcular_costo(duracion)       # polimorfismo
        con_descuento = base * (1 - descuento)
        total = con_descuento * (1 + impuesto)

        if total < 0:
            raise CalculoInconsistenteError("El total calculado es negativo.")
        return round(total, 2)