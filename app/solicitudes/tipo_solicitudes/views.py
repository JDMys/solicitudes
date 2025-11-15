<<<<<<< HEAD
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import FormTipoSolicitud
from .models import (
    TipoSolicitud, FormularioSolicitud, CampoFormulario,
    Solicitud, RespuestaCampo, ArchivoAdjunto, SeguimientoSolicitud
)
import uuid

=======
from datetime import datetime
import os
import csv
import io
from django.http import HttpResponse
from django.db.models import Count
from django.shortcuts import render, redirect
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI
import matplotlib.pyplot as plt
from .forms import FormTipoSolicitud
from .models import Solicitud, TipoSolicitud
from .funcionalidad import FuncionesAvanzadas
>>>>>>> 26e440e98a7ff1615b49cc77a11509ba8a1bd3f1

def bienvenida(request):
    return render(request, 'bienvenida.html')

def lista_solicitudes(request):
    context = {
        'tipo_solicitudes': TipoSolicitud.objects.all()
    }
    return render(request, 'solicitudes/lista_tipo_solicitudes.html', context)


def agregar(request):
    if request.method == 'POST':
        form = FormTipoSolicitud(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tipo_solicitudes')
    else:
        form = FormTipoSolicitud()
<<<<<<< HEAD

    return render(request, 'agregar_solicitud.html', {'form': form})


@login_required
def crear_solicitud(request, tipo_id):
    tipo = get_object_or_404(TipoSolicitud, id=tipo_id)
    formulario = tipo.formulario
    campos = formulario.campos.all()

    if request.method == 'POST':
        folio = str(uuid.uuid4())[:8]

        solicitud = Solicitud.objects.create(
            usuario=request.user,
            tipo_solicitud=tipo,
            folio=folio
        )

        for campo in campos:
            valor = request.POST.get(campo.nombre, '')

            respuesta = RespuestaCampo.objects.create(
                solicitud=solicitud,
                campo=campo,
                valor=valor
            )

            if campo.tipo == 'file':
                archivos = request.FILES.getlist(campo.nombre)
                for archivo in archivos:
                    ArchivoAdjunto.objects.create(
                        solicitud=solicitud,
                        respuesta=respuesta,
                        archivo=archivo,
                        nombre=archivo.name
                    )

        return redirect('mis_solicitudes')

    return render(request, 'solicitudes/crear_solicitud.html', {
        'tipo': tipo,
        'formulario': formulario,
        'campos': campos
    })


@login_required
def mis_solicitudes(request):
    solicitudes = Solicitud.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'solicitudes/mis_solicitudes.html', {'solicitudes': solicitudes})


@login_required
def detalle_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id, usuario=request.user)

    respuestas = solicitud.respuestas.all()
    seguimientos = SeguimientoSolicitud.objects.filter(solicitud=solicitud).order_by('-fecha_creacion')

    return render(request, 'solicitudes/detalle_solicitud.html', {
        'solicitud': solicitud,
        'respuestas': respuestas,
        'seguimientos': seguimientos
    })
=======
    context = {
        'form': form
    }
    return render(request, 'agregar_solicitud.html', context)

#obtiene les pinchis solicitudes y las mete en un contexto cfff
def obtener_solicitudes(request):
    solicitudes = Solicitud.objects.all() # 0 dias w
    tipos_solicitudes = TipoSolicitud.objects.all() #aqui si salen
    contexto_solicitudes = {
        'solicitudes': solicitudes
    }
    #print(f"Solicitudes obtenidas: {solicitudes}, total de {solicitudes.count()}")
    #print(f"Tipos de solicitudes obtenidas: {tipos_solicitudes}, total de {tipos_solicitudes.count()}")
    return contexto_solicitudes


def filtrar_solicitudes_fecha(solicitudes, dia, mes, semana):
    
    if dia!= 0:
        solicitudes = solicitudes.filter(fecha_creacion__day=dia)

    elif mes!=0:
        solicitudes = solicitudes.filter(fecha_creacion__month=mes)

    elif semana!=0:
        year = datetime.now().year
        inicio = datetime.fromisocalendar(year, semana, 1)
        fin = datetime.fromisocalendar(year, semana, 7)
        solicitudes = solicitudes.filter(fecha_creacion__range=[inicio, fin])   

    return solicitudes

