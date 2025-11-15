from django.db import transaction
from django.forms import ValidationError, inlineformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from .forms import FormArchivoAdjunto, FormFormularioSolicitud, FormSolicitud, FormTipoSolicitud
from .models import ArchivoAdjunto, CampoFormulario, FormularioSolicitud, RespuestaCampo, Solicitud, TipoSolicitud
from .funcionalidad import FuncionesAvanzadas

def bienvenida(request):
    return render(request, 'bienvenida.html')


def lista_solicitudes(request):
    funciones_avanzadas = FuncionesAvanzadas()
    resultado = funciones_avanzadas.calculo_extremo(2, 2)
    context = {
        'tipo_solicitudes': TipoSolicitud.objects.all(),
        'resultado': resultado
    }
    return render(request, 'lista_tipo_solicitudes.html', context)

def agregar(request):
    if request.method == 'POST':
        form = FormTipoSolicitud(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tipo_solicitudes')
    else:
        form = FormTipoSolicitud()
    context = {
        'form': form
    }
    return render(request, 'agregar_solicitud.html', context)

def lista_formularios(request):
    context = {
        'formularios': FormularioSolicitud.objects.all(),
        'resultado': FormularioSolicitud.objects.all().count
    }
    return render(request, 'lista_formulario.html', context)

def generar_folio_unico():
    import uuid
    return f"FOLIO-{uuid.uuid4().hex[:8].upper()}"

def crear_o_editar_formulario(request, pk=None):
    instancia = None
    if pk:
        instancia = get_object_or_404(FormularioSolicitud, pk=pk)

    if request.method == 'POST':
        form = FormFormularioSolicitud(request.POST, instance=instancia)
        
        if form.is_valid():
            form.save()
            return redirect('listar_formularios')
    else:
        form = FormFormularioSolicitud(instance=instancia)
        
    if instancia:
        titulo = "Editar Formulario de Solicitud"
    else:
        titulo = "Crear Nuevo Formulario de Solicitud"
        
    context = {
        'form': form,
        'titulo': titulo,
        'instancia': instancia,
    }
    return render(request, 'crear_formulario_solicitud.html', context)