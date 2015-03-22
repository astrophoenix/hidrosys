#encoding:utf-8
#from django.forms import ModelForm
# from django import forms
# from hidro_core.models import Equipo
# class EquipoForm(forms.Form):
# 	ACTIVO = 'A'
# 	INACTIVO = 'I'
# 	ESTADO = (
# 				(ACTIVO, "ACTIVO"),
# 				(INACTIVO,"INACTIVO"),
# 			)
# 	nombre = forms.CharField(max_length = 100, widget=forms.TextInput({'class':'text-field form-control', 'style' : 'width:50%;' }))
# 	estado = forms.ChoiceField(choices = ESTADO, widget=forms.Select(attrs = {'class': 'form-control', 'style' : 'width:20%;'}))
# 	def save(self):
# 		equipo = Equipo()
# 		equipo.nombre = self.cleaned_data['nombre']
# 		equipo.estado = self.cleaned_data['estado']
# 		equipo.save()
# 		return equipo
