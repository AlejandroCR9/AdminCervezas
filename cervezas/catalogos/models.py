from django.db import models
from django.forms import ModelForm

# Create your models here.
class Marca(models.Model):
    marca = models.CharField(max_length = 100)
    def __str__(self):
        return self.marca

class MarcaForm(ModelForm):
    class Meta:
        model = Marca
        fields = ['marca']
        labels = {
            'marca': 'Marca:',
        }

class Presentacion (models.Model):
    presentacion = models.CharField(max_length=100)
    def __str__(self):
        return self.presentacion

class PresentacionForm(ModelForm):
    class Meta:
        model = Presentacion
        fields = ['presentacion']
        labels = {
            'presentacion': 'Presentacion:',
        }