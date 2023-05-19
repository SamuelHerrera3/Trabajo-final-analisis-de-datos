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


print('tabla_areas_operativas')
print(tabla_areas_operativas)
print('tabla_areas_no_operativas')
print(tabla_areas_no_operativas)
tabla_areas_operativas = tabla_areas_operativas.fillna(0)
tabla_areas_operativas = tabla_areas_operativas.replace('', 0)

tabla_areas_no_operativas = tabla_areas_no_operativas.fillna(0)
tabla_areas_no_operativas = tabla_areas_no_operativas.replace('', 0)

arrCostos = []
for columna, serie in tabla_areas_operativas[otros_costos['BaseDeActividad']].iteritems():
    serie_float = serie.astype(float)
    suma = serie_float.sum() 
    arrCostos.append(suma)
otros_costos['Costos'] = arrCostos


arrGastos = []
for columna, serie in tabla_areas_no_operativas[otros_costos['BaseDeActividad']].iteritems():
    
    print('esta es lña serie')
    print(serie)
    for i in serie:
        print('esta es el i')
        print(i)
        if serie[i] == '':
            i = 0
    print(serie)        
    serie.astype(int)
    suma = serie_float.sum() 
    arrGastos.append(suma)
print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')    
print(arrGastos)    
otros_costos['Gastos'] = arrGastos

# arrGastos = []
# for columna, serie in tabla_areas_no_operativas[otros_costos['BaseDeActividad']].iteritems():
#     print('serie')
#     print(serie)
#     try:
#         serie_clean = pd.to_numeric(serie, errors='coerce')
#         serie_float = serie.astype(float)
#     except ValueError:
#         pass
#     suma = serie_float.sum() 
#     print('suma total')
#     print(suma)
#     print(type(suma))
#     arrGastos.append(suma)

# otros_costos['Gastos'] = arrGastos

for i in otros_costos['Recurso']:
 
    print(i)
    if i == 'Depreciacion Proyector' or i == 'Internet':
        otros_costos['Costos'] = otros_costos['Costos'] / 104 * tabla_areas_operativas['Personas']
        # otros_costos['Gastos'] = otros_costos['Gastos'] / 104 * tabla_areas_no_operativas['Personas']
    # else:
        # otros_costos['Costos'] = otros_costos['Costos']

print('este es el resultado final')
print(otros_costos)
