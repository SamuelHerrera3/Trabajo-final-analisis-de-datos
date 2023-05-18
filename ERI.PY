import pandas as pd

ingresos = pd.read_csv('./Business/ingresosEmpresa.csv')
depreciacion = pd.read_csv('./Business/depreciacion.csv')



# Crear DataFrame inicial con las columnas "Conceptos" y "2023"
data = {'Conceptos': ['ingresos', 'costos', 'utilidad bruta', 'Gastos Administrativos', 'Depreciaciones', 'Utilidad Operacional', 'Utilidad Antes Impuestos', 'Impuestos', 'Utilidad Neta']}
df = pd.DataFrame(data, columns=['Conceptos', '2023'])

total_suma = ingresos['Total'].sum()
total_depreciacion = depreciacion['Depreciación'].sum()

# Agregar filas con los valores deseados
df.loc[0, '2023'] = total_suma  # Valor para ingresos
df.loc[1, '2023'] = 0  # Valor para costos
df.loc[2, '2023'] = 0  # Valor para utilidad bruta
df.loc[3, '2023'] = 0  # Valor para utilidad bruta
df.loc[4, '2023'] = total_depreciacion  # Valor para utilidad bruta
df.loc[5, '2023'] = total_depreciacion  # Valor para utilidad bruta
df.loc[6, '2023'] = total_depreciacion  # Valor para utilidad bruta
df.loc[7, '2023'] = total_depreciacion  # Valor para utilidad bruta

print(df)