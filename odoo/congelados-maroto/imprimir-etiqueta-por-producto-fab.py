action = {}

if record:
    move_lines = record.move_finished_ids.mapped('move_line_ids')
    lots_with_expiration = move_lines.filtered(lambda l: l.lot_id and l.lot_id.use_date)
    num_labels = int(record.product_qty)

    if lots_with_expiration:
        docids_list = []
        for line in lots_with_expiration:
            qty = int(line.qty_done or 1)
            docids_list += [line.lot_id.id] * qty
        report_name = 'stock.label_lot_template_view'
    else:
        docids_list = [record.id] * num_labels
        report_name = 'mrp.label_production_view'

    report = env['ir.actions.report'].search([('report_name', '=', report_name)], limit=1)

    if report:
        result = report.report_action(docids_list)
        result['close_on_report_download'] = True
        action = result
    else:
        raise UserError("No se ha podido encontrar la acción de informe con el nombre técnico: %s" % report_name)
