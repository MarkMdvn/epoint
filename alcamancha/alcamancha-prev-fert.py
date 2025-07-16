# ==================================================================
#  ACCIÓN GLOBAL DEFINITIVA - Previsiones de Fertilizantes (v16 - Final)
# ==================================================================

FERTILIZER_CATEGORY_ID = 6
CAMPO_PERIODO_EN_PEDIDO = 'x_studio_periodo_de_reserva'
CAMPO_DOSIS_EN_PRODUCTO = 'x_studio_dosis_por_hectarea'
CAMPO_NOMBRE_PERIODO = 'x_name'
CAMPO_LINEAS_DE_PREVISION = 'x_studio_lneas_de_previsin'

plantaciones_existentes = env['x_plantacion'].search(
    [('x_contacto', '!=', False)])
contactos_activos = plantaciones_existentes.mapped('x_contacto')


todos_los_periodos = env['x_periodo_de_reserva'].search([])
todos_los_fertilizantes = env['product.product'].search(
    [('categ_id', '=', FERTILIZER_CATEGORY_ID)])

for partner in contactos_activos:
    plantaciones_del_socio = env['x_plantacion'].search(
        [('x_contacto', '=', partner.id)])
    total_ha = sum(
        plantacion.x_studio_hectreas for plantacion in plantaciones_del_socio)

    if total_ha == 0:
        continue

    for periodo in todos_los_periodos:
        nombre_del_periodo = periodo[CAMPO_NOMBRE_PERIODO] or 'Sin Nombre'

        prevision = env['x_prevision_de_fertili'].search([
            ('x_studio_contacto', '=', partner.id),
            ('x_studio_periodo_agrario', '=', periodo.id)
        ], limit=1)

        if not prevision:
            nombre_prevision = "Prevision para %s - %s" % (
                partner.name, nombre_del_periodo)

            prevision = env['x_prevision_de_fertili'].create({
                'x_name': nombre_prevision,
                'x_studio_contacto': partner.id,
                'x_studio_periodo_agrario': periodo.id,
                'x_studio_hectreas_totales': total_ha,
            })
        else:
            prevision.write({'x_studio_hectreas_totales': total_ha})

        prevision[CAMPO_LINEAS_DE_PREVISION].unlink()
        lineas_para_crear = []

        for fert in todos_los_fertilizantes:
            dosis_ha = fert[CAMPO_DOSIS_EN_PRODUCTO]
            if not dosis_ha or dosis_ha == 0.0:
                continue

            domain = [
                ('partner_id', '=', partner.id),
                (CAMPO_PERIODO_EN_PEDIDO, '=', periodo.id),
                ('state', 'in', ['sale', 'done'])
            ]
            pedidos_comprados = env['sale.order'].search(domain)
            lineas_producto = pedidos_comprados.order_line.filtered(
                lambda l: l.product_id.id == fert.id)
            comprado_tn = sum(lineas_producto.mapped('product_uom_qty'))

            necesidad_tn = total_ha * dosis_ha
            vals = {
                'x_name': fert.name,
                'x_studio_fertilizante': fert.product_tmpl_id.id,
                'x_studio_dosis_por_hectrea_toneladas': dosis_ha,
                'x_studio_necesidad_total_tn': necesidad_tn,
                'x_studio_total_comprado_tn': comprado_tn,
                'x_studio_diferencia_tn': necesidad_tn - comprado_tn,
                'x_studio_hectareas_cubiertas': comprado_tn / dosis_ha if dosis_ha > 0 else 0,
            }
            lineas_para_crear.append((0, 0, vals))

        if lineas_para_crear:
            prevision.write({CAMPO_LINEAS_DE_PREVISION: lineas_para_crear})
