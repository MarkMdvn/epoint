
for quant in records:
  if quant.quantity > 0 and not quant.lot_id:
    

    referencia_producto = quant.product_id.default_code or str(quant.product_id.id)
    lote_nombre_unico = f"INICIAL-{referencia_producto}"

    lot = env['stock.lot'].search([
        ('name', '=', lote_nombre_unico),
        ('product_id', '=', quant.product_id.id),
        ('company_id', '=', quant.company_id.id)
    ], limit=1)

    if not lot:
      lot = env['stock.lot'].create({
          'name': lote_nombre_unico,
          'product_id': quant.product_id.id,
          'company_id': quant.company_id.id,
      })

    current_quantity = quant.quantity

    quant._update_available_quantity(quant.product_id, quant.location_id, -current_quantity, owner_id=quant.owner_id)

    env['stock.quant']._update_available_quantity(quant.product_id, quant.location_id, current_quantity, lot_id=lot, owner_id=quant.owner_id)