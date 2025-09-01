
field_mapping = {
    'name': 'name',
    'email': 'email',
    'phone': 'phone',
}

extra_fields_for_notes = [
    'x_studio_provincia',
    'x_studio_ciudad',
    'x_studio_cdigo_postal',
]

boolean_field = 'x_studio_contacto_de_evento'


all_attendees = env['event.registration'].search([])

for attendee in all_attendees:
    email = attendee.email
    if not email:
        continue

    if env['res.partner'].search_count([('email', 'ilike', email.strip())]) > 0:
        continue


    vals = {}
    for source_field, dest_field in field_mapping.items():
        if source_field in attendee._fields:
            vals[dest_field] = attendee[source_field]

    if boolean_field in env['res.partner']._fields:
        vals[boolean_field] = True
    
    notes_list = []
    for field_name in extra_fields_for_notes:
        if field_name in attendee._fields:
            value = attendee[field_name]
            if value:
                field_label = attendee.fields_get([field_name])[field_name]['string']
                if hasattr(value, 'display_name'):
                    value = value.display_name
                notes_list.append(f"{field_label}: {value}")
    
    if notes_list:
        header = f"Contacto creado automáticamente desde el evento: {attendee.event_id.name}\n\n--- DATOS ADICIONALES ---\n"
        vals['comment'] = header + "\n".join(notes_list)

    env['res.partner'].create(vals)