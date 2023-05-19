import pandas as pd

ruta_datos_procesados = './Business/'
ingresos = pd.read_csv('./Business/ingresosEmpresa.csv')
depreciacion = pd.read_csv('./Business/depreciacion.csv')
kardex = pd.read_csv('./Business/Kardex.csv')
empleados = pd.read_csv('./Business/empleados.csv')
otros_costos = pd.read_csv('./Business/otros_costos.csv')

#Empaque almacenamiento y lavado 

condicion = empleados['CodDependencia'].isin([10101, 10201, 10901])

gastos = empleados[~empleados['CodDependencia'].isin([10101, 10201, 10901])]

gastos =  gastos['Salario Total'].sum()


costos = empleados[condicion]

costos = costos['Salario Total'].sum()


productos_terminados = kardex[kardex['Referencia'].str.startswith('P')]

productos_terminados = productos_terminados['saldo'].astype(float).sum()

otros_costos_operativos = otros_costos['Costos'].sum()
costos = costos + productos_terminados + otros_costos_operativos

# Crear DataFrame inicial con las columnas "Conceptos" y "2023"
data = {'Conceptos': ['ingresos', 'costos', 'utilidad bruta', 'Gastos Administrativos', 'Depreciaciones', 'Utilidad Operacional', 'Utilidad Antes Impuestos', 'Impuestos', 'Utilidad Neta']}
eri = pd.DataFrame(data, columns=['Conceptos', '2023'])

total_suma = ingresos['Total'].sum()
total_depreciacion = depreciacion['Depreciación'].sum()

utilidad_bruta = total_suma - costos
utilidad_operacional = utilidad_bruta - gastos -total_depreciacion

impuestos = utilidad_operacional * 0.35

# Agregar filas con los valores deseados
eri.loc[0, '2023'] = total_suma  # Valor para ingresos
eri.loc[1, '2023'] = costos  # Valor para costos
eri.loc[2, '2023'] = utilidad_bruta # Valor para utilidad bruta
eri.loc[3, '2023'] = gastos  # Valor para utilidad bruta
eri.loc[4, '2023'] = total_depreciacion  # Valor para utilidad bruta
eri.loc[5, '2023'] =  utilidad_operacional # Valor para utilidad bruta
eri.loc[6, '2023'] = utilidad_operacional # Valor para utilidad bruta
eri.loc[7, '2023'] = impuestos # Valor para utilidad bruta
eri.loc[8, '2023'] = utilidad_operacional - impuestos # Valor para utilidad bruta

eri.to_csv( ruta_datos_procesados + 'ERI.csv', index=False)
print(eri)