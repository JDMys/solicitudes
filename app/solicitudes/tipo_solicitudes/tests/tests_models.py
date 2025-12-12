from django.test import TestCase
from django.core.exceptions import ValidationError
from tipo_solicitudes.models import TipoSolicitud


class TestSmokeTest(TestCase):

    def test_dos_mas_dos(self):
        self.assertEqual(2, 2)

    def test_tres_mas_tres(self):
        self.assertEqual(3, 3)

    def test_insertar_tipo_solicitud_constancia(self):
        tipo = TipoSolicitud.objects.create(
            nombre='Constancia',
            descripcion='Constancia para servicio social'
        )
        self.assertEqual(tipo.nombre, TipoSolicitud.objects.first().nombre)
        # self.assertEqual(1, TipoSolicitud.objects.count())

    def test_cantidad_maxima_caracteres_tipo_solicitud(self):
        tipo = TipoSolicitud(
            nombre='Constancia alsdjasdhasjdk asdkashdkajshdkasdhaksdjhaksdjh askdjahsdka sdakshdakjsd kashdjasdhajs dhasjdhasjkd haskdjhaskjdhaskdhaskjdhaskjdhha ks djasdjhajskd ha skdhasd',
            descripcion='Constancia para servicio social'
        )
        with self.assertRaises(ValidationError):
            tipo.full_clean()

    def test_nombre_requerdio(self):
        tipo = TipoSolicitud(
            nombre='',
            descripcion='Constancia para servicio social'
        )
        with self.assertRaises(ValidationError):
            tipo.full_clean()

    def test_mensaje_error_requerido(self):
        tipo = TipoSolicitud(
            nombre='',
            descripcion='Constancia para servicio social'
        )
        try:
            tipo.full_clean()
        except ValidationError as ex:
            msg = ex.message_dict['nombre'][0]
            self.assertEqual('Este campo no puede estar en blanco.', msg)

    def test_cantidad_maxima_caracteres_mensaje(self):
        tipo = TipoSolicitud(
            nombre='Constancia alsdjasdhasjdk asdkashdkajshdkasdhaksdjhaksdjh askdjahsdka sdakshdakjsd kashdjasdhajs dhasjdhasjkd haskdjhaskjdhaskdhaskjdhaskjdhha ks djasdjhajskd ha skdhasd',
            descripcion='Constancia para servicio social'
        )
        try:
            tipo.full_clean()
        except ValidationError as ex:
            msg = ex.message_dict['nombre'][0]
            self.assertEqual(
                'Asegúrese de que este valor tenga como máximo 150 caracteres (tiene 169).', msg)
