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
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from hidro_core.models import Equipo, EquipoMedicion, UmbralMedidaFisica
from hidro_core.forms import EquipoForm, BuscarEquipoForm, UmbralForm
#from django.core.mail import send_mail
import json
from django.core import serializers
from datetime import datetime, date
import xlwt
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from django.forms.formsets import formset_factory

# Create your views here.
def login_usuario(request):
	
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		
		acceso = authenticate(username = username, password = password)

		if acceso is not None:
			if acceso.is_active and acceso.is_superuser:
				login(request, acceso)
				return HttpResponseRedirect(reverse(dashboard))
				#return HttpResponseRedirect(reverse(consultar_equipos))
			else:
				errors = 'Usuario No Autorizado'
				return render_to_response('login.html', context_instance=RequestContext(request))
	
		
	return render_to_response('login.html', context_instance=RequestContext(request))

@login_required
def salir(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def dashboard(request):
	titulo_modulo = "Mediciones "
	usuario = None
	equipos_list = None
	
	# form_buscar = BuscarEquipoForm()
	# if 'nombre' in request.GET:
	# 	nombre = request.GET['nombre']
	# 	equipos_list = Equipo.objects.filter(nombre = nombre)
	# else:
	# 	equipos_list = Equipo.objects.all()

	# paginator = Paginator(equipos_list, 5) # Show 25 contacts per page
	# page = request.GET.get('page')
	# try:
	#     equipos = paginator.page(page)
	# except PageNotAnInteger:
	#     # If page is not an integer, deliver first page.
	#     equipos = paginator.page(1)
	# except EmptyPage:
	#     # If page is out of range (e.g. 9999), deliver last page of results.
	#     equipos = paginator.page(paginator.num_pages)

	usuario = request.user.username
	parametros = {
		"usuario" : usuario, 
		"titulo_modulo": titulo_modulo, 
		#"equipos": equipos, 
		#"form_buscar":form_buscar
	}
	return render_to_response('dashboard.html',parametros, context_instance=RequestContext(request))


# @login_required
# def configuracion(request, id = None):
# 	titulo_modulo = "Configuraciones "
# 	usuario = None
# 	formset = None
# 	if request.method == "GET":
# 		if id:
# 			configuracion = UmbralMedidaFisica.objects.get(pk = id)
# 			form_configuracion = UmbralForm(instance = configuracion)
# 		else:
# 			#formset_configuracion = formset_factory(UmbralForm, extra=3)

# 			ConfiguracionFormSet = formset_factory(UmbralForm, extra=3)
# 			#form_configuracion = UmbralForm()
# 	if request.method == "POST":
# 		ConfiguracionFormSet = formset_factory(UmbralForm, extra=3)
# 		formset = ConfiguracionFormSet(request.POST)

#         if(formset.is_valid()):
#             #message = "Thank you"
#             for form in formset:
#                 #print form
#                 form.save()

# 		#formset = QuestionFormSet(request.POST)
# 		#formset_configuracion = UmbralForm(request.POST)
# 		# formset_configuracion = formset_factory(UmbralForm)
# 		# form_configuracion.is_valid():
# 		# 	configuracion = form_configuracion.save()
# 		# 	return HttpResponseRedirect(reverse(configuracion, args = [configuracion.id]))
# 		# 	#response = redirect(reverse(agregarDescuento, args = [prestamo.id]))
		

# 	usuario = request.user.username
# 	parametros = {
# 		"usuario" : usuario, 
# 		"titulo_modulo": titulo_modulo, 
# 		"formset" : ConfiguracionFormSet()
# 	}
# 	return render_to_response('configuracion.html',parametros, context_instance=RequestContext(request))

@login_required
def configuracion(request):
	titulo_modulo = "Configuración "
	usuario = None
	ConfiguracionFormSet = formset_factory(UmbralForm, extra = 0)

	if request.method == "GET":
		configuraciones = UmbralMedidaFisica.objects.all().order_by("id").values()
		formset = ConfiguracionFormSet(initial = list(configuraciones))
				
	if request.method == "POST":
	    formset = ConfiguracionFormSet(request.POST)

	    if formset.is_valid():
	        for form in formset:
	            form.save()
		return HttpResponseRedirect(reverse(configuracion))

	    else:
	        print "Something went wrong"

	
	usuario = request.user.username
	parametros = {
		"usuario" : usuario, 
		"titulo_modulo": titulo_modulo, 
		'formset': formset
	}
	return render_to_response('configuracion.html',parametros, context_instance=RequestContext(request))


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
def medicionesxequipo(request, id = None, variable_fisica=None):
	equipo = Equipo.objects.get(pk = id)
	equipo_mediciones_list = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion')

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

	equipo_mediciones_ultimas = equipo_mediciones[:3]
	titulo_modulo = "Mediciones "
	usuario = request.user.username
	parametros = {"titulo_modulo": titulo_modulo, "usuario" : usuario, "variable_fisica" : variable_fisica, "equipo_mediciones": equipo_mediciones, "equipo": equipo}
	return render_to_response('mediciones.html',parametros, context_instance=RequestContext(request))


@login_required
def medicionesxequipo_ajax(request, id = None):
	equipo = Equipo.objects.get(pk = id)
	equipo_mediciones_list = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion')
	variable_fisica = request.GET['variable_fisica']
	equipo_mediciones = equipo_mediciones_list[:10]
	umbrales = UmbralMedidaFisica.objects.all()
	umbral = {
		"temperatura_aire" : umbrales[0].umbral,
		"humedad_aire" : umbrales[1].umbral,
		"intensidad_luz" :umbrales[3].umbral, 
	}

	parametros = {"umbral": umbral, "variable_fisica": variable_fisica, "equipo_mediciones": equipo_mediciones, "equipo": equipo}
	return render_to_response('mediciones_ajax.html',parametros, context_instance=RequestContext(request))

@login_required
def medicionesxequipoactual(request, id = None):
	if id:
		equipo_mediciones_list = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion')
		paginator = Paginator(equipo_mediciones_list, 5) # Show 25 contacts per page
		page = request.GET.get('page')
		try:
		    equipo_mediciones = paginator.page(page)
		except PageNotAnInteger:
		    equipo_mediciones = paginator.page(1)
		except EmptyPage:
		    equipo_mediciones = paginator.page(paginator.num_pages)

		equipo_mediciones_ultimas = equipo_mediciones[:3]
		for mediciones in equipo_mediciones_ultimas:
			if mediciones.temperatura > 1 or mediciones.humedad > 1 or mediciones.intensidad_luz > 1:
				mensaje = 'temperatura : ' + str(mediciones.temperatura) + "\n"
				mensaje += 'humedad : ' + str(mediciones.humedad) + "\n"
				mensaje += 'intensidad_luz : ' + str(mediciones.intensidad_luz) + "\n"
				#print str(mensaje)
				#mail_origen = 'galexanderomero24@gmail.com'
				#mail_destino = 'galexanderomero24@gmail.com'
				#send_mail('Arlerta en Medición', mensaje, mail_origen,[mail_destino], fail_silently=False)

		equipo = Equipo.objects.get(pk = id)
		titulo_modulo = "Mediciones " + str(equipo_mediciones[0].equipo.nombre)
		usuario = request.user.username
		parametros = {
			"titulo_modulo": titulo_modulo, 
			"equipo_mediciones": equipo_mediciones, 
			"equipo": equipo,
			"usuario" : usuario
		}
		return render_to_response('mediciones.html',parametros, context_instance=RequestContext(request))
	
	return HttpResponseRedirect(reverse(consultar_equipos))

@login_required
def graficasxequipo(request, id = None):
	equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion')
	usuario = request.user.username
	parametros = {"equipo_mediciones": equipo_mediciones, "usuario" : usuario}
	return render_to_response('graficas_estadisticas.html',parametros, context_instance=RequestContext(request))
	

@login_required
def obtener_datos_medidos_equipo(request, id = None):
	equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion')[:10]
	json_data = serializers.serialize("json", equipo_mediciones)
	return HttpResponse(json_data, content_type='application/json')


@login_required
def obtener_umbrales(request, id = None):
	umbrales = UmbralMedidaFisica.objects.all().order_by("id")
	json_umbrales = serializers.serialize("json", umbrales)
	return HttpResponse(json_umbrales, content_type='application/json')


@login_required
def exportar_excel(request, id):
	variable_fisica = request.GET['variable_fisica']

	umbrales = UmbralMedidaFisica.objects.all()
	if variable_fisica =="temperatura_aire":
		equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion').values('fecha_creacion','temperatura')
		key = 'temperatura'
		umbral_variable_fisica =  umbrales[0].umbral
		header_variable_fisica = 'Tempertura [°C]'		
	elif variable_fisica =="humedad_aire":
		equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion').values('fecha_creacion', 'humedad')
		key = 'humedad'
		umbral_variable_fisica =  umbrales[1].umbral
		header_variable_fisica = 'Humedad [%]'
	elif variable_fisica =="intensidad_luz":
		key = 'intensidad_luz'
		header_variable_fisica = 'Intensidad Luz [%]'
		umbral_variable_fisica =  umbrales[3].umbral
		equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion').values('fecha_creacion', 'intensidad_luz')
	
	
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
	sheet.col(2).width = 256 * len(header_variable_fisica)
	formato_estilo_cabecera.font = font

	formato_estilo_alerta = xlwt.XFStyle() # Create Style
	pattern = xlwt.Pattern()
	pattern.pattern = xlwt.Pattern.SOLID_PATTERN
	pattern.pattern_fore_colour = xlwt.Style.colour_map['red']
	formato_estilo_alerta.pattern = pattern

	# Cabecera del excel
	header = ['Fecha', 'Hora', header_variable_fisica]
	for hcol, hcol_data in enumerate(header): # [(0,'Header 1'), (1, 'Header 2'), (2,'Header 3'), (3,'Header 4')]
		sheet.write(0, hcol, hcol_data, formato_estilo_cabecera)
	data = []
	for d in list(equipo_mediciones):
		fecha = d['fecha_creacion'].strftime("%d/%m/%Y")
		hora = d['fecha_creacion'].strftime("%H:%M:%S")
		tipo_variable = d[key]
		data.append([fecha, hora, tipo_variable])
		
	
	for row, row_data in enumerate(data, start=1): # start from row no.1
		formato = formato_estilo_default
	   	for col, col_data in enumerate(row_data):
	   		if col == 2:
	   			if col_data > umbral_variable_fisica:
					formato = formato_estilo_alerta	   			   			
			sheet.write(row, col, col_data, formato)

	fecha_actual = datetime.now().date()
	equipo = Equipo.objects.get(pk = id)
	nombre_archivo = equipo.nombre.replace(" ", "") + "_" + str(fecha_actual) + ".xls"
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename='+nombre_archivo
	book.save(response)
	return response


@login_required
def exportar_pdf(request, id):
	
	variable_fisica = request.GET['variable_fisica']

	umbrales = UmbralMedidaFisica.objects.all()
	if variable_fisica =="temperatura_aire":
		equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion').values('fecha_creacion','temperatura')
		key = 'temperatura'
		umbral_variable_fisica =  umbrales[0].umbral
		header_variable_fisica = 'Tempertura [°C]'		
	elif variable_fisica =="humedad_aire":
		equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion').values('fecha_creacion', 'humedad')
		key = 'humedad'
		umbral_variable_fisica =  umbrales[1].umbral
		header_variable_fisica = 'Humedad [%]'
	elif variable_fisica =="intensidad_luz":
		key = 'intensidad_luz'
		header_variable_fisica = 'Intensidad Luz [%]'
		umbral_variable_fisica =  umbrales[3].umbral
		equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion').values('fecha_creacion', 'intensidad_luz')
	
	response = HttpResponse(content_type='application/pdf')

	fecha_actual = datetime.now().date()
	equipo = Equipo.objects.get(pk = id)
	pdf_name = equipo.nombre.replace(" ", "") + "_" + str(fecha_actual) + ".pdf"


	# la linea 26 es por si deseas descargar el pdf a tu computadora
	# response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
	buff = BytesIO()
	doc = SimpleDocTemplate(buff,
	                        pagesize=letter,
	                        rightMargin=40,
	                        leftMargin=40,
	                        topMargin=60,
	                        bottomMargin=18,
	                        )
	mediciones = []
	styles = getSampleStyleSheet()
	header = Paragraph("Mediciones", styles['Heading1'])
	mediciones.append(header)
	headings = ('Fecha', 'Hora', header_variable_fisica)


	data = []
	for d in list(equipo_mediciones):
		fecha = d['fecha_creacion'].strftime("%d/%m/%Y")
		hora = d['fecha_creacion'].strftime("%H:%M:%S")
		tipo_variable = d[key]
		data.append([fecha, hora, tipo_variable])
	#print allclientes

	t = Table([headings] + data)
	t.setStyle(TableStyle(
	    [
	        ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
	        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
	        ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
	    ]
	))
	mediciones.append(t)
	doc.build(mediciones)
	response.write(buff.getvalue())
	buff.close()
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
