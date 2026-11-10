"""
 módulo de excepciones personalizadas de software_fj

 todas las excepciones del sistema heredan de softwareFJerror, de modo que se pueda capturar de forma general(except SoftwareFJerror)
 o de forma especifica (except ClienteDuplicadoError)"""





class SoftwareFJerror(Exception):
    """Excepción base de software_fj"""
    def __init__(self, mensaje="error en el sistema Software_fj"):
         super().__init__(mensaje)
         self.mensaje = mensaje


#------------
#error de datos 
#------------

class DatoInvalidoError(SoftwareFJerror):
     """un dato que no cumple el formato esperado"""

class ClienteInvalidoError(DatoInvalidoError):
    """Los datos de un cliente son inválidos (nombre, correo, etc.)."""

class DuracionInvalidaError(DatoInvalidoError):
    """La duración de una reserva es cero, negativa o no numérica."""

class ParametroFaltanteError(SoftwareFJerror):
    """Falta un parámetro obligatorio (llegó como None o vacío)."""

class CalculoInconsistenteError(SoftwareFJerror):
    """Un cálculo da un resultado sin sentido (total negativo, descuento > 100 %)."""


# ---------------------------------------------------------------
# Errores de clientes y servicios
# ---------------------------------------------------------------
class ClienteDuplicadoError(SoftwareFJerror):
    """Se intentó registrar un cliente que ya existe."""

class EntidadNoEncontradaError(SoftwareFJerror ):
    """No existe el cliente, servicio o reserva buscado."""


class ServicioInvalidoError(SoftwareFJerror):
    """Los parámetros de un servicio son incorrectos (capacidad negativa, etc.)."""


class ServicioNoDisponibleError(SoftwareFJerror):
    """El servicio solicitado no está disponible."""

# ---------------------------------------------------------------
# Errores de operaciones
# ---------------------------------------------------------------
class OperacionNoPermitidaError(SoftwareFJerror):
    """La operación no se puede hacer en el estado actual (ej. cancelar dos veces)."""