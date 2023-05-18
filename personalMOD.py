import pandas as pd
import numpy as np

RAIZ = 'C:/Dev/test/Trabajo-final-analisis-de-datos'
ruta_datos_procesados = './Business/'

empleados_salario = pd.read_csv('./carpetaAux/BDEmpleados.csv')

empleados = pd.read_csv('./carpetaAux/BDEmpleados.csv')

PrestamosHoras = pd.read_csv('./carpetaAux/PrestamosHoras.csv')

#Se retiran los puntos del dataFrame
empleados['Salario'] = empleados['Salario'].str.replace('.', '')
#Se convierten los salarios a float para un mejor tratamiento a la hora del calculo
empleados['Salario'] = empleados['Salario'].astype(float)
#Se combierten los datos a tipo numerico 
empleados['Salario'] = pd.to_numeric(empleados['Salario'])

empleados['AuxTPTE'] = empleados['Salario'].apply(lambda x: 140606 if x >= 2319999 else 0)
#Se agrega la columna cesantias 
empleados['Cesantias'] = (empleados['Salario'] + empleados['AuxTPTE']) * 0.0833
#Se agrega la columna Intereses
empleados['Intereses'] = (empleados['Salario'] + empleados['AuxTPTE']) * 0.01
#Se agrega la columna Prima 
empleados['Prima'] = (empleados['Salario'] + empleados['AuxTPTE']) * 0.0833
#Se agrega la columna vacaciones 
empleados['Vacaciones'] = empleados['Salario'] * 0.0417
#Se agrega la columna Salud
empleados['Salud'] = empleados['Salario'] * 0.0850
#Se agrega la columna Pension
empleados['Pension'] = empleados['Salario'] * 0.12
#Se agrega la columns arl
empleados['Arl'] = empleados['Salario'] * 0.00522
#Se agrega la columna ccf
empleados['Ccf'] = empleados['Salario'] * 0.02
#Se agrega la columna Sena
empleados['Sena'] = empleados['Salario'] * 0.02
#Se agrega la columna del Salario total
empleados['Salario Total'] = empleados['Salario'] + empleados['AuxTPTE'] 
+ empleados['Cesantias'] + empleados['Intereses'] +empleados['Prima'] +empleados['Vacaciones']
+empleados['Salud']+empleados['Pension']+empleados['Arl']+empleados['Ccf']+empleados['Sena']


empleados['Valor Hora']= empleados['Salario Total'] /240

empleados.to_csv( ruta_datos_procesados + 'empleados.csv', index=False)

print('-----------------------------')


PrestamosHoras['Horas'] = PrestamosHoras['Horas'].str.replace(',', '').astype(float)

nuevo_dataframe = empleados.groupby(['Cargo','CodDependencia'])['Salario Total'].sum().reset_index(name='TotalSalarios')

horasTotal = PrestamosHoras.groupby(['Cargo'])['Horas'].sum().reset_index(name='Horas Prestadas')

horasTotal['DependenciaDestino'] = PrestamosHoras['DependenciaDestino']

nuevo_dataframe = nuevo_dataframe.merge(horasTotal, on='Cargo', how='left')

nuevo_dataframe = nuevo_dataframe.fillna(0)

nuevo_dataframe = nuevo_dataframe.merge(empleados[['Cargo', 'Valor Hora']].drop_duplicates(), on='Cargo', how='left')

nuevo_dataframe['Valor H'] = nuevo_dataframe['Valor Hora'] * nuevo_dataframe['Horas Prestadas']

nuevo_dataframe = nuevo_dataframe.drop(['Valor Hora'], axis=1)
# SALARIO GASTO: (Coger de la tabla PrestamoHoras la cantidad de horas que van para la 
# DependenciaDestino diferente a la  DependenciaOrigen multiplicado por el 
# valor de la hora  VALOR HORA del respectivo Cargo en BDEmpleado) más 
# (el salario de cada CARGO de Las dependencias que no sea del CodDEPENDENCIA “LAVADO Y DESINFECCIÓN, 
# EMPAQUE Y ALMACÉN”

horas_por_dependencia = PrestamosHoras.groupby('DependenciaDestino')['Horas'].sum()
nuevo_dataframe2 = pd.DataFrame({'DependenciaDestino': horas_por_dependencia.index, 'Horas Sumadas': horas_por_dependencia.values})


diccionario_horas = nuevo_dataframe2.set_index('DependenciaDestino')['Horas Sumadas'].to_dict()

nuevo_dataframe['Salario Gasto'] = nuevo_dataframe['CodDependencia'].map(diccionario_horas)

nuevo_dataframe['Salario Gasto'] =nuevo_dataframe['Salario Gasto'] * nuevo_dataframe['Valor H']

suma_condicional = lambda row: row['Salario Gasto'] + row['TotalSalarios'] if row['CodDependencia'] not in ['10101', '10201', '10901'] else row['Salario Gasto']


nuevo_dataframe['Salario Gasto'] = nuevo_dataframe.apply(suma_condicional, axis=1)


condicion = nuevo_dataframe['CodDependencia'].isin([10101, 10201, 10901])
datos_filtrados = nuevo_dataframe[condicion]

# Calcular la suma de 'TotalSalarios' solo para los datos filtrados
suma_total_salarios = datos_filtrados['TotalSalarios'].sum()

nuevo_dataframe['Salario Costo'] = datos_filtrados['TotalSalarios'] 

condicion = (nuevo_dataframe['Salario Costo'].notna()) & (nuevo_dataframe['Salario Costo'] != 0)

nuevo_dataframe.loc[condicion, 'Salario Costo'] = suma_total_salarios -nuevo_dataframe['Salario Gasto']

nuevo_dataframe = nuevo_dataframe.drop(['DependenciaDestino'], axis=1)

print(nuevo_dataframe)

nuevo_dataframe.to_csv( ruta_datos_procesados + 'SalarioGasto.csv', index=False)