def solicitudes_por_tipo(solicitudes_filtradas):
    solicitudes = (
        solicitudes_filtradas
        .values('tipo_solicitud__nombre')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    data = [
        {
            "tipo": s["tipo_solicitud__nombre"],
            "total": s["total"]
        }
        for s in solicitudes
    ]

    return data

def vista_tres_graficas(request):
    """

    """
    hoy = datetime.now().date()
    año, semana, _ = hoy.isocalendar()

    # Todas las solicitudes
    solicitudes = Solicitud.objects.all()

    # --- HOY ---
    solicitudes_hoy = solicitudes.filter(
        fecha_creacion__date=hoy
    )
    data_hoy = solicitudes_por_tipo(solicitudes_hoy)

    # --- SEMANA ---
    inicio_semana = datetime.fromisocalendar(hoy.year, semana, 1)
    fin_semana = datetime.fromisocalendar(hoy.year, semana, 7)
    solicitudes_semana = solicitudes.filter(
        fecha_creacion__range=[inicio_semana, fin_semana]
    )
    data_semana = solicitudes_por_tipo(solicitudes_semana)

    # --- MES ---
    solicitudes_mes = solicitudes.filter(
        fecha_creacion__year=hoy.year,
        fecha_creacion__month=hoy.month
    )
    data_mes = solicitudes_por_tipo(solicitudes_mes)

    context = {
        "hoy": data_hoy,
        "semana": data_semana,
        "mes": data_mes,
    }

    return render(request, "grafica.html", context)

def generar_pdf_graficas(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="graficas_solicitudes.pdf"'
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1458b1'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    title = Paragraph("Tendencias de Solicitudes", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))

    hoy = datetime.now().date()
    año, semana, _ = hoy.isocalendar()
    solicitudes = Solicitud.objects.all()
    
    # --- HOY ---
    solicitudes_hoy = solicitudes.filter(fecha_creacion__date=hoy)
    data_hoy = solicitudes_por_tipo(solicitudes_hoy)
    
    # --- SEMANA ---
    inicio_semana = datetime.fromisocalendar(hoy.year, semana, 1)
    fin_semana = datetime.fromisocalendar(hoy.year, semana, 7)
    solicitudes_semana = solicitudes.filter(
        fecha_creacion__range=[inicio_semana, fin_semana]
    )
    data_semana = solicitudes_por_tipo(solicitudes_semana)
    
    # --- MES ---
    solicitudes_mes = solicitudes.filter(
        fecha_creacion__year=hoy.year,
        fecha_creacion__month=hoy.month
    )
    data_mes = solicitudes_por_tipo(solicitudes_mes)
    
    def crear_grafico(data, titulo):
        if not data:
            return None
            
        fig, ax = plt.subplots(figsize=(8, 5))
        tipos = [item['tipo'] for item in data]
        totales = [item['total'] for item in data]
        
        colores_barras = ['#c9a24d', '#202146', '#d7d7d7', '#c9a24d', '#202146']
        bars = ax.bar(tipos, totales, color=colores_barras[:len(tipos)], width=0.6)
        
        max_valor = max(totales) if totales else 1
        ax.set_ylim(0, max_valor * 1.5)  
        
        ax.set_xlabel('Tipo de Solicitud', fontweight='bold', fontsize=11)
        ax.set_ylabel('Número de Solicitudes', fontweight='bold', fontsize=11)
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        
        tipos_formateados = []
        for tipo in tipos:
            if len(tipo) > 15:
                palabras = tipo.split()
                lineas = []
                linea_actual = []
                for palabra in palabras:
                    linea_actual.append(palabra)
                    if len(' '.join(linea_actual)) > 15:
                        lineas.append(' '.join(linea_actual[:-1]))
                        linea_actual = [palabra]
                if linea_actual:
                    lineas.append(' '.join(linea_actual))
                tipos_formateados.append('\n'.join(lineas))
            else:
                tipos_formateados.append(tipo)
        
        ax.set_xticks(range(len(tipos)))
        ax.set_xticklabels(tipos_formateados, fontsize=9, ha='center')
        plt.yticks(fontsize=10)
        
        for i, v in enumerate(totales):
            ax.text(i, v + (max_valor * 0.02), str(v), 
                   ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        ax.yaxis.grid(True, linestyle='--', alpha=0.3)
        ax.set_axisbelow(True)
        
        plt.tight_layout()
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        img_buffer.seek(0)
        plt.close()
        
        return img_buffer
    
    def agregar_seccion(data, titulo_seccion):
        subtitle = Paragraph(titulo_seccion, styles['Heading2'])
        elements.append(subtitle)
        elements.append(Spacer(1, 0.1*inch))
        
        if data:
            img_buffer = crear_grafico(data, titulo_seccion)
            if img_buffer:
                img = Image(img_buffer, width=6*inch, height=3.5*inch)
                elements.append(img)
                elements.append(Spacer(1, 0.3*inch))
        else:
            elements.append(Paragraph("No hay datos para este período", styles['Normal']))
            elements.append(Spacer(1, 0.3*inch))

    agregar_seccion(data_hoy, "Solicitudes de Hoy")
    agregar_seccion(data_semana, "Solicitudes de Esta Semana")
    agregar_seccion(data_mes, "Solicitudes de Este Mes")
    
    fecha_generacion = Paragraph(
        f"Reporte generado el {hoy.strftime('%d/%m/%Y')}",
        styles['Normal']
    )
    elements.append(Spacer(1, 0.3*inch))
    elements.append(fecha_generacion)
    
    doc.build(elements)
    
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response

def generar_csv_graficas(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="solicitudes.csv"'

    writer = csv.writer(response)
    
    # Encabezados del CSV
    writer.writerow([
        'ID', 
        'Usuario', 
        'Tipo de Solicitud', 
        'Folio', 
        'Fecha de Creacion'
    ])

    # Datos
    solicitudes = Solicitud.objects.all()

    for s in solicitudes:
        writer.writerow([
            s.id,
            s.usuario.username,
            s.tipo_solicitud.nombre,
            s.folio,
            s.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
        ])

    return response
>>>>>>> 26e440e98a7ff1615b49cc77a11509ba8a1bd3f1
