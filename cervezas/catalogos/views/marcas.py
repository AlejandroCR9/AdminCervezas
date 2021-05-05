from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from ..models import Marca, MarcaForm, Presentacion


@login_required()
def marcas_list(request):
    """
    Recibe la peticion y obtiene los registros guardados en la tabla 
    relacionada a los modelos Marca y Presentacion para despues
    guardarlos en sus respectivas variables.
    
    Retorna la vista de index.html junto a los resultados obenidos 
    por las consultas.

    """
    marcas = Marca.objects.all()        #Obtiene todas las marcas
    presentaciones = Presentacion.objects.all()     #Obtiene todas las presentaciones
    return render(request, 'catalogos/index.html', {
        'marcas': marcas,
        'presentaciones': presentaciones
        })

@login_required()
def marca_save(request, form, template_name):
    """
    Recibe como parametros una peticion, un ModelForm y una cadena con
    la ruta del templata, dependiendo del tipo de peticion retorna la
    vista correspondiente.
    """
    data = dict()       #Se inicializa la variable donde \
                        #se encontrara la reespuesta.
    #Se verifica el tipo de request que se envio.
    if request.method == 'POST':
        if form.is_valid(): #Verifica que el ModelForm sea valido.
            form.save()     #Guarda la informacion en la base de datos.
            data['form_is_valid'] = True    #Para que el front sepa que \
                                            #todo salio bien.
            data['type'] = True     #Tabla que se actualizara en la vista: True = Marcas
            marcas = Marca.objects.all()    #Recupera la info actualizada dela bd

            #Guarda el html de la tabla que se mostrara y le adjunta los valores
            #que se le desplegaran 
            data['html_list'] = render_to_string('catalogos/marcas/marcas_list.html', {
                'marcas': marcas
            })
        else:
            data['form_is_valid'] = False 
    else:
        #Cuando no es una peticion POST se envia el formulario que utilizara el modal
        #junto a su template
        context = {'form': form}    
        data['html_form'] = render_to_string(template_name, context, request)
    return JsonResponse(data)

def marcas_create(request):
    """
    Dependiendo del request enviado se inicializa un nuevo ModelForm
    de las marcas o se le adjunta el request que se esta haciendo para saber
    que tipo de vista mostrar: el formulario que se le esta enviando o la tabla
    """
    if request.method == 'POST':        #Si el request es un POST
        form = MarcaForm(request.POST)  #Se inicializa un ModelForm con el
                                        #Ya que se esta tratando de enviar info a la bd
    else:
        form = MarcaForm()         #Es una peticion nueva para crear
        
    return marca_save(request, form, 'catalogos/marcas/marcas_create.html')

def marcas_edit(request, pk):
    """
    Dependiendo del request enviado se inicializa un nuevo ModelForm
    de las marcas o se le adjunta el request que se esta haciendo para saber
    que tipo de vista mostrar: el formulario que se le esta enviando o la tabla
    """
    marca = get_object_or_404(Marca, pk=pk)  #Se busca la instancia a editar
    if request.method == 'POST':    #Si es un request POST
        #Se inicilaiza el form con el request y la instancia a editar
        form = MarcaForm(request.POST, instance=marca)  
    else:
        #Si no solamente con la instancia a editar para que pueda ser mostrada 
        #en el formulario
        form = MarcaForm(instance=marca)

    return marca_save(request, form, 'catalogos/marcas/marcas_edit.html')

@login_required()
def marcas_delete(request, pk):
    """
    Dependiendo del request enviado se muestra el modal de confirmacion
    o se actualiza la tabla mostrada en el navegador
    """
    marca = get_object_or_404(Marca, pk=pk) #Se busca la instancia a borrar
    data = dict()   #Se inicializa la variable que almacena la respuesta
    if request.method == 'POST':    #Verifica que tipo de request se hace
        marca.delete()      #Si es un post con el ID se elimina la instancia 
        data['form_is_valid'] = True    #Verificador para el post que todo fue bien
        data['type'] = True     #Tabla que se actualizara en la vista: True = marcas
        marcas = Marca.objects.all()    #Se recuperan las instancias restantes en la bd

        #Guarda el html de la tabla que se mostrara y le adjunta los valores
        #que se le desplegaran 
        data['html_list'] = render_to_string('catalogos/marcas/marcas_list.html', {
            'marcas': marcas
        })
    else:
        #Si el request no es un POST se envia la info que se mostrara en el modal
        data['html_form'] = render_to_string('catalogos/marcas/marcas_delete.html', {
            'marca': marca
        }, request)
    return JsonResponse(data)