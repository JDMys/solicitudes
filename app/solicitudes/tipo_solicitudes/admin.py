from django.contrib import admin
from .models import (
    TipoSolicitud,
    Solicitud
)

admin.site.register(TipoSolicitud)
admin.site.register(Solicitud)
