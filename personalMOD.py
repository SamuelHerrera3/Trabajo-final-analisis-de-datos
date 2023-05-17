import pandas as pd

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


# salario_Gasto = empleados_salario['Cargo']

# salario_Gasto['CodDependencia'] = empleados_salario['CodDependencia']

PrestamosHoras['Horas'] = PrestamosHoras['Horas'].str.replace(',', '.').astype(float)

nuevo_dataframe = empleados.groupby(['Cargo','CodDependencia'])['Salario Total'].sum().reset_index(name='TotalSalarios')

horasTotal = PrestamosHoras.groupby(['Cargo'])['Horas'].sum().reset_index(name='Horas Prestadas')

nuevo_dataframe = nuevo_dataframe.merge(horasTotal, on='Cargo', how='left')

nuevo_dataframe = nuevo_dataframe.fillna(0)

nuevo_dataframe = nuevo_dataframe.merge(empleados[['Cargo', 'Valor Hora']].drop_duplicates(), on='Cargo', how='left')

nuevo_dataframe['Valor H'] = nuevo_dataframe['Valor Hora'] * nuevo_dataframe['Horas Prestadas']

nuevo_dataframe = nuevo_dataframe.drop(['Valor Hora'], axis=1)

nuevo_dataframe['Salario Gasto'] = PrestamosHoras['DependenciaDestino']

print(nuevo_dataframe)