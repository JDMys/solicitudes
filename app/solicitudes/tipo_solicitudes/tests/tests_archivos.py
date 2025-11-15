from django.test import TestCase
from django.urls import reverse


class TestDescargas(TestCase):

    # -------------------------------------------------
    # TEST 1: Descarga de PDF funciona
    # -------------------------------------------------
    def test_descarga_pdf(self):
        url = reverse("generar_pdf_graficas")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertIn("attachment", response["Content-Disposition"])

    # -------------------------------------------------
    # TEST 2: Descarga de CSV funciona
    # -------------------------------------------------
    def test_descarga_csv(self):
        url = reverse("generar_csv_graficas")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn("attachment", response["Content-Disposition"])
