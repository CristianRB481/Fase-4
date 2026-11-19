"""Pruebas de AsesoriaEspecializada."""

from software_fj.asesoria import AsesoriaEspecializada
from software_fj.excepciones import ParametroFaltanteError, ServicioInvalidoError


def prueba_asesoria_valida():
    a = AsesoriaEspecializada("ASE-1", "Python", 40000, "Ana Pérez")
    assert a.nivel == "basico" and a.disponible and not a.urgente
    print("OK  asesoría válida")


def prueba_costo_basico():
    a = AsesoriaEspecializada("ASE-1", "Python", 40000, "Ana Pérez")
    assert a.calcular_costo(2) == 80000
    assert a.calcular_costo_total(2) == 95200.0     # con IVA 19 %
    print("OK  costo nivel básico")


def prueba_costo_avanzado():
    a = AsesoriaEspecializada("ASE-2", "Bases de datos", 40000, "Luis Gómez",
                              nivel="avanzado")
    assert a.calcular_costo(2) == 160000            # 40000 * 2 * 2.0
    print("OK  costo nivel avanzado")


def prueba_costo_urgente():
    a = AsesoriaEspecializada("ASE-3", "Redes", 40000, "Marta Ruiz",
                              urgente=True)
    assert a.calcular_costo(2) == 100000.0          # 80000 + 25 %
    assert a.calcular_costo_total(2) == 119000.0
    print("OK  costo urgente")


def prueba_con_descuento():
    a = AsesoriaEspecializada("ASE-1", "Python", 40000, "Ana Pérez")
    assert a.calcular_costo_total(2, descuento=0.5) == 47600.0
    print("OK  costo con descuento")


def prueba_sin_especialista():
    try:
        AsesoriaEspecializada("ASE-4", "Mala", 40000, "")
        print("FALLO")
    except ParametroFaltanteError:
        print("OK  especialista faltante rechazado")


def prueba_nivel_invalido():
    try:
        AsesoriaEspecializada("ASE-5", "Mala", 40000, "Ana Pérez", nivel="experto")
        print("FALLO")
    except ServicioInvalidoError:
        print("OK  nivel inválido rechazado")


def prueba_tarifa_invalida():
    try:
        AsesoriaEspecializada("ASE-6", "Mala", -10, "Ana Pérez")
        print("FALLO")
    except ServicioInvalidoError:
        print("OK  tarifa negativa rechazada")


def prueba_informacion():
    a = AsesoriaEspecializada("ASE-7", "Python", 40000, "Ana Pérez",
                              nivel="Intermedio", urgente=True)
    texto = a.mostrar_informacion()
    assert "Ana Pérez" in texto and "intermedio" in texto and "urgente" in texto
    print("OK  información")


if __name__ == "__main__":
    prueba_asesoria_valida()
    prueba_costo_basico()
    prueba_costo_avanzado()
    prueba_costo_urgente()
    prueba_con_descuento()
    prueba_sin_especialista()
    prueba_nivel_invalido()
    prueba_tarifa_invalida()
    prueba_informacion()
    print("\nTodas las pruebas pasaron.")