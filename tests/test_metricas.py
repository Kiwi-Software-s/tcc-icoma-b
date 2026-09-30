import unittest
from datetime import datetime, timezone

from app.repositories.resgate_repository import (
    _normalizar_codigo,
    _periodos_diarios,
    _periodos_mensais,
    _periodos_semanais,
)


class MetricasTest(unittest.TestCase):
    def setUp(self):
        self.agora = datetime(2026, 9, 30, 15, 0, tzinfo=timezone.utc)

    def test_normaliza_codigo(self):
        self.assertEqual(_normalizar_codigo(" eco-plastico-001 "), "ECO-PLASTICO-001")

    def test_periodos_tem_tamanhos_esperados(self):
        self.assertEqual(len(_periodos_mensais(self.agora)), 6)
        self.assertEqual(len(_periodos_semanais(self.agora)), 8)
        self.assertEqual(len(_periodos_diarios(self.agora)), 7)

    def test_periodos_estao_ordenados(self):
        for periodos in (
            _periodos_mensais(self.agora),
            _periodos_semanais(self.agora),
            _periodos_diarios(self.agora),
        ):
            inicios = [p["inicio"] for p in periodos]
            self.assertEqual(inicios, sorted(inicios))


if __name__ == "__main__":
    unittest.main()
