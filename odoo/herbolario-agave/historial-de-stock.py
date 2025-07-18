historial_model = env['x_historial_de_stock']
pedidos_con_stock_negativo = set()

historial_model.search([]).write({'x_studio_pedido_tiene_negativos': False})
historial_model.search([]).unlink()

todas_las_lineas = env['sale.order.line'].search([
    ('order_id.state', 'in', ['draft', 'sent'])
], order='create_date asc')

stock_corriente = {}

for line in todas_las_lineas:
    if not line.product_id:
        continue

    product_en_linea = line.product_id

    kit_bom = env['mrp.bom'].search([
        ('product_tmpl_id', '=', product_en_linea.product_tmpl_id.id),
        ('type', '=', 'phantom')
    ], limit=1)

    if kit_bom:
        for bom_line in kit_bom.bom_line_ids:
            component_template = bom_line.product_id.product_tmpl_id

            if component_template.type != 'consu':
                continue

            cantidad_total_componente = bom_line.product_qty * line.product_uom_qty

            componente_tmpl_id = component_template.id
            if componente_tmpl_id not in stock_corriente:
                stock_antes = component_template.qty_available
            else:
                stock_antes = stock_corriente[componente_tmpl_id]

            stock_despues = stock_antes - cantidad_total_componente
            stock_corriente[componente_tmpl_id] = stock_despues

            if stock_despues < 0:
                pedidos_con_stock_negativo.add(line.order_id.id)

            historial_model.create({
                'x_studio_producto': componente_tmpl_id,
                'x_studio_contacto': line.order_id.partner_id.id,
                'x_studio_pedido_de_venta': line.order_id.id,
                'x_studio_cantidad_movida': cantidad_total_componente,
                'x_studio_stock_antes_del_movimiento': stock_antes,
                'x_studio_stock_despus_del_movimiento': stock_despues,
                'x_name': f"Pedido de {component_template.name} (desde Kit: {kit_bom.product_tmpl_id.name})",
            })
    else:
        product_template = product_en_linea.product_tmpl_id

        if product_template.type != 'consu':
            continue

        product_tmpl_id = product_template.id
        if product_tmpl_id not in stock_corriente:
            stock_antes = product_template.qty_available
        else:
            stock_antes = stock_corriente[product_tmpl_id]

        cantidad_movida = line.product_uom_qty
        stock_despues = stock_antes - cantidad_movida
        stock_corriente[product_tmpl_id] = stock_despues

        if stock_despues < 0:
            pedidos_con_stock_negativo.add(line.order_id.id)

        historial_model.create({
            'x_studio_producto': product_tmpl_id,
            'x_studio_contacto': line.order_id.partner_id.id,
            'x_studio_pedido_de_venta': line.order_id.id,
            'x_studio_cantidad_movida': cantidad_movida,
            'x_studio_stock_antes_del_movimiento': stock_antes,
            'x_studio_stock_despus_del_movimiento': stock_despues,
            'x_name': f"Pedido de {product_template.name}",
        })

if pedidos_con_stock_negativo:
    registros_a_marcar = historial_model.search([
        ('x_studio_pedido_de_venta', 'in', list(pedidos_con_stock_negativo))
    ])
    registros_a_marcar.write({
        'x_studio_pedido_tiene_negativos': True
    })
