import pandas as pd
from unidecode import unidecode

RAIZ = 'C:/Dev/test/Trabajo-final-analisis-de-datos'
ruta_datos_procesados = '/Business/'

baseActividad = pd.read_csv('./carpetaAux/BasesDeActividad.csv')
infoEstadistica = pd.read_csv('./carpetaAux/InfoEstadísticaEmpresa.csv')

otros_costos = baseActividad.copy()
# kardex[(kardex['Tipo'] == 'Salida') & (kardex['Referencia'] == elemento)
filtro_operativas = infoEstadistica['Dependencia'].isin(['LAVADO Y DESINFECCION', 'EMPAQUE', 'ALMACEN'])
filtro_areas_operativas = infoEstadistica.loc[filtro_operativas]


filtro_no_operativas = ~infoEstadistica['Dependencia'].isin(['LAVADO Y DESINFECCION', 'ALMACEN', 'EMPAQUE'])
filtro_areas_no_operativas = infoEstadistica.loc[filtro_no_operativas]

filtro_areas_operativas.columns = filtro_areas_operativas.columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

print('antes del proceso')
print(otros_costos)
otros_costos.drop_duplicates() 
otros_costos.reset_index(drop=True)  
duplicados = otros_costos.columns[otros_costos.columns.duplicated()]
print(duplicados)
for valor in otros_costos['Recurso']:

    if valor == 'Depreciacion Proyector' or valor == 'Internet':
        otros_costos['Costos'] = filtro_areas_operativas[otros_costos['BaseDeActividad']].sum() / 104 * filtro_areas_operativas['Personas']
        otros_costos['Gastos'] = filtro_areas_no_operativas[otros_costos['BaseDeActividad']].sum() / 104 * filtro_areas_operativas['Personas']
    else:
        otros_costos['Costos'] = filtro_areas_operativas[otros_costos['BaseDeActividad']].sum()
        otros_costos['Gastos'] = filtro_areas_no_operativas[otros_costos['BaseDeActividad']].sum()

print('este es el resultado final')
print(otros_costos)