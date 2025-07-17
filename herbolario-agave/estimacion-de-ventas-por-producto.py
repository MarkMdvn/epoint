env['x_estimacion_de_ventas'].search([]).unlink()

today = datetime.date.today()
doce_meses_atras = today - datetime.timedelta(days=365)

lineas_a_procesar = env['sale.order.line'].search([
    ('create_date', '>=', doce_meses_atras),
    ('product_id.type', '=', 'consu'),
])

datos_agrupados = {}
for line in lineas_a_procesar:
    fecha_mes = line.create_date.date().replace(day=1)
    
    clave = (line.product_id.product_tmpl_id.id, fecha_mes)
    
    if clave not in datos_agrupados:
        datos_agrupados[clave] = {
            'unidades': 0,
            'pedidos': set()
        }
    
    datos_agrupados[clave]['unidades'] += line.product_uom_qty
    datos_agrupados[clave]['pedidos'].add(line.order_id.id)

registros_a_crear = []
for clave, totales in datos_agrupados.items():
    product_tmpl_id = clave[0]
    mes_fecha = clave[1]
    
    vals = {
      'x_studio_producto': product_tmpl_id,
      'x_studio_mes': mes_fecha,
      'x_studio_pedidos': len(totales['pedidos']),
      'x_studio_unidades': totales['unidades'],
      'x_name': f"{env['product.template'].browse(product_tmpl_id).name} - {mes_fecha.strftime('%B %Y').capitalize()}"
    }
    registros_a_crear.append(vals)

if registros_a_crear:
    env['x_estimacion_de_ventas'].create(registros_a_crear)

action = {
    "type": "ir.actions.client",
    "tag": "reload",
}