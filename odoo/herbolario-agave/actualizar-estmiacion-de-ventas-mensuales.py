env['x_prediccion_mensual_d'].search([]).unlink()

PESOS = [50, 30, 15, 8, 4, 3, 2, 1, 0.5, 0.4, 0.2, 0.1]
FECHA_INICIO_DATOS = datetime.date(2025, 9, 1)

historial_ventas = env['x_estimacion_de_ventas'].search_read(
    [],
    ['x_studio_producto', 'x_studio_mes', 'x_studio_pedidos', 'x_studio_unidades']
)

datos_por_producto = {}
product_names = {}
for venta in historial_ventas:
    product_id = venta['x_studio_producto'][0]
    product_name = venta['x_studio_producto'][1]
    
    if product_id not in datos_por_producto:
        datos_por_producto[product_id] = {}
        product_names[product_id] = product_name
    
    fecha_mes = venta['x_studio_mes'] 
    
    datos_por_producto[product_id][fecha_mes] = {
        'pedidos': venta['x_studio_pedidos'],
        'unidades': venta['x_studio_unidades']
    }


# modificar - TODO
today = datetime.date.today()
meses_a_consultar = []
fecha_actual = today.replace(day=1) 

for _ in range(12):
    meses_a_consultar.append(fecha_actual)
    dia_anterior = fecha_actual - datetime.timedelta(days=1)
    fecha_actual = dia_anterior.replace(day=1)

registros_a_crear = []
for product_id, historial_producto in datos_por_producto.items():
    
    suma_ponderada_pedidos = 0.0
    suma_ponderada_unidades = 0.0
    divisor_dinamico = 0.0
    
    for peso, fecha_mes in zip(PESOS, meses_a_consultar):
        
        if fecha_mes >= FECHA_INICIO_DATOS:
            
            divisor_dinamico += peso
            datos_mes = historial_producto.get(fecha_mes)
            
            if datos_mes:
                pedidos = datos_mes['pedidos']
                unidades = datos_mes['unidades']
            else:
                pedidos = 0
                unidades = 0
            
            suma_ponderada_pedidos += (pedidos * peso)
            suma_ponderada_unidades += (unidades * peso)
            
    resultado_ponderado = (suma_ponderada_pedidos * 0.65) + (suma_ponderada_unidades * 0.35)
    
    if divisor_dinamico > 0:
        estimacion_final = resultado_ponderado / divisor_dinamico
    else:
        estimacion_final = 0.0
    
    product_name = product_names[product_id]
    
    vals = {
        'x_studio_producto': product_id,
        'x_studio_estimacion_mensual': estimacion_final,
        'x_name': product_name,
    }
    registros_a_crear.append(vals)

if registros_a_crear:
    env['x_prediccion_mensual_d'].create(registros_a_crear)

action = {
    "type": "ir.actions.client",
    "tag": "reload",
}
