"""Punto de entrada interactivo del sistema Software FJ."""

from software_fj.asesoria import AsesoriaEspecializada
from software_fj.cliente import Cliente
from software_fj.equipo import AlquilerEquipo
from software_fj.excepciones import SoftwareFJerror
from software_fj.sala import EXTRAS_DISPONIBLES, ReservaSala


def mostrar_banner():
    print("================================")
    print("======== Software FJ ===========")
    print("================================")


def leer_numero(mensaje, tipo=float):
    while True:
        try:
            return tipo(input(mensaje).strip().replace(",", "."))
        except ValueError:
            print("Error: ingrese un número válido.")


def leer_si_no(mensaje):
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta in ("si", "sí", "s", "true", "1"):
            return True
        if respuesta in ("no", "n", "false", "0"):
            return False
        print("Error: responda sí o no.")


def crear_sala(servicios):
    try:
        identificacion = input("Identificación de la sala: ").strip()
        nombre = input("Nombre de la sala: ").strip()
        tarifa = leer_numero("Tarifa por hora: ")
        capacidad = leer_numero("Capacidad: ", int)
        print("Extras disponibles:", ", ".join(EXTRAS_DISPONIBLES))
        extras_texto = input("Extras separados por coma (vacío para ninguno): ").strip()
        extras = [extra.strip() for extra in extras_texto.split(",") if extra.strip()]
        servicio = ReservaSala(
            identificacion, nombre, tarifa, capacidad, extras
        )
        servicios.append(servicio)
        print("\nSala creada:")
        print(servicio.mostrar_informacion())
    except (SoftwareFJerror, ValueError) as error:
        print(f"Error: {error}")


def crear_equipo(servicios):
    try:
        identificacion = input("Identificación del equipo: ").strip()
        nombre = input("Nombre del equipo: ").strip()
        tarifa = leer_numero("Tarifa por hora: ")
        tipo_equipo = input("Tipo de equipo: ").strip()
        unidades = leer_numero("Unidades disponibles: ", int)
        con_seguro = leer_si_no("¿Incluir seguro? (sí/no): ")
        servicio = AlquilerEquipo(
            identificacion, nombre, tarifa, tipo_equipo, unidades, con_seguro
        )
        servicios.append(servicio)
        print("\nEquipo creado:")
        print(servicio.mostrar_informacion())
    except (SoftwareFJerror, ValueError) as error:
        print(f"Error: {error}")


def crear_asesoria(servicios):
    try:
        identificacion = input("Identificación de la asesoría: ").strip()
        nombre = input("Tema de asesoría: ").strip()
        tarifa = leer_numero("Tarifa por hora: ")
        especialista = input("Nombre del especialista: ").strip()
        nivel = input("Nivel (basico/intermedio/avanzado): ").strip()
        urgente = leer_si_no("¿Es urgente? (sí/no): ")
        servicio = AsesoriaEspecializada(
            identificacion, nombre, tarifa, especialista, nivel, urgente
        )
        servicios.append(servicio)
        print("\nAsesoría creada:")
        print(servicio.mostrar_informacion())
    except (SoftwareFJerror, ValueError) as error:
        print(f"Error: {error}")


def crear_cliente(clientes):
    try:
        identificacion = input("Identificación (5 a 15 dígitos): ").strip()
        if any(cliente.identificacion == identificacion for cliente in clientes):
            print("Error: ya existe un cliente con esa identificación.")
            return
        nombre = input("Nombre completo: ").strip()
        correo = input("Correo electrónico: ").strip()
        telefono = input("Teléfono: ").strip()
        direccion = input("Dirección: ").strip()
        cliente = Cliente(identificacion, nombre, correo, telefono, direccion)
        clientes.append(cliente)
        print("\nCliente registrado:")
        cliente.mostrar_informacion()
    except ValueError as error:
        print(f"Error: {error}")


def listar_clientes(clientes):
    if not clientes:
        print("\nNo hay clientes registrados.")
        return
    print(f"\nClientes registrados: {len(clientes)}")
    for cliente in clientes:
        cliente.mostrar_informacion()


def listar_servicios(servicios):
    if not servicios:
        print("\nNo hay servicios registrados.")
        return
    print("\nServicios registrados:")
    for indice, servicio in enumerate(servicios, start=1):
        print(f"{indice}. {servicio.mostrar_informacion()}")


def calcular_costo(servicios):
    listar_servicios(servicios)
    if not servicios:
        return
    try:
        indice = leer_numero("Seleccione el número del servicio: ", int)
        if indice < 1 or indice > len(servicios):
            print("Error: selección fuera de rango.")
            return
        duracion = leer_numero("Duración en horas: ")
        descuento = leer_numero("Descuento (0 a 100 %): ") / 100
        servicio = servicios[indice - 1]
        total = servicio.calcular_costo_total(duracion, descuento=descuento)
        print(f"\nCosto total con IVA: ${total:,.2f}")
    except (SoftwareFJerror, ValueError) as error:
        print(f"Error: {error}")


def mostrar_menu():
    print("\n1. Registrar cliente")
    print("2. Ver clientes")
    print("3. Crear reserva de sala")
    print("4. Crear alquiler de equipo")
    print("5. Crear asesoría")
    print("6. Ver servicios")
    print("7. Calcular costo")
    print("0. Salir")


def main():
    mostrar_banner()
    servicios = []
    clientes = []
    opciones = {
        "1": crear_cliente,
        "3": crear_sala,
        "4": crear_equipo,
        "5": crear_asesoria,
    }

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "0":
            print("Hasta pronto.")
            break
        if opcion in opciones:
            opciones[opcion](clientes if opcion == "1" else servicios)
        elif opcion == "2":
            listar_clientes(clientes)
        elif opcion == "6":
            listar_servicios(servicios)
        elif opcion == "7":
            calcular_costo(servicios)
        else:
            print("Error: opción no válida.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma terminado.")
