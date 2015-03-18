# coding=utf-8
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
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

@login_required
def dashboard(request):
    titulo_modulo = "Equipos "
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

    return render_to_response('dashboard.html',{"titulo_modulo": titulo_modulo, "equipos": equipos}, context_instance=RequestContext(request))
   
@login_required
def medicionesxequipo(request, id):
	#print "equipo_id" + str(id)
	#try:
	equipo = Equipo.objects.get(pk = id)
	equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion')
	titulo_modulo = "Mediciones " + str(equipo_mediciones[0].equipo.nombre)
	return render_to_response('equipo_mediciones.html',{"titulo_modulo": titulo_modulo, "equipo_mediciones": equipo_mediciones, "equipo": equipo}, context_instance=RequestContext(request))
	#except:
	#    return HttpResponseRedirect(reverse(dashboard))

@login_required
def medicionesxequipoactual(request, id):
	try:
		equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion')
		equipo = Equipo.objects.get(pk = id)
		titulo_modulo = "Mediciones " + str(equipo_mediciones[0].equipo.nombre)
		return render_to_response('mediciones.html',{"titulo_modulo": titulo_modulo, "equipo_mediciones": equipo_mediciones, "equipo": equipo}, context_instance=RequestContext(request))
	except:
	    return HttpResponseRedirect(reverse(dashboard))

@login_required
def graficasxequipo(request, id):
	#try:
	equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion')
		#titulo_modulo = "Graficas " + str(equipo_mediciones[0].equipo.nombre)
	return render_to_response('graficas_estadisticas.html',{"equipo_mediciones": equipo_mediciones}, context_instance=RequestContext(request))
	#except:
	    #return HttpResponseRedirect(reverse(dashboard))

@login_required
def obtener_datos_medidos_equipo(request, id):
    equipo_mediciones = EquipoMedicion.objects.filter(equipo_id = id).order_by('-fecha_creacion')[:10]
    #limit = 10
    #count = equipo_mediciones.count()
    #equipo_mediciones = equipo_mediciones.order_by('-fecha_creacion')[count-limit:]
    data = serializers.serialize("json", equipo_mediciones)
    return HttpResponse(data, content_type='application/json')
	
	
	
	
	
	



