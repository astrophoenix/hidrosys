from django.conf.urls import patterns, include, url
from django.contrib import admin
from hidro_core.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hidro_sys.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', "hidro_core.views.login_usuario"),
    #url(r'^logout/', "hidro_core.views.logout"),
    url(r'^registrar_obtener_equipo/', "hidro_core.views.registrar_obtener_equipo"),
    url(r'^registrar_obtener_equipo/(?P<id>\d+)/$', "hidro_core.views.registrar_obtener_equipo"),
	url(r'^dashboard/', "hidro_core.views.dashboard"),
	url (r'^medicionesxequipo/(?P<id>\d+)/$', 'hidro_core.views.medicionesxequipo'),
	url (r'^medicionesxequipoactual/(?P<id>\d+)/$', 'hidro_core.views.medicionesxequipoactual'),
	url (r'^graficasxequipo/(?P<id>\d+)/$', 'hidro_core.views.graficasxequipo'),
	url (r'^obtener_datos_medidos_equipo/(?P<id>\d+)/$', 'hidro_core.views.obtener_datos_medidos_equipo')
	#url(r'^logout/', logout),
)
