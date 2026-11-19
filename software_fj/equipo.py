"""
Módulo equipo de Software FJ.

Define AlquilerEquipo, un servicio especializado que hereda de Servicio.
"""

from software_fj.servicio import Servicio
from software_fj.excepciones import (
    OperacionNoPermitidaError,
    ParametroFaltanteError,
    ServicioInvalidoError,
)

# Recargo por contratar seguro (10 % del costo base).
RECARGO_SEGURO = 0.10


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos tecnológicos."""

    def __init__(self, identificacion, nombre, tarifa_base, tipo_equipo,
                 unidades_disponibles, con_seguro=False):
        # Se guardan ANTES de super() porque Servicio.__init__ llama
        # a validar_parametros(), que usa estos atributos.
        self._tipo_equipo = tipo_equipo
        self._unidades = unidades_disponibles
        self._con_seguro = con_seguro
        # La disponibilidad inicial depende de si hay unidades.
        hay_unidades = isinstance(unidades_disponibles, int) and unidades_disponibles > 0
        super().__init__(identificacion, nombre, tarifa_base, hay_unidades)

    # ---------------------------------------------------------
    # Propiedades (encapsulamiento)
    # ---------------------------------------------------------
    @property
    def tipo_equipo(self):
        """Tipo de equipo que se alquila."""
        return self._tipo_equipo

    @property
    def unidades_disponibles(self):
        """Unidades que quedan para alquilar."""
        return self._unidades

    @property
    def con_seguro(self):
        """Indica si el alquiler incluye seguro."""
        return self._con_seguro

    # ---------------------------------------------------------
    # Métodos propios: control de unidades
    # ---------------------------------------------------------
    def reservar_unidad(self):
        """Descuenta una unidad. Si no quedan, lanza una excepción."""
        if self._unidades <= 0:
            raise OperacionNoPermitidaError(
                f"No quedan unidades de '{self.nombre}'."
            )
        self._unidades -= 1
        # Sin unidades, el servicio deja de estar disponible.
        if self._unidades == 0:
            self._disponible = False

    def liberar_unidad(self):
        """Devuelve una unidad (por ejemplo, al cancelar una reserva)."""
        self._unidades += 1
        self._disponible = True

    # ---------------------------------------------------------
    # Métodos sobrescritos de Servicio (polimorfismo)
    # ---------------------------------------------------------
    def validar_parametros(self):
        """Valida los datos propios de un equipo."""
        # Parámetros faltantes
        if self._tipo_equipo is None or not str(self._tipo_equipo).strip():
            raise ParametroFaltanteError("El tipo de equipo es obligatorio.")
        if self._unidades is None:
            raise ParametroFaltanteError("Las unidades disponibles son obligatorias.")

        # Unidades: entero igual o mayor que cero (bool se descarta)
        if (not isinstance(self._unidades, int)
                or isinstance(self._unidades, bool)
                or self._unidades < 0):
            raise ServicioInvalidoError(
                "Las unidades deben ser un entero mayor o igual a cero."
            )

        # Tarifa: número positivo
        if (not isinstance(self._tarifa_base, (int, float))
                or isinstance(self._tarifa_base, bool)
                or self._tarifa_base <= 0):
            raise ServicioInvalidoError("La tarifa debe ser un número mayor que cero.")

        # Seguro: solo True o False
        if not isinstance(self._con_seguro, bool):
            raise ServicioInvalidoError("El seguro debe ser True o False.")

    def calcular_costo(self, duracion):
        """Costo base: tarifa * horas, más recargo si tiene seguro."""
        costo = self._tarifa_base * duracion
        if self._con_seguro:
            costo += costo * RECARGO_SEGURO
        return costo

    def mostrar_informacion(self):
        """Descripción del equipo."""
        seguro = "con seguro" if self._con_seguro else "sin seguro"
        estado = "disponible" if self._disponible else "no disponible"
        return (f"Equipo {self.nombre} ({self._tipo_equipo}) | "
                f"Unidades: {self._unidades} | "
                f"Tarifa: ${self._tarifa_base:,.0f}/hora | "
                f"{seguro} | {estado}")