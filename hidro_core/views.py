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
from hidro_core.models import Equipo, EquipoMedicion
from hidro_core.forms import EquipoForm, BuscarEquipoForm
#from django.core.mail import send_mail
import json
from django.core import serializers

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
	titulo_modulo = "Equipos "
	usuario = None
	equipos_list = None
	
	form_buscar = BuscarEquipoForm()
	if 'nombre' in request.GET:
		nombre = request.GET['nombre']
		equipos_list = Equipo.objects.filter(nombre = nombre)
	else:
		equipos_list = Equipo.objects.all()

	paginator = Paginator(equipos_list, 25) # Show 25 contacts per page
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
	return render_to_response('dashboard.html',parametros, context_instance=RequestContext(request))
   
@login_required
def medicionesxequipo(request, id = None):
	equipo = Equipo.objects.get(pk = id)
	equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion')
	equipo_mediciones_ultimas = equipo_mediciones[:3]
	titulo_modulo = "Mediciones " + str(equipo_mediciones[0].equipo.nombre)
	usuario = request.user.username
	parametros = {"titulo_modulo": titulo_modulo, "usuario" : usuario, "equipo_mediciones": equipo_mediciones, "equipo": equipo}
	return render_to_response('equipo_mediciones.html',parametros, context_instance=RequestContext(request))

@login_required
def medicionesxequipoactual(request, id = None):
	if id:
		equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion')
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
	
	
	return HttpResponseRedirect(reverse(dashboard))

@login_required
def graficasxequipo(request, id = None):
	equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion')
	usuario = request.user.username
	parametros = {"equipo_mediciones": equipo_mediciones, "usuario" : usuario}
	return render_to_response('graficas_estadisticas.html',parametros, context_instance=RequestContext(request))
	

@login_required
def obtener_datos_medidos_equipo(request, id = None):
    equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion')[:10]
    data = serializers.serialize("json", equipo_mediciones)
    return HttpResponse(data, content_type='application/json')


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
	return HttpResponseRedirect(reverse(dashboard))
