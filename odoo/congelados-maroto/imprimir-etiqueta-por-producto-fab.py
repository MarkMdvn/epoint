action = {}

if record:
  num_labels = int(record.product_qty)
  docids_list = [record.id] * num_labels
  
  nombre_tecnico_informe = 'mrp.label_production_view'
  report = env['ir.actions.report'].search([('report_name', '=', nombre_tecnico_informe)], limit=1)
  
  if report:
    result = report.report_action(docids_list)
    result['close_on_report_download'] = True
    action = result
  else:
    raise UserError("No se ha podido encontrar la acción de informe con el nombre técnico: %s" % nombre_tecnico_informe)