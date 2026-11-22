"""
Módulo gestor de Software FJ.

GestorSoftwareFJ coordina clientes, servicios y reservas usando solo
listas internas (sin base de datos). Aquí se demuestran los bloques
try/except/else/finally y el encadenamiento de excepciones.
"""

from software_fj.cliente import Cliente
from software_fj.servicio import Servicio
from software_fj.reserva import Reserva
from software_fj.logger import registrar_evento, registrar_error
from software_fj.excepciones import (
    SoftwareFJError,
    ClienteInvalidoError,
    ClienteDuplicadoError,
    DuracionInvalidaError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
)


class GestorSoftwareFJ:
    """Administra clientes, servicios y reservas en memoria."""

    def __init__(self):
        # Listas internas: reemplazan a la base de datos.
        self._clientes = []
        self._servicios = []
        self._reservas = []
        # Números de reserva (posición + 1) según su estado.
        self._confirmadas = set()
        self._canceladas = set()

    # ---------------------------------------------------------
    # Búsquedas
    # ---------------------------------------------------------
    def buscar_cliente(self, identificacion):
        """Devuelve el cliente o lanza EntidadNoEncontradaError."""
        for cliente in self._clientes:
            if str(cliente.identificacion) == str(identificacion):
                return cliente
        raise EntidadNoEncontradaError(f"No existe el cliente '{identificacion}'.")

    def buscar_servicio(self, identificacion):
        """Devuelve el servicio o lanza EntidadNoEncontradaError."""
        for servicio in self._servicios:
            if str(servicio.identificacion) == str(identificacion):
                return servicio
        raise EntidadNoEncontradaError(f"No existe el servicio '{identificacion}'.")

    def buscar_reserva(self, numero):
        """Devuelve la reserva con ese número (1, 2, 3...)."""
        if not isinstance(numero, int) or not 1 <= numero <= len(self._reservas):
            raise EntidadNoEncontradaError(f"No existe la reserva '{numero}'.")
        return self._reservas[numero - 1]

    # ---------------------------------------------------------
    # Clientes: try / except / else
    # ---------------------------------------------------------
    def registrar_cliente(self, identificacion, nombre, correo, telefono, direccion):
        """Crea y guarda un cliente validando sus datos."""
        try:
            cliente = Cliente(identificacion, nombre, correo, telefono, direccion)
        except (ValueError, TypeError, AttributeError) as error:
            # ENCADENAMIENTO: el error original queda en __cause__.
            registrar_error(f"Cliente inválido ({identificacion}): {error}")
            raise ClienteInvalidoError(str(error)) from error
        else:
            # El else solo corre si NO hubo excepción al crear el cliente.
            try:
                self.buscar_cliente(identificacion)
            except EntidadNoEncontradaError:
                self._clientes.append(cliente)
                registrar_evento(f"Cliente registrado: {identificacion}")
                return cliente
            registrar_error(f"Cliente duplicado: {identificacion}")
            raise ClienteDuplicadoError(f"El cliente '{identificacion}' ya existe.")

    # ---------------------------------------------------------
    # Servicios
    # ---------------------------------------------------------
    def agregar_servicio(self, servicio):
        """Guarda un servicio ya creado (sala, equipo o asesoría)."""
        if not isinstance(servicio, Servicio):
            registrar_error("Se intentó agregar un objeto que no es Servicio.")
            raise ServicioInvalidoError("El objeto no es un servicio válido.")
        try:
            self.buscar_servicio(servicio.identificacion)
        except EntidadNoEncontradaError:
            self._servicios.append(servicio)
            registrar_evento(f"Servicio agregado: {servicio.identificacion}")
            return servicio
        registrar_error(f"Servicio duplicado: {servicio.identificacion}")
        raise ServicioInvalidoError(f"El servicio '{servicio.identificacion}' ya existe.")

    # ---------------------------------------------------------
    # Reservas: try / except / else / finally
    # ---------------------------------------------------------
    def crear_reserva(self, id_cliente, id_servicio, duracion):
        """Crea una reserva PENDIENTE y devuelve su número."""
        try:
            if (not isinstance(duracion, (int, float)) or isinstance(duracion, bool)
                    or duracion <= 0):
                raise DuracionInvalidaError("La duración debe ser un número mayor que cero.")
            cliente = self.buscar_cliente(id_cliente)
            servicio = self.buscar_servicio(id_servicio)
            if not servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{servicio.nombre}' no está disponible."
                )
            try:
                reserva = Reserva(cliente, servicio, duracion)
            except (TypeError, ValueError) as error:
                raise OperacionNoPermitidaError(
                    "No se pudo construir la reserva."
                ) from error
        except SoftwareFJError as error:
            registrar_error(f"Reserva fallida: {error}")
            raise
        else:
            self._reservas.append(reserva)
            numero = len(self._reservas)
            registrar_evento(f"Reserva #{numero} creada ({id_cliente} / {id_servicio}).")
            return numero
        finally:
            # El finally corre SIEMPRE, haya o no error.
            registrar_evento(f"Intento de reserva finalizado ({id_cliente} / {id_servicio}).")

    def confirmar_reserva(self, numero):
        """Confirma una reserva pendiente."""
        try:
            reserva = self.buscar_reserva(numero)
            if numero in self._canceladas:
                raise OperacionNoPermitidaError("No se puede confirmar una reserva cancelada.")
            if numero in self._confirmadas:
                raise OperacionNoPermitidaError("La reserva ya está confirmada.")
            servicio = reserva.servicio
            # Los equipos descuentan una unidad al confirmar.
            if hasattr(servicio, "reservar_unidad"):
                servicio.reservar_unidad()
            try:
                reserva.confirmar()
            except Exception:
                if hasattr(servicio, "liberar_unidad"):
                    servicio.liberar_unidad()
                raise
        except SoftwareFJError as error:
            registrar_error(f"Confirmación fallida (#{numero}): {error}")
            raise
        else:
            self._confirmadas.add(numero)
            registrar_evento(f"Reserva #{numero} confirmada.")

    def cancelar_reserva(self, numero, motivo=None):
        """Cancela una reserva (motivo opcional)."""
        try:
            reserva = self.buscar_reserva(numero)
            if numero in self._canceladas:
                raise OperacionNoPermitidaError("La reserva ya estaba cancelada.")
            reserva.cancelar(motivo)
        except SoftwareFJError as error:
            registrar_error(f"Cancelación fallida (#{numero}): {error}")
            raise
        else:
            # Si estaba confirmada, el equipo recupera su unidad.
            if numero in self._confirmadas and hasattr(reserva.servicio, "liberar_unidad"):
                reserva.servicio.liberar_unidad()
            self._confirmadas.discard(numero)
            self._canceladas.add(numero)
            registrar_evento(f"Reserva #{numero} cancelada. Motivo: {motivo or 'sin motivo'}.")

    def calcular_total(self, numero, descuento=0.0):
        """Total de la reserva con IVA y descuento opcional (polimorfismo)."""
        try:
            reserva = self.buscar_reserva(numero)
            return reserva.servicio.calcular_costo_total(
                reserva.duracion, descuento=descuento
            )
        except SoftwareFJError as error:
            registrar_error(f"Cálculo fallido (#{numero}): {error}")
            raise

    # ---------------------------------------------------------
    # Listados
    # ---------------------------------------------------------
    def listar_clientes(self):
        return list(self._clientes)

    def listar_servicios(self):
        return list(self._servicios)

    def listar_reservas(self):
        return list(self._reservas)