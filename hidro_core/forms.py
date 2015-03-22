#encoding:utf-8
from django.forms import ModelForm
from django import forms
from hidro_core.models import Equipo
class EquipoForm(forms.Form):
	ACTIVO = 'A'
	INACTIVO = 'I'
	ESTADO = (
				(ACTIVO, "ACTIVO"),
				(INACTIVO,"INACTIVO"),
			)
	id = forms.IntegerField(widget = forms.HiddenInput(), required=False)
	nombre = forms.CharField(max_length = 100, widget=forms.TextInput({'class':'text-field form-control', 'style' : 'width:50%;' }))
	estado = forms.ChoiceField(choices = ESTADO, widget=forms.Select(attrs = {'class': 'form-control', 'style' : 'width:20%;'}))
	
	def save(self, usuario):
		if self.cleaned_data['id']:
			equipo = Equipo.objects.get(pk = int(self.cleaned_data['id']))
		else:
			equipo = Equipo()
		equipo.nombre = self.cleaned_data['nombre']
		equipo.estado = self.cleaned_data['estado']
		equipo.usuario = usuario
		equipo.save()
		return equipo

class BuscarEquipoForm(forms.Form):
	nombre = forms.CharField(max_length = 100, widget=forms.TextInput({'class':'text-field form-control', 'style' : 'width:100%;' }))
