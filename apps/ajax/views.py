import datetime
from django.shortcuts import render

# Create your views here.
import json
import traceback
from django.views.decorators.http import require_http_methods

from apps.productos.models import TipoProducto, Producto
from apps.recepcion.models import RecepcionVehiculo
from sismec.dao import producto_dao, proveedor_dao, recepcion_dao, cliente_dao
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
@require_http_methods(["GET"])
def getTipoProductoAutocomplete(request):
    if request.method == 'GET':
        try:
            data = request.GET
            nombre = data.get('nombre', '')
            filtros = {'nombre': nombre}
            object_list = producto_dao.getTipoProductoAutocomplete(filtros)
            json_response = json.dumps(object_list)
            return HttpResponse(json_response, content_type='application/json')
        except Exception as e:
            traceback.print_exc(e.args)
            return HttpResponseServerError('No se ha podido obtener un resultado')


@require_http_methods(["GET"])
def getTipoProductoById(request):
    if request.method == 'GET':
        try:
            id_producto = request.GET['producto_id']
            print("id ->" + id_producto);
            object_list = TipoProducto.objects.filter(id=id_producto)
            data = serializers.serialize('json', list(object_list))
            return HttpResponse(data, content_type="application/json")
        except Exception as e:
            traceback.print_exc(e.args)
            return HttpResponseServerError('No se ha podido obtener un resultado')


@require_http_methods(["GET"])
def getProveedorAutocomplete(request):
    if request.method == 'GET':
        try:
            data = request.GET
            nombres = data.get('nombres', '')
            filtros = {'nombres': nombres}
            object_list = proveedor_dao.getProveedorAutocomplete(filtros)
            json_response = json.dumps(object_list)
            return HttpResponse(json_response, content_type='application/json')
        except Exception as e:
            traceback.print_exc(e.args)
            return HttpResponseServerError('No se ha podido obtener un resultado')


@require_http_methods(["GET"])
def getProductoAutocomplete(request):
    if request.method == 'GET':
        try:
            data = request.GET
            nombre = data.get('nombre', '')
            filtros = {'nombre': nombre}
            object_list = producto_dao.getProductoAutocomplete(filtros)
            json_response = json.dumps(object_list)
            return HttpResponse(json_response, content_type='application/json')
        except Exception as e:
            traceback.print_exc(e.args)
            return HttpResponseServerError('No se ha podido obtener un resultado')

@require_http_methods(["GET"])
def getMarcaAutocomplete(request):
    if request.method == 'GET':
        try:
            data = request.GET
            descripcion = data.get('descripcion', '')
            filtros = {'descripcion': descripcion}
            object_list = recepcion_dao.getMarcaAutocomplete(filtros)
            json_response = json.dumps(object_list)
            return HttpResponse(json_response, content_type='application/json')
        except Exception as e:
            traceback.print_exc(e.args)
            return HttpResponseServerError('No se ha podido obtener un resultado')

@require_http_methods(["GET"])
def getModeloAutocomplete(request):
    if request.method == 'GET':
        try:
            data = request.GET
            descripcion = data.get('descripcion', '')
            marca = data.get('marca','')
            filtros = {'descripcion': descripcion, 'marca': marca}
            object_list = recepcion_dao.getModeloAutocomplete(filtros)
            json_response = json.dumps(object_list)
            return HttpResponse(json_response, content_type='application/json')
        except Exception as e:
            traceback.print_exc(e.args)
            return HttpResponseServerError('No se ha podido obtener un resultado')


@require_http_methods(["GET"])
def getClienteAutocomplete(request):
    if request.method == 'GET':
        try:
            data = request.GET
            nombres = data.get('nombres', '')
            filtros = {'nombres': nombres}
            object_list = cliente_dao.getClienteAutocomplete(filtros)
            json_response = json.dumps(object_list)
            return HttpResponse(json_response, content_type='application/json')
        except Exception as e:
            traceback.print_exc(e.args)
            return HttpResponseServerError('No se ha podido obtener un resultado')

def default(o):
  if type(o) is datetime.date or type(o) is datetime.datetime:
    return o.isoformat()

@require_http_methods(["GET"])
def getRecepcionAutocomplete(request):
    if request.method == 'GET':
        try:
            data = request.GET
            codigo = data.get('codigo', '')
            filtros = {'codigo': codigo}
            object_list = recepcion_dao.getRecepcionAutocomplete(filtros)
            json_response = json.dumps(object_list, default=default)
            return HttpResponse(json_response, content_type='application/json')
        except Exception as e:
            traceback.print_exc(e.args)
            return HttpResponseServerError('No se ha podido obtener un resultado')

@require_http_methods(["GET"])
def getRecepcionById(request):
    if request.method == 'GET':
        try:
            data = request.GET
            id_recepcion = int(data.get('codigo', ''))
            recepcion= RecepcionVehiculo()
            recepcion = RecepcionVehiculo.objects.filter(id=id_recepcion);
            data = serializers.serialize('json', list(recepcion))
            return HttpResponse(data, content_type="application/json")
        except Exception as e:
            traceback.print_exc(e.args)
            return HttpResponseServerError('No se ha podido obtener un resultado')

@require_http_methods(["GET"])
def getProductoById(request):
    if request.method == 'GET':
        try:
            data = request.GET
            if (data.get('id_producto', '') == ''):
                id_producto = 0
            else:
                id_producto = int(data.get('id_producto', ''))
            producto = Producto.objects.filter(id=id_producto)
            data = serializers.serialize('json', list(producto))
            return HttpResponse(data, content_type="application/json")
        except Exception as e:
            traceback.print_exc(e.args)
            return HttpResponseServerError('No se ha podido obtener un resultado')