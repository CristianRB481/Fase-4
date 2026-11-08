from software_fj.entidad import Entidad
from software_fj.validaciones import (
    validar_identificacion,
    validar_nombre,
    validar_correo
)


class Cliente(Entidad):
    """Representa un cliente de Software FJ."""

    def __init__(self, identificacion, nombre, correo, telefono, direccion):

        # Validar los datos antes de crear el cliente
        if not validar_identificacion(identificacion):
            raise ValueError("La identificación no es válida.")

        if not validar_nombre(nombre):
            raise ValueError("El nombre no es válido.")

        if not validar_correo(correo):
            raise ValueError("El correo electrónico no es válido.")

        if not telefono or not str(telefono).strip():
            raise ValueError("El teléfono es obligatorio.")

        if not direccion or not direccion.strip():
            raise ValueError("La dirección es obligatoria.")

        # Inicializar los atributos heredados de Entidad
        super().__init__(identificacion, nombre.strip(), correo.strip())

        # Atributos privados del cliente
        self.__telefono = str(telefono).strip()
        self.__direccion = direccion.strip()

# Las propiedades permiten consultar sus valores sin acceder directamente a ellos.
    @property
    def telefono(self):
        return self.__telefono

    @property
    def direccion(self):
        return self.__direccion

    def mostrar_informacion(self):
        """Muestra los datos del cliente."""

        print("\n===== INFORMACIÓN DEL CLIENTE =====")
        print(f"Identificación: {self.identificacion}")
        print(f"Nombre: {self.nombre}")
        print(f"Correo: {self.correo}")
        print(f"Teléfono: {self.telefono}")
        print(f"Dirección: {self.direccion}")

    def actualizar_telefono(self, nuevo_telefono):
        """Actualiza el teléfono del cliente."""

        if not nuevo_telefono or not str(nuevo_telefono).strip():
            raise ValueError("El teléfono no puede estar vacío.")

        self.__telefono = str(nuevo_telefono).strip()

    def actualizar_direccion(self, nueva_direccion):
        """Actualiza la dirección del cliente."""

        if not isinstance(nueva_direccion, str) or not nueva_direccion.strip():
            raise ValueError("La dirección no puede estar vacía.")

        self.__direccion = nueva_direccion.strip()
