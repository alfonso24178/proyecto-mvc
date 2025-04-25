
import unittest
from app import create_app

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True

    def test_home_status_code(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_materias_listado(self):
        response = self.app.get("/materias")
        self.assertIn(response.status_code, [200, 302])  # 302 si redirige a login

    def test_materias_busqueda(self):
        response = self.app.get("/materias?search=matematicas")
        self.assertIn(response.status_code, [200, 302])

    def test_formulario_nueva_materia(self):
        response = self.app.get("/materias/nueva")
        self.assertIn(response.status_code, [200, 302])

if __name__ == "__main__":
    unittest.main()
