import unittest

from app.repositories.beneficio_repository import BENEFICIOS, obter_beneficio


class CatalogoTest(unittest.TestCase):
    def test_catalogo_tem_beneficios_validos(self):
        self.assertGreaterEqual(len(BENEFICIOS), 4)
        for beneficio_id, item in BENEFICIOS.items():
            self.assertEqual(item["id"], beneficio_id)
            self.assertGreater(item["preco_pontos"], 0)
            self.assertGreater(item["desconto"], 0)
            self.assertTrue(item["nome"])
            self.assertTrue(item["loja"])

    def test_busca_beneficio_normaliza_id(self):
        self.assertIsNotNone(obter_beneficio(" ECOBAG-SUSTENTAVEL "))
        self.assertIsNone(obter_beneficio("nao-existe"))


if __name__ == "__main__":
    unittest.main()
