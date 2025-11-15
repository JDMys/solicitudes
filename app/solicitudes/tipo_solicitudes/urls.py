from django.urls import path
from tipo_solicitudes import views

#'tipo-solicitud/'
urlpatterns = [
<<<<<<< HEAD
    path('nuevo/', views.agregar, name='agrega_solicitud'),
    path('lista/', views.lista_solicitudes, name='lista_tipo_solicitudes'),
    path('crear/<int:tipo_id>/', views.crear_solicitud, name='crear_solicitud'),
    path('mis-solicitudes/', views.mis_solicitudes, name='mis_solicitudes'),
    path('solicitud/<int:solicitud_id>/', views.detalle_solicitud, name='detalle_solicitud'),
=======
    path('', views.agregar, name='agrega_solicitud'),
    path('lista', views.lista_solicitudes, name='lista_tipo_solicitudes'),
    path('grafica_solicitudes/', views.vista_tres_graficas, name='grafica_solicitudes'),
    path('generar_pdf_graficas/', views.generar_pdf_graficas, name='generar_pdf_graficas'),
    path('generar_csv_graficas/', views.generar_csv_graficas, name='generar_csv_graficas'),
>>>>>>> 26e440e98a7ff1615b49cc77a11509ba8a1bd3f1
]
