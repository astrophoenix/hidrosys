#encoding:utf-8
from django.forms import ModelForm
from django import forms
from hidro_core.models import Equipo, UmbralMedidaFisica
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

class UmbralForm(forms.Form):
	id = forms.IntegerField(widget = forms.HiddenInput(), required=False)
	nom_variable_fisica = forms.CharField(max_length = 100, required=False, widget=forms.TextInput({'class':'text-field form-control', 'readonly' : 'readonly'}))
	variable_fisica = forms.CharField(max_length = 100, required=False, widget=forms.TextInput({'class':'text-field form-control', 'readonly' : 'readonly', 'type':'hidden'}))
	umbral_base = forms.DecimalField(max_digits = 11, decimal_places = 2, required=False, widget=forms.TextInput({'class':'text-field form-control text-center'}))
	umbral_verde = forms.DecimalField(max_digits = 11, decimal_places = 2, required=False, widget=forms.TextInput({'class':'text-field form-control text-center'  }))
	umbral_amarillo = forms.DecimalField(max_digits = 11, decimal_places = 2, required=False, widget=forms.TextInput({'class':'text-field form-control text-center'  }))
	umbral_naranja = forms.DecimalField(max_digits = 11, decimal_places = 2, required=False, widget=forms.TextInput({'class':'text-field form-control text-center'  }))
	
	def save(self):
		if self.cleaned_data['id']:
			umbral = UmbralMedidaFisica.objects.get(pk = int(self.cleaned_data['id']))
		else:
			umbral = UmbralMedidaFisica()
		umbral.variable_fisica = self.cleaned_data['variable_fisica']
		umbral.nom_variable_fisica = self.cleaned_data['nom_variable_fisica']
		umbral.umbral_base = self.cleaned_data['umbral_base']
		umbral.umbral_verde = self.cleaned_data['umbral_verde']
		umbral.umbral_amarillo = self.cleaned_data['umbral_amarillo']
		umbral.umbral_naranja = self.cleaned_data['umbral_naranja']
		umbral.save()
		return umbral


class BuscarMedicionesForm(forms.Form):
	
	MESES = (
        ('0', 'Seleccionar'), 
        ('1', 'Enero'), 
        ('2', 'Febrero'), 
        ('3', 'Marzo'),
        ('4', 'Abril'), 
        ('5', 'Mayo'), 
        ('6', 'Junio'),
        ('7', 'Julio'), 
        ('8', 'Agosto'), 
        ('9', 'Septiembre'),
        ('10', 'Octubre'), 
        ('11', 'Noviembre'), 
        ('12', 'Diciembre')
    )

	anio = forms.CharField(max_length = 5, widget=forms.TextInput({'class':'text-field form-control', 'style' : 'width:100%;' }))
	mes = forms.ChoiceField(required = False, choices = MESES,widget=forms.Select(attrs={'class':'form-control'}) )
	fecha_desde = forms.DateField(required = False, input_formats = ('%d/%m/%Y',),widget=forms.widgets.TextInput({'class':'form-control text-center'}))
	fecha_hasta = forms.DateField(required = False, input_formats = ('%d/%m/%Y',),widget=forms.widgets.TextInput({'class':'form-control text-center'}))
