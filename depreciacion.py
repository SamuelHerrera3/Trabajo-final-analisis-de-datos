import pandas as pd

RAIZ = 'C:/Dev/test/Trabajo-final-analisis-de-datos'
ruta_datos_procesados = './Business/'

actFijos = pd.read_csv('./carpetaAux/ActFijos.csv')
tabla_depreciacion = actFijos[['Código', 'Referencia', 'Ubicación', 'Cantidad', 'ValorEnLibrosUnitario', 'VidaÚtil', 'VidaEconómica', 'MétodoDepreciación', 'ValorSalvamento']]

def calcular_depreciacion(row):
    if row['MétodoDepreciación'] == 'Linea recta':
        return row['ValorEnLibrosUnitario'] / row['VidaÚtil'];
    elif row['MétodoDepreciación'] == 'Reduccion de saldos':
        return row['ValorEnLibrosUnitario'] * 1-(row['ValorSalvamento'] / row['ValorEnLibrosUnitario']) ** (1/row['VidaÚtil'])
    elif row['MétodoDepreciación'] == 'No se deprecia':
        return 0
    else:
        return None
    
tabla_depreciacion['Depreciación'] = tabla_depreciacion.apply(calcular_depreciacion, axis=1)
tabla_depreciacion.to_csv(ruta_datos_procesados + 'depreciacion.csv', index=False)