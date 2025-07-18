env['x_analisis_de_stock_wc'].search([]).unlink()

presupuestos = env['sale.order'].search([('state', 'in', ['draft', 'sent'])])

nuevos_registros = []
for presupuesto in presupuestos:
  for line in presupuesto.order_line:
    if not line.product_id:
      continue

    product_template = line.product_id.product_tmpl_id
    

    if product_template.type != 'consu':
        continue

    unidades_pedidas = line.product_uom_qty
    
    quants = env['stock.quant'].search([
        ('product_id', 'in', product_template.product_variant_ids.ids),
        ('location_id.usage', '=', 'internal'),
    ])
    stock_disponible_total = sum(quants.mapped('quantity'))

    stock_en_camino_total = 0.0
    purchase_lines = env['purchase.order.line'].search([
        ('product_id', 'in', product_template.product_variant_ids.ids),
        ('order_id.state', '=', 'purchase')
    ])
    for po_line in purchase_lines:
        cantidad_pendiente = po_line.product_qty - po_line.qty_received
        if cantidad_pendiente > 0:
            stock_en_camino_total += cantidad_pendiente
    
    diferencia = (stock_disponible_total + stock_en_camino_total) - unidades_pedidas
    
    proveedor_id = product_template.seller_ids[0].partner_id.id if product_template.seller_ids else False
    
    nuevos_registros.append({
      'x_studio_producto_plantilla': product_template.id,
      'x_studio_unidades_pedidas': unidades_pedidas,
      'x_studio_stock_disponible': stock_disponible_total,
      'x_studio_stock_en_camino': stock_en_camino_total,
      'x_studio_diferencia': diferencia,
      'x_studio_proveedor': proveedor_id,
      'x_name': product_template.name,
    })

if nuevos_registros:
  env['x_analisis_de_stock_wc'].create(nuevos_registros)

action = {
    "type": "ir.actions.client",
    "tag": "reload",
}