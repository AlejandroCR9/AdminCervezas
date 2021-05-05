from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from ..models import Productos, ProductosForm
from cervezas.catalogos.models import Presentacion, Marca

@login_required()
def home(request):
    """
    Devuelve la vista principal que se muestra luego de iniciar sesion
    """
    return render(request,'productos/home.html')

@login_required()
def productos_list(request):
    """
    
    Recibe la peticion y obtiene los registros guardados en la tabla 
    relacionada al modelo Productos para despues guardarlo
     en su respectiva variable.
    
    Retorna la vista de index.html junto a los resultados obenido 
    por la consulta.
    """
    band = "disabled"
    productos = Productos.objects.all()
    if Marca.objects.all() and Presentacion.objects.all():
        band = ""
    return render(request, 'productos/index.html', {
        'productos': productos,
        'canadd': band
        })

@login_required()
def productos_save(request, form, template_name):
    """
    Recibe como parametros una peticion, un ModelForm y una cadena con
    la ruta del templata, dependiendo del tipo de peticion retorna la
    vista correspondiente.
    """
    data = dict()   #Se inicializa la variable donde \
                        #se encontrara la reespuesta.
    #Se verifica el tipo de request que se envio.
    if request.method == 'POST':
        if form.is_valid(): #Verifica que el ModelForm sea valido.
            form.save()      #Guarda la informacion en la base de datos.
            data['form_is_valid'] = True    #Para que el front sepa que \
                                            #todo salio bien.
            productos = Productos.objects.all()   #Recupera la info actualizada dela bd

            #Guarda el html de la tabla que se mostrara y le adjunta los valores
            #que se le desplegaran 
            data['html_list'] = render_to_string('productos/productos_list.html', {
                'productos': productos,
            })
        else:
            data['form_is_valid'] = False
    else:
        #Cuando no es una peticion POST se envia el formulario que utilizara el modal
        #junto a su template
        context = {'form': form}
        data['html_form'] = render_to_string(template_name, context, request)
    return JsonResponse(data)

def productos_create(request):
    """
    Dependiendo del request enviado se inicializa un nuevo ModelForm
    de las marcas o se le adjunta el request que se esta haciendo para saber
    que tipo de vista mostrar: el formulario que se le esta enviando o la tabla
    """
    if request.method == 'POST':    #Si el request es un POST
        form = ProductosForm(request.POST)  #Se inicializa un ModelForm con el
                                        #Ya que se esta tratando de enviar info a la bd
    else:
        form = ProductosForm()      #Es una peticion nueva para crear
    return productos_save(request, form, 'productos/productos_create.html')

def productos_edit(request, pk):
    """
    Dependiendo del request enviado se inicializa un nuevo ModelForm
    de las marcas o se le adjunta el request que se esta haciendo para saber
    que tipo de vista mostrar: el formulario que se le esta enviando o la tabla
    """
    #Se busca la instancia a editar
    producto = get_object_or_404(Productos, pk=pk)  
    if request.method == 'POST':     #Si es un request POST
        #Se inicilaiza el form con el request y la instancia a editar
        form = ProductosForm(request.POST, instance=producto)
    else:
        #Si no solamente con la instancia a editar para que pueda ser mostrada 
        #en el formulario
        form = ProductosForm(instance=producto) 

    return productos_save(request, form, 'productos/productos_edit.html')

@login_required()
def productos_delete(request, pk):
    """
    Dependiendo del request enviado se muestra el modal de confirmacion
    o se actualiza la tabla mostrada en el navegador
    """
    #Se busca la instancia a borrar
    producto = get_object_or_404(Productos, pk=pk)
    data = dict()   #Se inicializa la variable que almacena la respuesta
    if request.method == 'POST':    #Verifica que tipo de request se hace
        producto.delete()           #Si es un post con el ID se elimina la instancia
        data['form_is_valid'] = True     #Verificador para el post que todo fue bien
        productos = Productos.objects.all()  #Se recuperan las instancias restantes en la bd
        #Guarda el html de la tabla que se mostrara y le adjunta los valores
        #que se le desplegaran 
        data['html_list'] = render_to_string('productos/productos_list.html', {
            'productos': productos,
        })
    else:
        #Si el request no es un POST se envia la info que se mostrara en el modal
        data['html_form'] = render_to_string('productos/productos_delete.html', {
            'producto': producto
        }, request)
    return JsonResponse(data)
