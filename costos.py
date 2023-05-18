import pandas as pd
import numpy as np

RAIZ = 'C:/Dev/test/Trabajo-final-analisis-de-datos'
ruta_datos_procesados = '/Business/'

baseActividad = pd.read_csv('./carpetaAux/BasesDeActividad.csv')
infoEstadistica = pd.read_csv('./carpetaAux/InfoEstadísticaEmpresa.csv')

otros_costos = baseActividad.copy()

filtro_operativas = infoEstadistica['Dependencia'].isin(['LAVADO Y DESINFECCION', 'EMPAQUE', 'ALMACEN'])
tabla_areas_operativas = infoEstadistica.loc[filtro_operativas]


filtro_no_operativas = ~infoEstadistica['Dependencia'].isin(['LAVADO Y DESINFECCION', 'ALMACEN', 'EMPAQUE'])
tabla_areas_no_operativas = infoEstadistica.loc[filtro_no_operativas]

tabla_areas_operativas.columns = tabla_areas_operativas.columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
tabla_areas_no_operativas.columns = tabla_areas_no_operativas.columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')


arr = []

for columna, serie in tabla_areas_operativas[otros_costos['BaseDeActividad']].iteritems():
    suma_columna = serie.sum()
    arr.append(suma_columna)
    print("Columna:", columna)
    print("Suma:", suma_columna)
otros_costos['Costos'] = arr

for i in otros_costos['Recurso']:
    print('´´´´´´´´´´´´´´´´´´´´')
    print(i)
    #dependiendo de lo que haya en la columna recurso de la tabla bases de actividad, 
    if i == 'Depreciacion Proyector' or i == 'Internet':
        print('------------------------------')
        print(otros_costos['Costos'])
        print(type(otros_costos['Costos']))
        otros_costos['Costos'] = otros_costos['Costos'] / 104 * tabla_areas_operativas['Personas']
        otros_costos['Costos'] = otros_costos['Costos'] / 104 * tabla_areas_no_operativas['Personas']

print('este es el resultado final')
print(otros_costos)
