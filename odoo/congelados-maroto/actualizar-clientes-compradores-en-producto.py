for order in records:
  partner = order.partner_id
  if partner:
    for line in order.order_line:
      product_template = line.product_template_id
      if product_template:
        product_template.write({
            'x_studio_comprado_por_clientes': [(4, partner.id)]
        })