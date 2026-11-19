"""
Módulo asesoria de Software FJ.

Define AsesoriaEspecializada, un servicio que hereda de Servicio.
"""

from software_fj.servicio import Servicio
from software_fj.excepciones import ParametroFaltanteError, ServicioInvalidoError

# Factor que multiplica la tarifa según el nivel de la asesoría.
FACTOR_NIVEL = {
    "basico": 1.0,
    "intermedio": 1.5,
    "avanzado": 2.0,
}

# Recargo por pedir la asesoría con urgencia (25 % del costo).
RECARGO_URGENTE = 0.25


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría con un especialista."""

    def __init__(self, identificacion, nombre, tarifa_base, especialista,
                 nivel="basico", urgente=False, disponible=True):
        # Se guardan ANTES de super() porque Servicio.__init__ llama
        # a validar_parametros(), que usa estos atributos.
        self._especialista = especialista
        # Normalizamos el nivel a minúsculas (si es texto) para comparar.
        self._nivel = nivel.strip().lower() if isinstance(nivel, str) else nivel
        self._urgente = urgente
        super().__init__(identificacion, nombre, tarifa_base, disponible)

    # ---------------------------------------------------------
    # Propiedades (encapsulamiento)
    # ---------------------------------------------------------
    @property
    def especialista(self):
        """Nombre del especialista que da la asesoría."""
        return self._especialista

    @property
    def nivel(self):
        """Nivel de la asesoría (basico, intermedio, avanzado)."""
        return self._nivel

    @property
    def urgente(self):
        """Indica si la asesoría es urgente."""
        return self._urgente

    # ---------------------------------------------------------
    # Métodos sobrescritos de Servicio (polimorfismo)
    # ---------------------------------------------------------
    def validar_parametros(self):
        """Valida los datos propios de una asesoría."""
        # Parámetro faltante: el especialista es obligatorio
        if self._especialista is None or not str(self._especialista).strip():
            raise ParametroFaltanteError("El especialista es obligatorio.")

        # Nivel: debe existir en el catálogo
        if self._nivel not in FACTOR_NIVEL:
            raise ServicioInvalidoError(
                f"Nivel inválido. Opciones: {', '.join(FACTOR_NIVEL)}."
            )

        # Tarifa: número positivo (bool se descarta)
        if (not isinstance(self._tarifa_base, (int, float))
                or isinstance(self._tarifa_base, bool)
                or self._tarifa_base <= 0):
            raise ServicioInvalidoError("La tarifa debe ser un número mayor que cero.")

        # Urgente: solo True o False
        if not isinstance(self._urgente, bool):
            raise ServicioInvalidoError("El campo urgente debe ser True o False.")

    def calcular_costo(self, duracion):
        """Costo base: tarifa * horas * factor del nivel, más recargo si es urgente."""
        costo = self._tarifa_base * duracion * FACTOR_NIVEL[self._nivel]
        if self._urgente:
            costo += costo * RECARGO_URGENTE
        return costo

    def mostrar_informacion(self):
        """Descripción de la asesoría."""
        urgencia = "urgente" if self._urgente else "normal"
        estado = "disponible" if self._disponible else "no disponible"
        return (f"Asesoría {self.nombre} | Especialista: {self._especialista} | "
                f"Nivel: {self._nivel} | Tarifa: ${self._tarifa_base:,.0f}/hora | "
                f"{urgencia} | {estado}")