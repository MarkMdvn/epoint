
if record and record.partner_id:
    partner = record.partner_id

    latest_order = env['sale.order'].search([
        ('partner_id', '=', partner.id)
    ], order='date_order desc, id desc', limit=1)

    if latest_order and latest_order.id == record.id:
        
        message_with_data = None
        for message in record.message_ids:
            if message.body and "Nombre del caballo :" in message.body and "DNI del Propietario :" in message.body:
                message_with_data = message.body
                break

        if message_with_data:
            vals_to_update = {}
            
            field_map = {
                'Fecha de Nacimiento': 'x_studio_fecha_de_nacimiento',
                'Propietario': 'x_studio_propietario',
                'DNI del Propietario': 'x_studio_dni_del_propietario',
                'Nombre del caballo': 'x_studio_nombre_del_caballo',
                'Fecha de nacimiento del caballo': 'x_studio_fecha_de_nacimiento_del_caballo',
                'UELN': 'x_studio_ueln',
                'Microchip': 'x_studio_microchip',
                'Localidad': 'x_studio_localidad',
                'Provincia': 'x_studio_provincia'
            }

            text_with_newlines = message_with_data.replace('<br>', '\n').replace('</p>', '\n').replace('</div>', '\n')
            
            plain_text = ""
            in_tag = False
            for char in text_with_newlines:
                if char == '<':
                    in_tag = True
                elif char == '>':
                    in_tag = False
                elif not in_tag:
                    plain_text += char
            
            plain_text = plain_text.replace('&nbsp;', ' ').strip()
            
            lines = plain_text.split('\n')
            for line in lines:
                key_part, separator, value_part = line.partition(':')
                if separator:
                    key_part = key_part.strip()
                    
                    if key_part in field_map:
                        field_name = field_map[key_part]
                        value = value_part.strip()
                        
                        if value:
                            if 'fecha' in field_name:
                                date_parts = value.split('/')
                                if len(date_parts) == 3:
                                    vals_to_update[field_name] = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
                            else:
                                vals_to_update[field_name] = value

            attachment = env['ir.attachment'].search([
                ('res_model', '=', 'sale.order'),
                ('res_id', '=', record.id),
                ('mimetype', 'ilike', 'image/%')
            ], order='create_date desc', limit=1)

            if attachment:
                vals_to_update['x_studio_foto_de_la_documentacin_del_caballo'] = attachment.datas

            if vals_to_update:
                try:
                    partner.write(vals_to_update)
                    record.message_post(body="Los datos personalizados y la foto de la documentación del cliente han sido actualizados desde esta orden de venta.")
                except Exception as e:
                    pass