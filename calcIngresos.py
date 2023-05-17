import pandas as pd

RAIZ = 'C:/Dev/test/Trabajo-final-analisis-de-datos'
ruta_datos_procesados = '/Business/'

# Leemos el archivo csv limpio MvtoAlmacenV2 para trabajar con el
mvtos = pd.read_csv('./carpetaAux/MvtoAlmacénV2.csv')

# Leemos el archivo de precios
precios = pd.read_csv('./carpetaAux/Precios.csv')

# Filtramos por referencias que empiezan con la letra 'P'
filtro_referencia = mvtos[mvtos['Referencia'].str.startswith('P')]

# Filtramos por las salidas
filtro_salidas = filtro_referencia[filtro_referencia['Tipo'] == 'Salida']

# Hacemos un merge de los dos dataframes usando la columna 'Referencia'
merge = pd.merge(filtro_salidas, precios, on='Referencia')

# Creamos una nueva columna con el valor de la multiplicación
merge['Total'] = merge['Cantidades'].astype(int) * merge['PrecioVenta'].astype(int)

merge[['Fecha', 'Referencia', 'Tipo', 'Cantidades', 'PrecioVenta', 'Total']].to_csv(RAIZ + ruta_datos_procesados + 'ingresosEmpresa.csv', index=False)