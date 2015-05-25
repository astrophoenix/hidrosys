# coding=utf-8
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.forms.models import model_to_dict
from django.db import transaction
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response, render
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from hidro_core.models import Equipo, EquipoMedicion, UmbralMedidaFisica
from hidro_core.forms import BuscarMedicionesForm, UmbralForm
#from django.core.mail import send_mail
import json
from django.core import serializers
from datetime import datetime, date
import xlwt
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import Table
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.units import mm

from django.forms.formsets import formset_factory
from django.contrib import messages


# Create your views here.
def login_usuario(request):
	message, message_success, message_error = None, None, None
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		
		acceso = authenticate(username = username, password = password)

		if acceso is not None:
			if acceso.is_active and acceso.is_superuser:
				login(request, acceso)
				return HttpResponseRedirect(reverse(dashboard))
			else:
				message_error = '1'
				message = 'Usuario No Autorizado'
		else:
			message_error = '1'
			message = 'Acceso Incorrecto'

	parametros = {
		"message_success" : message_success,
		"message_error" : message_error,
		"message" : message, 
	}

	response = render_to_response('login.html',parametros, context_instance=RequestContext(request))
	response.delete_cookie('message_success')
	response.delete_cookie('message_error')
	response.delete_cookie('message')
	return response
	
