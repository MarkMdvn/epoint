product_map = {
    11: 'Individual',
    13: 'Profesional',
    12: 'Asociación',
}

all_partners = env['res.partner'].search([])

for partner in all_partners:
    relevant_lines = env['sale.order.line'].search([
        ('order_partner_id', '=', partner.id),
        ('product_id', 'in', list(product_map.keys())),
        ('state', 'in', ['sale', 'done'])
    ])

    if relevant_lines:
        sorted_lines = relevant_lines.sorted(key=lambda line: line.order_id.date_order, reverse=True)
        
        last_relevant_order_line = sorted_lines[0]
        
        product_id = last_relevant_order_line.product_id.id
        partner_type = product_map.get(product_id)
        
        if partner.x_studio_tipo_de_socio != partner_type:
            partner.write({
                'x_studio_tipo_de_socio': partner_type
            })