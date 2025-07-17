env['x_calculo_de_pedidos_a'].search([]).unlink()

productos_a_procesar = env['product.template'].search([
    ('type', '=', 'consu'),
    ('seller_ids', '!=', False)
])

registros_a_crear = []
for template in productos_a_procesar:
    proveedor_principal = template.seller_ids[0]

    analisis_record = env['x_analisis_de_stock_wc'].search([
        ('x_studio_producto_plantilla', '=', template.id)
    ], limit=1)
    diferencia = analisis_record.x_studio_diferencia if analisis_record else 0

    lista_de_descuentos = template.x_studio_descuento_de_proveedor_2.mapped(
        'x_name')

    # Se unen con " | " en lugar de "+"
    descuento = " | ".join(lista_de_descuentos)

    estimacion_mensual = 0
    unidades_a_pedir = max(0, estimacion_mensual - diferencia)

    vals = {
        'x_studio_producto_plantilla': template.id,
        'x_studio_proveedor': proveedor_principal.partner_id.id,
        'x_studio_cdigo_de_barras': template.barcode,
        'x_studio_diferencia_de_stock': diferencia,
        'x_studio_estimacin_mensual': estimacion_mensual,
        'x_studio_descuento_proveedor': descuento,
        'x_studio_unidades_a_pedir': unidades_a_pedir,
        'x_name': template.name,
    }
    registros_a_crear.append(vals)

if registros_a_crear:
    env['x_calculo_de_pedidos_a'].create(registros_a_crear)

action = {
    "type": "ir.actions.client",
    "tag": "reload",
}
