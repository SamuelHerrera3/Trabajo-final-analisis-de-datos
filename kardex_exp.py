import pandas as pd

def calcular_kardex_promedio_ponderado(datos_entradas, datos_salidas):

    # Args:
    #     datos_entradas (columna de un df): Lista de diccionarios con datos de las entradas al inventario.
    #         Cada diccionario debe contener las claves 'fecha', 'cantidad' y 'costo_unitario'.
    #     datos_salidas (columna de un df): Lista de diccionarios con datos de las salidas del inventario.
    #         Cada diccionario debe contener las claves 'fecha' y 'cantidad'.

    # Crear DataFrame para almacenar el Kardex
    columnas = ['Fecha', 'Entradas', 'Salidas', 'Existencias', 'Costo Unitario', 'Costo Total', 'Costo Promedio']
    kardex = pd.DataFrame(columns=columnas)
    
    # Calcular el Kardex
    existencias = 0
    costo_total = 0
    
    for entrada in datos_entradas:
        fecha_entrada = entrada['fecha']
        cantidad_entrada = entrada['cantidad']
        costo_unitario_entrada = entrada['costo_unitario']
        
        existencias += cantidad_entrada
        costo_total += cantidad_entrada * costo_unitario_entrada
        costo_promedio = costo_total / existencias
        
        kardex = kardex.append({
            'Fecha': fecha_entrada,
            'Entradas': cantidad_entrada,
            'Salidas': 0,
            'Existencias': existencias,
            'Costo Unitario': costo_unitario_entrada,
            'Costo Total': costo_total,
            'Costo Promedio': costo_promedio
        }, ignore_index=True)
    
    for salida in datos_salidas:
        fecha_salida = salida['fecha']
        cantidad_salida = salida['cantidad']
        
        kardex = kardex.append({
            'Fecha': fecha_salida,
            'Entradas': 0,
            'Salidas': cantidad_salida,
            'Existencias': existencias - cantidad_salida,
            'Costo Unitario': costo_promedio,
            'Costo Total': costo_promedio * (existencias - cantidad_salida),
            'Costo Promedio': costo_promedio
        }, ignore_index=True)
        
        existencias -= cantidad_salida
    
    return kardex
