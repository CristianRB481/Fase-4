
#Clase de reservas
#Se encarga de gestionar las reservas de servicios realizadas por los clientes.
#cancelar, confoimar servicios y mostrarlos.



# reserva.py
from software_fj.cliente import Cliente
from software_fj.servicio import Servicio
from software_fj.equipo import AlquilerEquipo
from software_fj.excepciones import (
    ClienteInvalidoError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    DuracionInvalidaError,
    OperacionNoPermitidaError,
    EntidadNoEncontradaError,
)

#creacion de la clase reserva
class Reserva:
    """Representa una reserva simple de un servicio para un cliente."""

    ESTADOS_VALIDOS = ("Pendiente", "Confirmada", "Cancelada")

    def __init__(self, cliente: Cliente, servicio: Servicio, duracion: float):
        if not isinstance(cliente, Cliente):
            raise ClienteInvalidoError("La reserva debe asociarse a un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ServicioInvalidoError("La reserva debe asociarse a un servicio válido.")
        if (not isinstance(duracion, (int, float))
                or isinstance(duracion, bool)
                or duracion <= 0):
            raise DuracionInvalidaError("La duración debe ser mayor que cero.")

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "Pendiente"
        self._motivo_cancelacion = None

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def duracion(self) -> float:
        return self._duracion

    @property
    def estado(self) -> str:
        return self._estado

    def confirmar(self):
        if self._estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )
        self._estado = "Confirmada"

    def cancelar(self, motivo=None):
        if self._estado == "Cancelada":
            raise OperacionNoPermitidaError("La reserva ya está cancelada.")
        self._estado = "Cancelada"
        self._motivo_cancelacion = motivo


class ReservaServicios:
    """Gestiona el carrito de compras y ciclo de vida de una reserva de servicios."""

    ESTADOS_VALIDOS = ("Pendiente", "Confirmada", "Cancelada")
