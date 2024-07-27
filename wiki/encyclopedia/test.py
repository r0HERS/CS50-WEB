from django.test import TestCase
from encyclopedia.models import ModeloTest

class EntryModelTest(TestCase):

    def setUp(self):
        self.aluno1 = ModeloTest.objects.get(id=1)
        self.aluno2 = ModeloTest.objects.get(id=2)
        self.aluno3 = ModeloTest.objects.get(id=3)
        

    def test_consulta_banco_dados(self):
        queryset = ModeloTest.objects.all()
        self.assertEqual(len(queryset), 3)
        self.assertIn(self.aluno1, queryset)
        self.assertIn(self.aluno2, queryset)
        self.assertIn(self.aluno3, queryset)