import pandas as pd
import numpy as np

RAIZ = 'C:/Dev/test/Trabajo-final-analisis-de-datos'
ruta_datos_procesados = '/Business/'

inventario = pd.read_csv('./carpetaAux/InventariosIniciales.csv', usecols=['Referencia','Cantidades','CostoUnit' ])
almacen = pd.read_csv('./carpetaAux/MvtoAlmacénV2.csv', usecols=['Fecha', 'Referencia', 'Descripción', 'Tipo'])
aux = pd.merge(inventario, almacen, on='Referencia', how='left')
tabla = aux.reindex(columns=['Fecha', 'Referencia', 'Descripción', 'Cantidades', 'CostoUnit', 'Tipo'])

# se diferencias materias primas de productos terminados
materias_primas = tabla[tabla['Referencia'].str.startswith('M')]
print(materias_primas)
print('---------------------------------------')
productos_terminados = tabla[tabla['Referencia'].str.startswith('P')]
print(productos_terminados)
# en este punto se tienen dos posibles kardex, uno para los productos terminados
# y otro para las materias primas

#funcion para calcular el costo de salida de un elemento del kardex 
def calcular_costo_salida(elemento, kardex):
    salidas = kardex[(kardex['tipo'] == 'salida') & (kardex['referencia'] == elemento)]
    entradas = kardex[(kardex['tipo'] == 'entrada') & (kardex['referencia'] == elemento)]
    
    cantidad_total_entradas = entradas['cantidades'].sum()
    costo_total_entradas = (entradas['cantidades'] * entradas['costo_unitario']).sum()
    
    cantidad_total_salidas = salidas['cantidades'].sum()
    
    saldo_inventario = cantidad_total_entradas - cantidad_total_salidas
    
    if saldo_inventario == 0:
        return "No hay elementos disponibles"
    
    costo_promedio_ponderado = costo_total_entradas / cantidad_total_entradas
    
    return costo_promedio_ponderado

elemento = 'A'

costo_salida = calcular_costo_salida(elemento, productos_terminados)
print("El costo de salida del elemento", elemento, "es:", costo_salida)