#funcion para inicializar la clase reserva
    def __init__(self, cliente: Cliente):
        if not isinstance(cliente, Cliente):
            raise ClienteInvalidoError("La reserva debe asociarse a un objeto Cliente válido.")

        self._cliente = cliente
        self._items: list[dict] = []
        self._estado = "Pendiente"

   
    # Propiedades
    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def items(self) -> list[dict]:
        """Devuelve una copia superficial para proteger la lista interna."""
        return list(self._items)

    
    # Gestión para Adquirir y Quitar servicios.
    #funcion para adquirir un servicio
    def adquirir_servicio(self, servicio: Servicio, duracion: float, descuento: float = 0.0):
        """Valida y agrega un servicio con su duración al carrito de reserva."""
        if self._estado != "Pendiente":
            raise OperacionNoPermitidaError(
                f"No se pueden agregar servicios a una reserva en estado '{self._estado}'."
            )

        if not isinstance(servicio, Servicio):
            raise ServicioInvalidoError("El elemento debe ser una instancia de Servicio.")

        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre}' no está disponible actualmente."
            )

        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise DuracionInvalidaError("La duración de la reserva debe ser mayor a cero.")

        # Control de inventario específico para AlquilerEquipo
        if isinstance(servicio, AlquilerEquipo):
            servicio.reservar_unidad()
        # Agregar el servicio a una lista de items.
        self._items.append({
            "servicio": servicio,
            "duracion": duracion,
            "descuento": descuento,
        })
    #funcion para remover un servicio
    def remover_servicio(self, identificacion_servicio):
        """Elimina un servicio del carrito mientras la reserva esté pendiente."""
        if self._estado != "Pendiente":
            raise OperacionNoPermitidaError(
                f"No se pueden quitar servicios de una reserva '{self._estado}'."
            )
        #ciclo para recorrer los items y eliminar el servicio que coincida con la identificacion
        for i, item in enumerate(self._items):
            if item["servicio"].identificacion == identificacion_servicio:
                servicio_removido = self._items.pop(i)["servicio"]
                if isinstance(servicio_removido, AlquilerEquipo):
                    servicio_removido.liberar_unidad()
                return
        # Si no se encuentra el servicio, se lanza una excepción
        raise EntidadNoEncontradaError(
            f"No se encontró el servicio con ID '{identificacion_servicio}' en el carrito."
        )
   
    # Ciclo de Vida de la Reserva (Confirmar, Procesar, Cancelar)
    #funcion para confirmar la reserva
    def confirmar_reserva(self):
        """Valida que el carrito no esté vacío y confirma la reserva."""
        if self._estado != "Pendiente":
            raise OperacionNoPermitidaError(
                f"Solo se pueden confirmar reservas pendientes (estado actual: '{self._estado}')."
            )
        if not self._items:
            raise OperacionNoPermitidaError("No se puede confirmar una reserva sin servicios.")

        self._estado = "Confirmada"
    #funcion para cancelar la reserva
    def cancelar_reserva(self):
        """Cancela la reserva y libera los recursos reservados."""
        if self._estado == "Cancelada":
            raise OperacionNoPermitidaError("La reserva ya se encuentra cancelada.")
        #ciclo para liberar los recursos reservados en caso de que el servicio sea de tipo AlquilerEquipo
        for item in self._items:
            servicio = item["servicio"]
            if isinstance(servicio, AlquilerEquipo):
                servicio.liberar_unidad()

        self._estado = "Cancelada"
        #funcion para procesar la reserva
    def procesar_reserva(self) -> dict:
        """Calcula los totales aplicando polimorfismo y devuelve un desglose estructurado."""
        if self._estado == "Cancelada":
            raise OperacionNoPermitidaError("No se puede procesar una reserva cancelada.")
        if not self._items:
            raise OperacionNoPermitidaError("El carrito está vacío.")
        #ciclo para recorrer los items y calcular el subtotal de cada servicio.
        total_general = 0.0
        detalle_servicios = []

        for item in self._items:
            servicio = item["servicio"]
            duracion = item["duracion"]
            descuento = item["descuento"]

            # cada subclase ejecuta su propio cálculo
            subtotal = servicio.calcular_costo_total(duracion, descuento=descuento)
            total_general += subtotal

            detalle_servicios.append({
                "id": servicio.identificacion,
                "nombre": servicio.nombre,
                "duracion_horas": duracion,
                "descuento_aplicado": f"{descuento * 100:.0f}%",
                "subtotal_con_iva": subtotal,
            })

        return {
            "cliente": self._cliente.nombre,
            "identificacion_cliente": self._cliente.identificacion,
            "estado_reserva": self._estado,
            "cantidad_servicios": len(self._items),
            "detalle": detalle_servicios,
            "total_a_pagar": round(total_general, 2),
        }
   
    # Presentación / Resumen
    
    def mostrar_resumen(self) -> str:
        """Genera un ticket o resumen legible de la reserva."""
        datos = self.procesar_reserva()

        lineas = [
            "==================================================",
            f"RESUMEN DE RESERVA - ESTADO: {datos['estado_reserva'].upper()}",
            "==================================================",
            f"Cliente: {datos['cliente']} (ID: {datos['identificacion_cliente']})",
            f"Correo:  {self._cliente.correo}",
            "--------------------------------------------------",
            "SERVICIOS ADQUIRIDOS:",
        ]
        #ciclo para recorrer los items y mostrar la informacion de cada servicio adquirido
        for item, det in zip(self._items, datos["detalle"]):
            servicio = item["servicio"]
            lineas.append(f"  * {servicio.mostrar_informacion()}")
            lineas.append(
                f"    Duración: {det['duracion_horas']}h | "
                f"Desc: {det['descuento_aplicado']} | "
                f"Subtotal (IVA inc.): ${det['subtotal_con_iva']:,.2f}"
            )
        #ciclo para mostrar el total a pagar
        lineas.extend([
            "--------------------------------------------------",
            f"TOTAL A PAGAR: ${datos['total_a_pagar']:,.2f}",
            "==================================================",
        ])

        return "\n".join(lineas)
