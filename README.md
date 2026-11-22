# Software FJ

Sistema integral de gestión de **clientes, servicios y reservas** para la empresa ficticia Software FJ, desarrollado en Python con programación orientada a objetos y manejo avanzado de excepciones.

Proyecto académico de la **UNAD – Ingeniería de Sistemas**, curso Programación 213023, Fase 4.

## Integrantes

| Integrante | Módulos principales |
|---|---|
| (cristian reyes barandica) | 
| (juan jose cuero betancourt) | 
| (andres felipe quijano santa) | 
| (santiago cortes chaspengal) | 
| 

## Servicios que ofrece la empresa

- **Reserva de salas** (`ReservaSala`): capacidad y extras opcionales (proyector, videoconferencia, pizarra).
- **Alquiler de equipos** (`AlquilerEquipo`): control de unidades y seguro opcional (+10 %).
- **Asesorías especializadas** (`AsesoriaEspecializada`): nivel (básico, intermedio, avanzado) y recargo por urgencia (+25 %).

## Estructura del proyecto

```
Fase-4/
├── main.py                    # Menú interactivo
├── ejecutar_simulacion.py     # Simulación de 13 operaciones
├── README.md
├── logs/
│   └── software_fj.log        # Registro de eventos y errores
├── pruebas/                   # Una prueba por módulo
└── software_fj/
    ├── excepciones.py         # Jerarquía de excepciones personalizadas
    ├── logger.py              # Registro en archivo de logs
    ├── validaciones.py        # Funciones de validación de datos
    ├── entidad.py             # Clase abstracta Entidad
    ├── cliente.py             # Cliente (atributos privados, validaciones)
    ├── servicio.py            # Clase abstracta Servicio
    ├── sala.py                # ReservaSala
    ├── equipo.py              # AlquilerEquipo
    ├── asesoria.py            # AsesoriaEspecializada
    ├── reserva.py             # Reserva y estados
    ├── gestor.py              # GestorSoftwareFJ (listas internas)
    └── simulacion.py          # Operaciones de prueba
```

## Diseño orientado a objetos

```
Entidad (abstracta)
├── Cliente
└── Servicio (abstracta)
    ├── ReservaSala
    ├── AlquilerEquipo
    └── AsesoriaEspecializada

Reserva ──► Cliente, Servicio
GestorSoftwareFJ ──► listas de clientes, servicios y reservas
```

| Concepto | Dónde se aplica |
|---|---|
| Abstracción | `Entidad` y `Servicio` (métodos con `@abstractmethod`) |
| Herencia | Los tres servicios heredan de `Servicio`, y este de `Entidad` |
| Polimorfismo | `calcular_costo_total` llama a `calcular_costo`, que cada servicio define distinto |
| Encapsulamiento | Atributos privados o protegidos con `@property` |
| Métodos sobrescritos | `calcular_costo`, `mostrar_informacion`, `validar_parametros` |
| "Sobrecarga" | `calcular_costo_total(duracion, descuento=0.0, impuesto=TASA_IVA)` con parámetros opcionales |

## Manejo de excepciones

Todas heredan de `SoftwareFJError`:





## Reglas de negocio acordadas

- **IVA:** 19 %, definido en la constante `TASA_IVA` de `servicio.py`.
- **Descuento:** opcional, como fracción entre 0 y 1 (0.1 = 10 %).
- **Estados de una reserva:** Pendiente, Confirmada y Cancelada.
- **Disponibilidad:** indicador simple; los equipos se controlan por unidades.
- **Sin base de datos:** la información vive en objetos y listas; los archivos se usan solo para el log.

## Cómo ejecutar


# Simulación de 13 operaciones (éxitos y fallos)
py ejecutar_simulacion.py

# Menú interactivo
py main.py

# Revisar el registro de eventos y errores
Get-Content logs/software_fj.log
```

## Pruebas

Se ejecutan desde la raíz del proyecto:

```powershell
py -m pruebas.prueba_excepciones
py -m pruebas.prueba_logger
py -m pruebas.prueba_servicio
py -m pruebas.prueba_sala
py -m pruebas.prueba_equipo
py -m pruebas.prueba_asesoria
```



