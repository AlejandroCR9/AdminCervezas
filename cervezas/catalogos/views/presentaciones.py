from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from ..models import Presentacion, PresentacionForm

@login_required()
def presentacion_save(request, form, template_name):
    """
    Recibe la peticion y obtiene los registros guardados en la tabla 
    relacionada a los modelos Marca y Presentacion para despues
    guardarlos en sus respectivas variables.
    
    Retorna la vista de index.html junto a los resultados obenidos 
    por las consultas.

    """
    data = dict()
    if request.method == 'POST':#Se inicializa la variable donde \
                                #se encontrara la reespuesta.
        #Se verifica el tipo de request que se envio.
        if form.is_valid():     #Verifica que el ModelForm sea valido.
            form.save()         #Guarda la informacion en la base de datos.
            data['form_is_valid'] = True    #Para que el front sepa que \
                                            #todo salio bien.
            data['type'] = False    #Tabla que se actualizara en la vista: True = Marcas
            presentaciones = Presentacion.objects.all()     #Recupera la info actualizada dela bd

            #Guarda el html de la tabla que se mostrara y le adjunta los valores
            #que se le desplegaran     
            data['html_list'] = render_to_string('catalogos/presentaciones/presentaciones_list.html', {
                'presentaciones': presentaciones
            })
        else:
            data['form_is_valid'] = False
    else:
        #Cuando no es una peticion POST se envia el formulario que utilizara el modal
        #junto a su template
        context = {'form': form}
        data['html_form'] = render_to_string(template_name, context, request)
    return JsonResponse(data)

def presentaciones_create(request):
    """
    Recibe como parametros una peticion, un ModelForm y una cadena con
    la ruta del templata, dependiendo del tipo de peticion retorna la
    vista correspondiente.
    """
    if request.method == 'POST':    #Si el request es un POST
        form = PresentacionForm(request.POST)       #Se inicializa un ModelForm con el
                                                    #Ya que se esta tratando de enviar info a la bd
    else:
        form = PresentacionForm()     #Es una peticion nueva para crear
    return presentacion_save(request, form, 'catalogos/presentaciones/presentaciones_create.html')

def presentaciones_edit(request, pk):
    """
    Dependiendo del request enviado se inicializa un nuevo ModelForm
    de las marcas o se le adjunta el request que se esta haciendo para saber
    que tipo de vista mostrar: el formulario que se le esta enviando o la tabla
    """
    #Se busca la insancia a editar
    presentacion = get_object_or_404(Presentacion, pk=pk)   
    if request.method == 'POST':      #Si es un request POST
        #Se inicilaiza el form con el request y la instancia a editar
        form = PresentacionForm(request.POST, instance=presentacion)
    else:
        #Si no solamente con la instancia a editar para que pueda ser mostrada 
        #en el formulario
        form = PresentacionForm(instance=presentacion)

    return presentacion_save(request, form, 'catalogos/presentaciones/presentaciones_edit.html')

@login_required()
def presentaciones_delete(request, pk):
    """
    Dependiendo del request enviado se inicializa un nuevo ModelForm
    de las marcas o se le adjunta el request que se esta haciendo para saber
    que tipo de vista mostrar: el formulario que se le esta enviando o la tabla
    """
    #Se busca la instancia a borrar
    presentacion = get_object_or_404(Presentacion, pk=pk)
    data = dict()                        #Se inicializa la variable que almacena la respuesta
    if request.method == 'POST':         #Verifica que tipo de request se hace
        presentacion.delete()            #Si es un post con el ID se elimina la instancia 
        data['form_is_valid'] = True     #Verificador para el post que todo fue bien
        data['type'] = False             #Tabla que se actualizara en la vista: True = marcas
        presentaciones = Presentacion.objects.all()#Se recuperan las instancias restantes en la bd

        #Guarda el html de la tabla que se mostrara y le adjunta los valores
        #que se le desplegaran 
        data['html_list'] = render_to_string('catalogos/presentaciones/presentaciones_list.html', {
            'presentaciones': presentaciones
        })
    else:
        #Si el request no es un POST se envia la info que se mostrara en el modal
        data['html_form'] = render_to_string('catalogos/presentaciones/presentaciones_delete.html', {
            'presentacion': presentacion
        }, request)
    return JsonResponse(data)