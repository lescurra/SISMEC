import traceback

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views.decorators.http import require_http_methods
from apps.compras.models import OrdenCompraCab, OrdenCompraDet
from django.contrib import messages
from django.urls import reverse
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
# Agregar un factura Compra
from apps.facturas.models import MovimientoCabecera, MovimientoDetalle
from apps.productos.models import Producto
from apps.proveedores.models import Proveedor

@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
def agregarFacturaCompra(request, id):
    t = loader.get_template('facturas/agregar.html')
    cabeceraOc = OrdenCompraCab.objects.get(pk=id)
    cabeceraOc.fecha_pedido = cabeceraOc.fecha_pedido.strftime("%d/%m/%Y")
    detallesOc = OrdenCompraDet.objects.filter(compra_cab__id=cabeceraOc.id)
    if request.method == 'POST':
        # Obtener tipo de movimiento
        tipo_movimiento = request.POST.get('tipo_movimiento', '')
        # Obtener el proveedor
        proveedor_list = request.POST.get('id_prov_client_select', '')
        # Obtener condicion de compra
        condicion_compra = request.POST.get('condicion_compra', '')
        # Obtener timbrado
        timbrado = request.POST.get('timbrado', '')
        # Obtener fecha ini timbrado
        fecha_ini_timbrado = datetime.strptime(request.POST.get('fecha_ini_timbrado', ''), "%Y-%m-%d")
        # Obtener fecha fin timbrado
        fecha_fin_timbrado = datetime.strptime(request.POST.get('fecha_fin_timbrado', ''), "%Y-%m-%d")
        # Obtener fecha emision de la factura
        fecha = datetime.strptime(request.POST.get('fecha', ''), "%Y-%m-%d")
        # Obtener numero factura
        numero_factura = request.POST.get('numero_factura', '')
        #TOTALES
        # precio_uni por cantidad
        sub_exentas = int(request.POST.get('sub_exentas', ''))
        # precio_uni por cantidad
        sub_iva5 = int(request.POST.get('sub_iva5', ''))
        # precio_uni por cantidad
        sub_iva10 = int(request.POST.get('sub_iva10', ''))
        # subtotal_iva5 / 21
        total_iva5 = int(request.POST.get('total_iva5', ''))
        # subtotal_iva10/ 11
        total_iva10 = int(request.POST.get('total_iva10', ''))

        try:
            for proveedor_id in proveedor_list:
                proveedor = Proveedor.objects.get(id=proveedor_id)
            movimiento = MovimientoCabecera()
            movimiento.fecha_emision = fecha
            movimiento.proveedor = proveedor
            movimiento.numero_factura = numero_factura
            movimiento.tipo_movimiento = tipo_movimiento
            movimiento.tipo_factura = condicion_compra
            movimiento.estado = MovimientoCabecera.PENDIENTE
            movimiento.monto_total = sub_exentas + sub_iva10 + sub_iva5
            movimiento.grav10_total = sub_iva10 - total_iva10
            movimiento.grav5_total = sub_iva5 - total_iva5
            movimiento.iva10_total = sub_iva10
            movimiento.iva5_total = sub_iva5
            movimiento.timbrado = timbrado
            movimiento.fecha_inicio = fecha_ini_timbrado
            movimiento.fecha_fin = fecha_fin_timbrado
            movimiento.orden_compra = cabeceraOc
            movimiento.save()
            #agregar detalles de la factura
            lista_detalles = json.loads(request.POST.get('detalle_factura', ''))
            for key in lista_detalles:
                detalle = MovimientoDetalle()
                id_producto = lista_detalles[key]['id_producto']
                producto = Producto.objects.get(id=id_producto)
                cantidad_item = int(lista_detalles[key]['cantidad_item'])
                precio_uni = lista_detalles[key]['precio_uni']
                exentas = lista_detalles[key]['exentas']
                iva_5 = lista_detalles[key]['iva_5']
                iva_10 = lista_detalles[key]['iva_10']
                detalle.compra_cab = id
                detalle.cantidad = cantidad_item
                detalle.producto = producto
                detalle.precio_unitario = precio_uni
                detalle.exentas = exentas
                detalle.iva5 = iva_5
                detalle.iva10 = iva_10
                detalle.movimiento_cab = movimiento
                detalle.save()
                #SE ACTUALIZA EL STOCK DE PRODUCTO
                cantidad_producto = int(producto.cantidad) + int(detalle.cantidad)
                producto.cantidad = cantidad_producto
                producto.save()
            #ACTUALIZAR ESTADO DE OC
            #cabeceraOc.estado= OrdenCompraCab.FACTURADO
            #cabeceraOc.save()
            status = 200
            mensajes = 'Movimiento agregado exitosamente'
            json_response = {'status' : status, 'mensajes' : mensajes}
            return HttpResponse(json.dumps(json_response), content_type='application/json')
        except Exception as e:
            traceback.print_exc(e.args)
            status = 500
            mensajes = 'Ha ocurrido un error'
            json_response = {'status': status, 'mensajes': mensajes}
            return HttpResponse(json.dumps(json_response), content_type='application/json')
    else:
        c = {
            'cabecera_oc': cabeceraOc,
            'detalles_oc': detallesOc
        }
    return HttpResponse(t.render(c, request))