import pandas as pd

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
    # Filtrar las filas de entrada y salida para el elemento seleccionado
    salidas = kardex[(kardex['Tipo'] == 'Salida') & (kardex['Referencia'] == elemento)]
    entradas = kardex[(kardex['Tipo'] == 'Entrada') & (kardex['Referencia'] == elemento)]

    # Calcular la cantidad total de entradas y el costo total de entradas
    cantidad_total_entradas = entradas['Cantidades'].sum()
    costo_total_entradas = (entradas['Cantidades'] * entradas['CostoUnit']).sum()

    # Calcular la cantidad total de salidas
    cantidad_total_salidas = salidas['Cantidades'].sum()

    # Calcular el saldo de inventario como la diferencia entre la cantidad total de entradas y salidas
    saldo_inventario = cantidad_total_entradas - cantidad_total_salidas
    
    # Verificar si no hay elementos disponibles
    if saldo_inventario == 0:
        return "No hay elementos disponibles"
    
    # Calcular el costo promedio ponderado dividiendo el costo total de entradas por la cantidad total de entradas
    costo_promedio_ponderado = costo_total_entradas / cantidad_total_entradas
    
    # Devolver el costo promedio ponderado
    return costo_promedio_ponderado

# EJEMPLO DE USO
elemento = 'P001'
costo_salida = calcular_costo_salida(elemento, productos_terminados)
print("El costo de salida del elemento", elemento, "es:", costo_salida)


# DIAGRAMA DE FLUJO
# Inicio
#   Obtener Kardex
#   Solicitar elemento
#   Filtrar las filas de salidas para el elemento seleccionado
#       Si no hay filas de salida para el elemento
#           Devolver "No hay elementos disponibles"
#       Calcular la cantidad total de salidas
#   Filtrar las filas de entradas para el elemento seleccionado
#       Calcular la cantidad total de entradas y el costo total de entradas
#   Calcular el saldo de inventario como la diferencia entre la cantidad total de entradas y la cantidad total de salidas
#       Si el saldo de inventario es igual a 0
#           Devolver "No hay elementos disponibles"
#   Calcular el costo promedio ponderado dividiendo el costo total de entradas por la cantidad total de entradas
#   Devolver el costo promedio ponderado
# Fin


# Lemguaje natural
    # -El algoritmo comienza obteniendo el Kardex, que es un DataFrame que contiene la información sobre las transacciones de entrada y salida de elementos.
    
    # -Luego, se solicita al usuario que ingrese el elemento para el cual se desea calcular el costo de salida.
    
    # -A continuación, se filtran las filas del Kardex correspondientes a las salidas del elemento seleccionado.
    
    # -Si no hay filas de salida para el elemento, se devuelve el mensaje "No hay elementos disponibles".
    
    # -Se procede a calcular la cantidad total de salidas sumando todas las cantidades de las filas filtradas.
    
    # -Después, se filtran las filas del Kardex correspondientes a las entradas del elemento seleccionado.
    
    # -Se calcula la cantidad total de entradas sumando todas las cantidades de las filas filtradas, y también se calcula el costo total de entradas multiplicando las cantidades por los costos unitarios y sumando los resultados.
    
    # -A continuación, se calcula el saldo de inventario restando la cantidad total de salidas de la cantidad total de entradas.
    
    # -Si el saldo de inventario es igual a 0, se devuelve el mensaje "No hay elementos disponibles".
    
    # -Se procede a calcular el costo promedio ponderado dividiendo el costo total de entradas por la cantidad total de entradas.
    
    # -Finalmente, se devuelve el costo promedio ponderado como resultado del algoritmo.