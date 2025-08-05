
GROUP_XML_ID = '__custom__123.123'
PRODUCT_REFS = ['ASO', 'CPRO', 'CSIA']


try:
    group_socios = env.ref(GROUP_XML_ID)
except Exception as e:
    raise UserError(f"CRON ERROR: No se pudo encontrar el grupo con XML ID: {GROUP_XML_ID}. Error: {e}")

hoy = datetime.datetime.now()
hace_un_ano = hoy - datetime.timedelta(days=365)

domain = [
    ('state', 'in', ['sale', 'done']),
    ('date_order', '>=', hace_un_ano.strftime('%Y-%m-%d %H:%M:%S')),
    ('order_line.product_id.default_code', 'in', PRODUCT_REFS)
]

active_orders = env['sale.order'].search(domain)

active_user_ids = active_orders.mapped('partner_id.user_ids.id')

group_socios.write({'user_ids': [(6, 0, active_user_ids)]})
