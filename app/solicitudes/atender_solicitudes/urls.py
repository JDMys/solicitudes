from django.urls import path
from .views import marcar_solicitud_en_proceso, cerrar_solicitud

urlpatterns = [
    path('marcar-en-proceso/<int:solicitud_id>/', marcar_solicitud_en_proceso, name='marcar_solicitud_en_proceso'),
    path('cerrar/<int:solicitud_id>/', cerrar_solicitud, name='cerrar_solicitud'),
]