@login_required
def salir(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def dashboard(request):
	titulo_modulo = "Mediciones "
	usuario = None
	equipos_list = None
	
	usuario = request.user.username
	parametros = {
		"usuario" : usuario, 
		"titulo_modulo": titulo_modulo, 
	}
	return render_to_response('dashboard.html', parametros, context_instance=RequestContext(request))

@login_required
def configuracion(request):
	titulo_modulo = "Configuración "
	usuario, message, message_success, message_error = None, None, None, None

	if 'message_success' in request.COOKIES:
		message_success = request.COOKIES['message_success']
		message = request.COOKIES['message']

	
	ConfiguracionFormSet = formset_factory(UmbralForm, extra = 0)
	if request.method == "GET":
		configuraciones = UmbralMedidaFisica.objects.all().order_by("id").values()
		formset = ConfiguracionFormSet(initial = list(configuraciones))
				
	if request.method == "POST":
	    formset = ConfiguracionFormSet(request.POST)
	    if formset.is_valid():
			for form in formset:
				form.save()
			response = HttpResponseRedirect(reverse(configuracion))
			response.set_cookie('message_success', '1')
			response.set_cookie('message', 'Configuración Guardada.')
			return response
	    else:
			message_error = '1'
			message = 'Configuración no Guardada.'

	usuario = request.user.username
	parametros = {
		"message_success" : message_success,
		"message_error" : message_error,
		"message" : message, 
		"usuario" : usuario, 
		"titulo_modulo": titulo_modulo, 
		'formset': formset
	}

	response = render_to_response('configuracion.html',parametros, context_instance=RequestContext(request))
	response.delete_cookie('message_success')
	response.delete_cookie('message_error')
	response.delete_cookie('message')
	return response


@login_required
def consultar_equipos(request):
	titulo_modulo = "Equipos "
	usuario = None
	equipos_list = None
	
	form_buscar = BuscarEquipoForm()
	if 'nombre' in request.GET:
		nombre = request.GET['nombre']
		equipos_list = Equipo.objects.filter(nombre = nombre)
	else:
		equipos_list = Equipo.objects.all()

	paginator = Paginator(equipos_list, 5) # Show 25 contacts per page
	page = request.GET.get('page')

	try:
	    equipos = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    equipos = paginator.page(1)
	except EmptyPage:
	    # If page is out of range (e.g. 9999), deliver last page of results.
	    equipos = paginator.page(paginator.num_pages)

	usuario = request.user.username
	parametros = {
		"usuario" : usuario, 
		"titulo_modulo": titulo_modulo, 
		"equipos": equipos, 
		"form_buscar":form_buscar
	}
	return render_to_response('consultar_equipos.html',parametros, context_instance=RequestContext(request))
   

@login_required
def reporte(request):
	
	titulo_modulo = "Reporte de Mediciones"
	usuario = None
	mediciones_list = None
	message, message_error = None, None
	flag_fechas = 0
	form_buscar = BuscarMedicionesForm(request.GET)
	equipo = Equipo.objects.get(pk=1)
	mediciones_list = EquipoMedicion.objects.filter(equipo=equipo).order_by('-fecha_creacion')
	
	if 'anio' in request.GET:
		anio = request.GET['anio']
		if anio != '':
			mediciones_list = mediciones_list.filter(fecha_creacion__year=anio).order_by('-fecha_creacion')

	if 'mes' in request.GET:
		mes = int(request.GET['mes'])
		if mes > 0:
			mediciones_list = mediciones_list.filter(fecha_creacion__month=mes).order_by('-fecha_creacion')

	if 'fecha_desde' in request.GET:
		fecha_desde = request.GET['fecha_desde']
		if fecha_desde != '':
			fecha_desde = datetime.strptime(fecha_desde, "%d/%m/%Y").strftime("%Y-%m-%d")
			flag_fechas = flag_fechas + 1

	if 'fecha_hasta' in request.GET:
		fecha_hasta = request.GET['fecha_hasta']
		if fecha_hasta != '':
			fecha_hasta = datetime.strptime(fecha_hasta, "%d/%m/%Y").strftime("%Y-%m-%d")
			flag_fechas = flag_fechas + 1

	if flag_fechas == 2:
		if fecha_desde > fecha_hasta:
			message_error = '1'
			message = 'La Fecha Desde no puede ser mayor a la Fecha Hasta.'
			mediciones_list = mediciones_list.filter(fecha_creacion__year=1).order_by('-fecha_creacion')
		else:
			mediciones_list = EquipoMedicion.objects.filter(equipo=equipo).order_by('-fecha_creacion')
			mediciones_list = mediciones_list.filter(fecha_creacion__range=[fecha_desde, fecha_hasta]).order_by('-fecha_creacion')
	
	if flag_fechas == 1:
		message_error = '1'
		message = 'La Fecha Desde o Hasta no pueden estar vacías.'


	paginator = Paginator(mediciones_list, 25) # Show 25 contacts per page
	page = request.GET.get('page')

	try:
	    mediciones = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    mediciones = paginator.page(1)
	except EmptyPage:
	    # If page is out of range (e.g. 9999), deliver last page of results.
	    mediciones = paginator.page(paginator.num_pages)

	usuario = request.user.username
	parametros = {
		"usuario" : usuario, 
		"titulo_modulo": titulo_modulo, 
		"mediciones": mediciones, 
		"message_error" : message_error,
		"message" : message,
		"form_buscar":form_buscar
	}

	response = render_to_response('reporte.html', parametros, context_instance=RequestContext(request))
	response.delete_cookie('message_success')
	response.delete_cookie('message_error')
	response.delete_cookie('message')
	return response


@login_required
def medicionesxequipo(request, id = None, variable_fisica=None):
	
	umbrales_variables_fisicas = None
	equipo = Equipo.objects.get(pk = id)
	equipo_mediciones_list = EquipoMedicion.objects.filter(equipo_id=id).order_by('-fecha_creacion')

	paginator = Paginator(equipo_mediciones_list, 5) # Show 25 contacts per page
	page = request.GET.get('page')
	try:
	    equipo_mediciones = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    equipo_mediciones = paginator.page(1)
	except EmptyPage:
	    # If page is out of range (e.g. 9999), deliver last page of results.
	    equipo_mediciones = paginator.page(paginator.num_pages)

	if variable_fisica != "compas_mag" or variable_fisica != "acelerometro":
		umbrales_variables_fisicas = UmbralMedidaFisica.objects.get(variable_fisica = variable_fisica)
	
	
	titulo_modulo = "Panel de Monitoreo "
	usuario = request.user.username
	parametros = {	"titulo_modulo": titulo_modulo, 
					"usuario" : usuario, "variable_fisica" : variable_fisica, 
					"equipo_mediciones": equipo_mediciones, 
					"equipo": equipo, 'umbrales_variables_fisicas' : umbrales_variables_fisicas}
	return render_to_response('mediciones.html',parametros, context_instance=RequestContext(request))


@login_required
def medicionesxequipo_ajax(request, id = None):
	
	var_fisica_umbrales = None
	equipo = Equipo.objects.get(pk = id)
	equipo_mediciones_list = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion')
	variable_fisica = request.GET['variable_fisica']
	equipo_mediciones = equipo_mediciones_list[:10]

	if variable_fisica != "compas_mag":
		var_fisica_umbrales = UmbralMedidaFisica.objects.get(variable_fisica = variable_fisica)
	
	
	parametros = {	"var_fisica_umbrales": var_fisica_umbrales, 
					"variable_fisica": variable_fisica, 
					"equipo_mediciones": equipo_mediciones, "equipo": equipo}

	return render_to_response('mediciones_ajax.html', parametros, context_instance=RequestContext(request))


@login_required
def graficasxequipo(request, id = None):
	equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion')
	usuario = request.user.username
	parametros = {"equipo_mediciones": equipo_mediciones, "usuario" : usuario}
	return render_to_response('graficas_estadisticas.html',parametros, context_instance=RequestContext(request))
	

@login_required
def obtener_datos_medidos_equipo(request, id = None):
	equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion')[:1]
	json_data = serializers.serialize("json", equipo_mediciones)
	return HttpResponse(json_data, content_type='application/json')


@login_required
def obtener_umbrales(request, id = None):
	umbrales = UmbralMedidaFisica.objects.all().order_by("id")
	json_umbrales = serializers.serialize("json", umbrales)
	return HttpResponse(json_umbrales, content_type='application/json')


def addPageNumber(canvas, doc):
    """
    Add the page number
    """
    page_num = canvas.getPageNumber()
    text = "Página %s" % page_num
    canvas.drawRightString(255*mm, 13*mm, text)

@login_required
def exportar_pdf(request, id):
	
	message_error, message = None, None
	flag_fechas = 0

	equipo = Equipo.objects.get(pk=id)
	equipo_mediciones = EquipoMedicion.objects.filter(equipo=equipo).order_by('-fecha_creacion')
	
	if 'anio' in request.GET:
		anio = request.GET['anio']
		if anio != '':
			equipo_mediciones = equipo_mediciones.filter(fecha_creacion__year=anio).order_by('-fecha_creacion')

	if 'mes' in request.GET:
		mes = int(request.GET['mes'])
		if mes > 0:
			equipo_mediciones = equipo_mediciones.filter(fecha_creacion__month=mes).order_by('-fecha_creacion')

	if 'fecha_desde' in request.GET:
		fecha_desde = request.GET['fecha_desde']
		if fecha_desde != '':
			fecha_desde = datetime.strptime(fecha_desde, "%d/%m/%Y").strftime("%Y-%m-%d")
			flag_fechas = flag_fechas + 1

	if 'fecha_hasta' in request.GET:
		fecha_hasta = request.GET['fecha_hasta']
		if fecha_hasta != '':
			fecha_hasta = datetime.strptime(fecha_hasta, "%d/%m/%Y").strftime("%Y-%m-%d")
			flag_fechas = flag_fechas + 1

	if flag_fechas == 2:
		if fecha_desde > fecha_hasta:
			message_error = '1'
			message = 'La Fecha Desde no puede ser mayor a la Fecha Hasta.'
			equipo_mediciones = equipo_mediciones.filter(fecha_creacion__year=1).order_by('-fecha_creacion')
		else:
			equipo_mediciones = EquipoMedicion.objects.filter(equipo=equipo).order_by('-fecha_creacion')
			equipo_mediciones = equipo_mediciones.filter(fecha_creacion__range=[fecha_desde, fecha_hasta]).order_by('-fecha_creacion')
	
	if flag_fechas == 1:
		message_error = 1
		message = 'La Fecha Desde o Hasta no pueden estar vacías.'


	if message_error == 1:
		response = HttpResponseRedirect(reverse(reporte))
		return response

	response = HttpResponse(content_type='application/pdf')
	fecha_actual = datetime.now().date()
	pdf_name = equipo.nombre.replace(" ", "") + "_" + str(fecha_actual) + ".pdf"


	# la linea 26 es por si deseas descargar el pdf a tu computadora
	# response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
	buff = BytesIO()
	doc = SimpleDocTemplate(buff,
		                        pagesize=landscape(letter),
		                        rightMargin=72,
		                        leftMargin=72,
                        		topMargin=50,
                        		bottomMargin=30
	                        )
	mediciones = []
	styles = getSampleStyleSheet()
	titulo = Paragraph("Reporte Mediciones", styles['Heading1'])
	mediciones.append(titulo)
	fecha_actual = fecha_actual.strftime("%d/%m/%Y")
	descripcion = Paragraph("Fecha Reporte : " + str(fecha_actual), styles['Heading2'])
	mediciones.append(descripcion)


	headings = ('Fecha', 'Hora', 'Temp. Aire(°C)', 'Hum. Aire(%)', 'Temp. Agua(°C)', 'Ilum.(Lux)', 'Viento(m/s)', 'Compás(°)', 'Aceleración(m/s²)')

	
	data = []
	for d in equipo_mediciones:
		fecha = d.fecha_creacion.strftime("%d/%m/%Y")
		hora = d.fecha_creacion.strftime("%H:%M:%S")
		temperatura_aire = d.temperatura
		humedad_aire = d.humedad
		temperatura_agua = d.temperatura_agua
		intensidad_luz = d.intensidad_luz
		viento = d.viento
		compas_mag = d.compaz_mag
		acelerometro = "x: " + str(d.acelerometro_x) + "\ny: " + str(d.acelerometro_y) + "\nz: " + str(d.acelerometro_z)
		data.append([fecha, hora, temperatura_aire,humedad_aire,temperatura_agua,intensidad_luz,viento,compas_mag,acelerometro])
	
	colwidths = [1*inch, 1*inch, 1.1*inch, 1*inch, 1.2*inch, 1*inch, 1*inch, .9*inch, 1.2*inch]
	
	t = Table([headings] + data, colwidths)
	t.setStyle(TableStyle(
	    [
	        ('GRID', (0, 0), (8, -1), 1, colors.black),
	        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
	        ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
	    ]
	))
	mediciones.append(t)
	doc.build(mediciones, onFirstPage=addPageNumber, onLaterPages=addPageNumber)
	response.write(buff.getvalue())
	buff.close()
	return response



@login_required
def exportar_excel(request, id):

	message_error, message = None, None
	flag_fechas = 0

	equipo = Equipo.objects.get(pk=id)
	equipo_mediciones = EquipoMedicion.objects.filter(equipo=equipo).order_by('-fecha_creacion')
	
	if 'anio' in request.GET:
		anio = request.GET['anio']
		if anio != '':
			equipo_mediciones = equipo_mediciones.filter(fecha_creacion__year=anio).order_by('-fecha_creacion')

	if 'mes' in request.GET:
		mes = int(request.GET['mes'])
		
		if mes > 0:
			equipo_mediciones = equipo_mediciones.filter(fecha_creacion__month=mes).order_by('-fecha_creacion')

	if 'fecha_desde' in request.GET:
		fecha_desde = request.GET['fecha_desde']
		if fecha_desde != '':
			fecha_desde = datetime.strptime(fecha_desde, "%d/%m/%Y").strftime("%Y-%m-%d")
			flag_fechas = flag_fechas + 1

	if 'fecha_hasta' in request.GET:
		fecha_hasta = request.GET['fecha_hasta']
		if fecha_hasta != '':
			fecha_hasta = datetime.strptime(fecha_hasta, "%d/%m/%Y").strftime("%Y-%m-%d")
			flag_fechas = flag_fechas + 1

	if flag_fechas == 2:
		if fecha_desde > fecha_hasta:
			message_error = '1'
			message = 'La Fecha Desde no puede ser mayor a la Fecha Hasta.'
			equipo_mediciones = equipo_mediciones.filter(fecha_creacion__year=1).order_by('-fecha_creacion')
		else:
			equipo_mediciones = EquipoMedicion.objects.filter(equipo=equipo).order_by('-fecha_creacion')
			equipo_mediciones = equipo_mediciones.filter(fecha_creacion__range=[fecha_desde, fecha_hasta]).order_by('-fecha_creacion')
	
	if flag_fechas == 1:
		message_error = 1
		message = 'La Fecha Desde o Hasta no pueden estar vacías.'


	if message_error == 1:
		response = HttpResponseRedirect(reverse(reporte))
		return response	
	
	
	book = xlwt.Workbook(encoding='utf8')
	sheet = book.add_sheet('my_sheet')   
	formato_estilo_default = xlwt.Style.default_style

	# Adding style for cell
	# Create Alignment
	alignment = xlwt.Alignment()
	# horz May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT,     
	# HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL,
	# HORZ_DISTRIBUTED
	alignment.horz = xlwt.Alignment.VERT_CENTER
	# May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED,
	# VERT_DISTRIBUTED
	alignment.vert = xlwt.Alignment.VERT_TOP
	formato_estilo_cabecera = xlwt.XFStyle() # Create Style
	formato_estilo_cabecera.alignment = alignment # Add Alignment to Style

	# font
	font = xlwt.Font()
	font.bold = True
	font.height = 200
	sheet.col(2).width = 256 * len('Temp. Aire(°C)')
	sheet.col(3).width = 256 * len('Hum. Aire(%)')
	sheet.col(4).width = 256 * len('Temp. Agua(°C)')
	sheet.col(5).width = 256 * len('Ilum.(Lux)')
	sheet.col(6).width = 256 * len('Viento(m/s)')
	sheet.col(7).width = 256 * len('Compás(°)')
	sheet.col(8).width = 256 * len('Aceleración(m/s²)')
	formato_estilo_cabecera.font = font

	formato_estilo_alerta = xlwt.XFStyle() # Create Style
	pattern = xlwt.Pattern()
	pattern.pattern = xlwt.Pattern.SOLID_PATTERN
	pattern.pattern_fore_colour = xlwt.Style.colour_map['red']
	formato_estilo_alerta.pattern = pattern


	formato_estilo_titulo = xlwt.XFStyle() # Create Style
	formato_estilo_titulo.alignment = alignment # Add Alignment to Style
	font = xlwt.Font()
	font.bold = True
	font.height = 300
	formato_estilo_titulo.font = font
	sheet.write(1, 0, "REPORTE MEDICIONES", formato_estilo_titulo)
	sheet.row(1).height = 256*2
	fecha_actual = datetime.now().date()

	sheet.write(2, 0, "Fecha : "+str(fecha_actual.strftime("%d/%m/%Y")), formato_estilo_default)

	# Cabecera del excel
	header = ['Fecha', 'Hora', 'Temp. Aire(°C)', 'Hum. Aire(%)', 'Temp. Agua(°C)', 'Ilum.(Lux)', 'Viento(m/s)', 'Compás(°)', 'Aceleración(m/s²)']
	for hcol, hcol_data in enumerate(header): # [(0,'Header 1'), (1, 'Header 2'), (2,'Header 3'), (3,'Header 4')]
		sheet.write(3, hcol, hcol_data, formato_estilo_cabecera)
	data = []
	for d in equipo_mediciones:
		fecha = d.fecha_creacion.strftime("%d/%m/%Y")
		hora = d.fecha_creacion.strftime("%H:%M:%S")
		temperatura_aire = d.temperatura
		humedad_aire = d.humedad
		temperatura_agua = d.temperatura_agua
		intensidad_luz = d.intensidad_luz
		viento = d.viento
		compas_mag = d.compaz_mag
		acelerometro = "x: " + str(d.acelerometro_x) + " y: " + str(d.acelerometro_y) + " z: " + str(d.acelerometro_z)
		data.append([fecha, hora, temperatura_aire,humedad_aire,temperatura_agua,intensidad_luz,viento,compas_mag,acelerometro])
		

	for row, row_data in enumerate(data, start=4): # start from row no.1
		formato = formato_estilo_default
	   	for col, col_data in enumerate(row_data):
	   	# 	if col == 2:
	   	# 		if col_data > umbral_variable_fisica:
					# formato = formato_estilo_alerta	   			   			
			sheet.write(row, col, col_data, formato)

	equipo = Equipo.objects.get(pk = id)
	nombre_archivo = equipo.nombre.replace(" ", "") + "_" + str(fecha_actual) + ".xls"
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename='+nombre_archivo
	book.save(response)
	return response

def linechart(request):

    #instantiate a drawing object
    import chart
    d = chart.MyLineChartDrawing()

    #extract the request params of interest.
    #I suggest having a default for everything.
    
    d.height = 500
    d.chart.height = 500
    
    d.width = 500
    d.chart.width = 500
   
    d.title._text = request.session.get('Some custom title')
    
    d.XLabel._text = request.session.get('X Axis Labell')
    d.YLabel._text = request.session.get('Y Axis Label')

    d.chart.data = [((1,1), (2,2), (2.5,1), (3,3), (4,5)),((1,2), (2,3), (2.5,2), (3.5,5), (4,6))]
   

    
    labels =  ["Label One","Label Two"]
    if labels:
        # set colors in the legend
        d.Legend.colorNamePairs = []
        for cnt,label in enumerate(labels):
                d.Legend.colorNamePairs.append((d.chart.lines[cnt].strokeColor,label))


    #get a GIF (or PNG, JPG, or whatever)
    binaryStuff = d.asString('gif')
    return HttpResponse(binaryStuff, 'image/gif')

@login_required
def registrar_obtener_equipo(request, id = None):
	equipo = None
	error_msg = None
	if request.method == 'POST':
		form_equipo = EquipoForm(request.POST)
		if form_equipo.is_valid():
			equipo = form_equipo.save(request.user)
			response = HttpResponseRedirect(reverse(registrar_obtener_equipo, args = [equipo.id]))
			return response
	else:
		if id:
			equipo = Equipo.objects.get(pk = id)
			form_equipo = EquipoForm(initial=model_to_dict(equipo))
		else:
			form_equipo = EquipoForm()

	usuario = request.user.username
	parametros = {"titulo_modulo" : "Equipo", "usuario" : usuario, "form_equipo" : form_equipo}
	return render_to_response('equipo.html',parametros, context_instance=RequestContext(request))
	

@login_required
def eliminar_equipo(request, id = None):
	equipo = Equipo.objects.get(pk = id).delete()
	return HttpResponseRedirect(reverse(consultar_equipos))
