from django.conf.urls import patterns, include, url
from django.contrib import admin
from hidro_core.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hidro_sys.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', "hidro_core.views.login_usuario"),
    url(r'^logout/$', "hidro_core.views.salir"),
    url(r'^registrar_obtener_equipo/$', "hidro_core.views.registrar_obtener_equipo"),
    url(r'^registrar_obtener_equipo/(?P<id>\d+)/$', "hidro_core.views.registrar_obtener_equipo"),
    url(r'^dashboard/$', "hidro_core.views.dashboard"),
    url(r'^configuracion/$', "hidro_core.views.configuracion"),
    url(r'^reporte/$', "hidro_core.views.reporte"),
    url(r'^notificaciones/$', "hidro_core.views.notificaciones"),
    url(r'^notificacion/$', "hidro_core.views.notificacion"),
    url (r'^medicionesxequipo/(?P<id>\d+)/(?P<variable_fisica>.+)/$', 'hidro_core.views.medicionesxequipo'),
	url (r'^medicionesxequipo_ajax/(?P<id>\d+)/$', 'hidro_core.views.medicionesxequipo_ajax'),
	url (r'^graficasxequipo/(?P<id>\d+)/$', 'hidro_core.views.graficasxequipo'),
    url (r'^obtener_datos_medidos_equipo/(?P<id>\d+)/$', 'hidro_core.views.obtener_datos_medidos_equipo'),
    url (r'^obtener_umbrales/$', 'hidro_core.views.obtener_umbrales'),
    url (r'^eliminar_equipo/(?P<id>\d+)/$', 'hidro_core.views.eliminar_equipo'),
    url (r'^exportar_excel/(?P<id>\d+)/$', 'hidro_core.views.exportar_excel'),
    url (r'^exportar_pdf/(?P<id>\d+)/$', 'hidro_core.views.exportar_pdf'),
    url (r'^charts/line/$', 'hidro_core.views.linechart'),
)
