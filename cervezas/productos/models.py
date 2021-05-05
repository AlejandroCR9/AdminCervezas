from django.db import models
from django.forms import ModelForm
from cervezas.catalogos.models import Marca, Presentacion
# Create your models here.
class Productos(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    presentacion = models.ForeignKey(Presentacion, on_delete=models.CASCADE)
    precio = models.FloatField(default = 0.0)
    def __str__(self):
        return str(self.marca) + " " + str(self.presentacion)

class ProductosForm(ModelForm):
    def __init__(self, *args, **kwargs):
            super(ProductosForm, self).__init__(*args, **kwargs)
            self.fields['precio'].widget.attrs['min'] = 1.0
    class Meta:
        model = Productos
        fields = ['marca', 'presentacion', 'precio']
        labels = {
            'marca': 'Marca:',
            'presentacion': 'Presentacion:',
            'precio': 'Precio:',

        }
        help_texts = {
            'marca': 'Seleccione marca de la cerveza.',
            'presentacion': 'Seleccione presentacion de la cerveza:',
            'precio': 'Ingrese el precio:',
        }