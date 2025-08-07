GROUP_XML_ID = '__custom__123.123'
PRODUCT_REFS = ['ASO', 'CPRO', 'CSIA']

_logger.info("Iniciando cron job: Sincronización de grupo de socios...")

try:
    group_socios = env.ref(GROUP_XML_ID, raise_if_not_found=True)
except ValueError:
    _logger.error(f"CRON ERROR: No se pudo encontrar el grupo con XML ID: {GROUP_XML_ID}.")
    raise UserError(f"CRON ERROR: No se pudo encontrar el grupo con XML ID: {GROUP_XML_ID}.")

hoy = datetime.datetime.now()
hace_un_ano = hoy - datetime.timedelta(days=365)

domain = [
    ('state', 'in', ['sale', 'done']),
    ('date_order', '>=', hace_un_ano.strftime('%Y-%m-%d %H:%M:%S')),
    ('order_line.product_id.default_code', 'in', PRODUCT_REFS)
]

active_orders = env['sale.order'].search(domain)
active_user_ids = active_orders.mapped('partner_id.user_ids.id')

_logger.info(f"Se encontraron {len(active_orders)} pedidos activos correspondientes a {len(active_user_ids)} usuarios únicos.")

try:
    group_socios.write({'user_ids': [(6, 0, active_user_ids)]})
    _logger.info(f"Sincronización completada. El grupo '{group_socios.name}' ahora tiene {len(active_user_ids)} miembros.")
except Exception as e:
    _logger.error(f"CRON ERROR: Fallo al escribir en el grupo '{group_socios.name}'. Error: {e}")
    raise UserError(f"CRON ERROR: Fallo al escribir en el grupo. Error: {e}")
