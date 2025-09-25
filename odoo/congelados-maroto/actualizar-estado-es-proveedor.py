all_supplier_info = env['product.supplierinfo'].search([])
supplier_partner_ids = set(all_supplier_info.mapped('partner_id').ids)

batch_size = 1000
offset = 0

while True:
    partners_batch = env['res.partner'].search([], limit=batch_size, offset=offset)
    
    if not partners_batch:
        break

    partners_to_set_true = env['res.partner']
    partners_to_set_false = env['res.partner']

    for partner in partners_batch:
        is_supplier = partner.id in supplier_partner_ids
        
        if partner.x_studio_es_proveedor != is_supplier:
            if is_supplier:
                partners_to_set_true |= partner
            else:
                partners_to_set_false |= partner

    if partners_to_set_true:
        partners_to_set_true.write({'x_studio_es_proveedor': True})
    if partners_to_set_false:
        partners_to_set_false.write({'x_studio_es_proveedor': False})

    offset += batch_size
