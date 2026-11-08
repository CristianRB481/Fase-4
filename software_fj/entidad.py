from abc import ABC, abstractmethod


class Entidad(ABC):
    """Clase base abstracta para las entidades del sistema."""

    def __init__(self, identificacion, nombre, correo):
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo

    @abstractmethod
    def mostrar_informacion(self):
        """Método que deben implementar las clases hijas."""
        pass
