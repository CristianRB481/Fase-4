"""Pruebas de manejo_errores.py (ejecutar con: python -m unittest)."""

import unittest

from software_fj.manejo_errores import (
    ErrorOperacion,
    ejecutar_lote,
    ejecutar_seguro,
    reintentar,
)


def dividir(a, b):
    return a / b


class PruebasEjecutarSeguro(unittest.TestCase):
    def test_operacion_correcta(self):
        self.assertEqual(ejecutar_seguro(dividir, 10, 2), (True, 5))

    def test_error_no_detiene_el_programa(self):
        exito, resultado = ejecutar_seguro(dividir, 1, 0, valor_por_defecto=-1)
        self.assertFalse(exito)
        self.assertEqual(resultado, -1)


class PruebasReintentar(unittest.TestCase):
    def test_agota_intentos_y_encadena_error(self):
        @reintentar(intentos=2, espera=0)
        def siempre_falla():
            raise ValueError("fallo")

        with self.assertRaises(ErrorOperacion) as contexto:
            siempre_falla()
        self.assertIsInstance(contexto.exception.__cause__, ValueError)


class PruebasLote(unittest.TestCase):
    def test_resumen(self):
        resumen = ejecutar_lote([
            ("división válida", dividir, (4, 2), {}),
            ("división por cero", dividir, (4, 0), {}),
        ])
        self.assertEqual(resumen["exitosas"], 1)
        self.assertEqual(resumen["fallidas"], 1)


if __name__ == "__main__":
    unittest.main()
