# coding=utf-8
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
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
#from hidro_core.forms import EquipoForm
import json
from django.core import serializers

# Create your views here.
def login_usuario(request):
	
	if request.method == 'POST':
		#form_login = AuthenticationForm(request.POST)
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

def salir(request):
    logout(request)
    #return render(request, 'login.html')
    return render_to_response('login.html', context_instance=RequestContext(request))


@login_required
def dashboard(request):
    titulo_modulo = "Equipos "
    usuario = None
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
    return render_to_response('dashboard.html',{"usuario" : usuario, "titulo_modulo": titulo_modulo, "equipos": equipos}, context_instance=RequestContext(request))
   
@login_required
def medicionesxequipo(request, id = None):
	#print "equipo_id" + str(id)
	#try:
	equipo = Equipo.objects.get(pk = id)
	equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion')
	titulo_modulo = "Mediciones " + str(equipo_mediciones[0].equipo.nombre)
	return render_to_response('equipo_mediciones.html',{"titulo_modulo": titulo_modulo, "equipo_mediciones": equipo_mediciones, "equipo": equipo}, context_instance=RequestContext(request))
	#except:
	#    return HttpResponseRedirect(reverse(dashboard))

@login_required
def medicionesxequipoactual(request, id = None):
	try:
		if id:
			equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion')
			equipo = Equipo.objects.get(pk = id)
			titulo_modulo = "Mediciones " + str(equipo_mediciones[0].equipo.nombre)
			parametros = {
				"titulo_modulo": titulo_modulo, 
				"equipo_mediciones": equipo_mediciones, 
				"equipo": equipo
			}
			return render_to_response('mediciones.html',parametros, context_instance=RequestContext(request))
	except ApplicationError, msg:
		print str(msg)
	
	return HttpResponseRedirect(reverse(dashboard))

@login_required
def graficasxequipo(request, id = None):
	#try:
	equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion')
		#titulo_modulo = "Graficas " + str(equipo_mediciones[0].equipo.nombre)
	return render_to_response('graficas_estadisticas.html',{"equipo_mediciones": equipo_mediciones}, context_instance=RequestContext(request))
	#except:
	    #return HttpResponseRedirect(reverse(dashboard))

@login_required
def obtener_datos_medidos_equipo(request, id = None):
    equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion')[:10]
    data = serializers.serialize("json", equipo_mediciones)
    return HttpResponse(data, content_type='application/json')

# @login_required
# def registrar_obtener_equipo(request, id = None):
# 	equipo = None
# 	error_msg = None
# 	if request.method == 'POST':
# 		form_equipo = EquipoForm(request.POST)
# 		if form_equipo.is_valid():
# 			try:
# 				equipo = form_equipo.save()
# 				response = redirect(reverse(registrar_obtener_equipo, args = [equipo.id]))
# 				return response
# 			except ApplicationError,e:
# 				error_msg = str(e)
# 				transaction.rollback()
# 			except:
# 				transaction.rollback()
# 				raise
# 	else:
# 		form_equipo = EquipoForm()

# 	usuario = request.user.username
# 	parametros = {"titulo_modulo" : "Equipo", "usuario" : usuario, "form_equipo" : form_equipo}
# 	return render_to_response('equipo.html',parametros, context_instance=RequestContext(request))
	
	
	
	
	
	



