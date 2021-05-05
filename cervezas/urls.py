from django.contrib import admin
from django.urls import path, include
from cervezas.catalogos.views import marcas, presentaciones
from cervezas.productos.views import productos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('django.contrib.auth.urls')),
    path('', productos.home, name='home'),
    #======================CATALOGO MARCAS URLS
    path('catalogo/', marcas.marcas_list, name='marcas_list' ),
    path('catalogo/marcas/create', marcas.marcas_create, name='marcas_create'),
    path('catalogo/marcas/edit/<int:pk>', marcas.marcas_edit, name='marcas_edit'),
    path('catalogo/marcas/delete/<int:pk>', marcas.marcas_delete, name='marcas_delete'),
    #======================CATALOGO PRESENTACIONES URLS 
    #path('catalogo/', presentaciones.presentaciones_list, name='presentaciones_list' ),
    path('catalogo/presentaciones/create', presentaciones.presentaciones_create, name='presentaciones_create'),
    path('catalogo/presentaciones/edit/<int:pk>', presentaciones.presentaciones_edit, name='presentaciones_edit'),
    path('catalogo/presentaciones/delete/<int:pk>', presentaciones.presentaciones_delete, name='presentaciones_delete'),
    #======================CATALOGO PRESENTACIONES URLS 
    path('productos/', productos.productos_list, name='productos_list' ),
    path('productos/create', productos.productos_create, name='productos_create'),
    path('productos/edit/<int:pk>', productos.productos_edit, name='productos_edit'),
    path('productos/delete/<int:pk>', productos.productos_delete, name='productos_delete'),
]
