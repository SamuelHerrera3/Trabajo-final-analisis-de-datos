import pandas as pd

RAIZ = 'C:/Dev/test/Trabajo-final-analisis-de-datos'
ruta_datos_procesados = '/Business/'

empleados_salario = pd.read_csv('./carpetaAux/BDEmpleados.csv')

empleados = pd.read_csv('./carpetaAux/BDEmpleados.csv')

#Se retiran los puntos del dataFrame
empleados['Salario'] = empleados['Salario'].str.replace('.', '')
#Se convierten los salarios a float para un mejor tratamiento a la hora del calculo
empleados['salario'] = empleados['Salario'].astype(float)
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

empleados.to_csv(RAIZ + ruta_datos_procesados + 'empleados.csv', index=False)

print('-----------------------------')


salario_Gasto = empleados_salario['Cargo']

salario_Gasto['CodDependencia'] =empleados_salario['CodDependencia']