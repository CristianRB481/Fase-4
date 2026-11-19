"""
Módulo sala de Software FJ.

Define ReservaSala, un servicio especializado que hereda de Servicio.
"""

from software_fj.servicio import Servicio
from software_fj.excepciones import ParametroFaltanteError, ServicioInvalidoError

# Extras disponibles y su costo por hora (en pesos colombianos).
# Es un diccionario: clave = nombre del extra, valor = costo por hora.
EXTRAS_DISPONIBLES = {
    "proyector": 15000,
    "videoconferencia": 20000,
    "pizarra": 5000,
}


class ReservaSala(Servicio):
    """Servicio de reserva de salas de reuniones."""

    def __init__(self, identificacion, nombre, tarifa_base, capacidad,
                 extras=None, disponible=True):
        # IMPORTANTE: Servicio.__init__ llama a validar_parametros(),
        # así que estos atributos se guardan ANTES de llamar a super().
        self._capacidad = capacidad
        # extras es opcional: si no llega, se usa una lista vacía.
        # (No usamos extras=[] como valor por defecto porque la lista
        # se compartiría entre objetos: es un error clásico de Python.)
        self._extras = list(extras) if extras else []
        super().__init__(identificacion, nombre, tarifa_base, disponible)

    # ---------------------------------------------------------
    # Propiedades (encapsulamiento)
    # ---------------------------------------------------------
    @property
    def capacidad(self):
        """Número máximo de personas de la sala."""
        return self._capacidad

    @property
    def extras(self):
        """Copia de los extras contratados (evita modificar la original)."""
        return list(self._extras)

    # ---------------------------------------------------------
    # Métodos sobrescritos de Servicio (polimorfismo)
    # ---------------------------------------------------------
    def validar_parametros(self):
        """Valida los datos propios de una sala."""
        # Parámetro faltante
        if self._capacidad is None:
            raise ParametroFaltanteError("La capacidad de la sala es obligatoria.")

        # Capacidad: entero positivo (bool es subclase de int, se descarta)
        if (not isinstance(self._capacidad, int)
                or isinstance(self._capacidad, bool)
                or self._capacidad <= 0):
            raise ServicioInvalidoError(
                "La capacidad debe ser un número entero mayor que cero."
            )

        # Tarifa: número positivo
        if (not isinstance(self._tarifa_base, (int, float))
                or isinstance(self._tarifa_base, bool)
                or self._tarifa_base <= 0):
            raise ServicioInvalidoError("La tarifa debe ser un número mayor que cero.")

        # Extras: solo los que existen en el catálogo
        for extra in self._extras:
            if extra not in EXTRAS_DISPONIBLES:
                raise ServicioInvalidoError(f"El extra '{extra}' no existe.")

    def calcular_costo(self, duracion):
        """Costo base: (tarifa por hora + extras por hora) * horas."""
        costo_extras = sum(EXTRAS_DISPONIBLES[e] for e in self._extras)
        return (self._tarifa_base + costo_extras) * duracion

    def mostrar_informacion(self):
        """Descripción de la sala."""
        extras = ", ".join(self._extras) if self._extras else "ninguno"
        estado = "disponible" if self._disponible else "no disponible"
        return (f"Sala {self.nombre} | Capacidad: {self._capacidad} personas | "
                f"Tarifa: ${self._tarifa_base:,.0f}/hora | "
                f"Extras: {extras} | {estado}")