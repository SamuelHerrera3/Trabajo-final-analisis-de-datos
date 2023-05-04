#se importan las librerias
import pandas
import numpy
import math as mat
import re
import os
import csv

#se setean las rutas
RAIZ = 'C:/Dev/test/DATA'
RutaDatosLimpios = '/Cleansed/'
rutas = {
        'ActFijos': '/Landing/ActFijos.csv',
        'BasesDeActividad': '/Landing/BasesDeActividad.csv',
        'BDEmpleados': '/Landing/BDEmpleados.csv',
        'InfoEstadísticaEmpresa': '/Landing/InfoEstadísticaEmpresa.csv',
        'InventariosIniciales': '/Landing/InventariosIniciales.csv',
        'MvtoAlmacénV2': '/Landing/MvtoAlmacénV2.csv',
        'OtrosRecursos': '/Landing/OtrosRecursos.csv',
        'Precios': '/Landing/Precios.csv',
        'PrestamosHoras': '/Landing/PrestamosHoras.csv',
}

# funcion para limpiar el texto de tildes
def eliminar_tildes(texto):
    texto = re.sub('[á]', 'a', texto)
    texto = re.sub('[é]', 'e', texto)
    texto = re.sub('[í]', 'i', texto)
    texto = re.sub('[ó]', 'o', texto)
    texto = re.sub('[úü]', 'u', texto)
    texto = re.sub('[ñ]', 'n', texto)
    texto = re.sub('[Á]', 'A', texto)
    texto = re.sub('[É]', 'E', texto)
    texto = re.sub('[Í]', 'I', texto)
    texto = re.sub('[Ó]', 'O', texto)
    texto = re.sub('[ÚÜ]', 'U', texto)
    texto = re.sub('[Ñ]', 'N', texto)
    return texto

for nombre, ruta in rutas.items():
    archivoCsv = RAIZ + ruta
    print(archivoCsv)
    tabla = pandas.read_csv(archivoCsv, sep = ";", encoding='latin1')
    #se recore la tabla para eliminar la columna unnamed
    for col in tabla.columns:
        if 'Unnamed' in col:
            tabla = tabla.drop(columns=[col])
    
    #Se limpian los datos usando la funcion eliminar tildes, respetando mayusculas y minusculas
    #Se cambian los espacios vacios por string vacios para mejor manejo
    for col in tabla.select_dtypes(include='object'):
        tabla[col] = tabla[col].apply(
            lambda x: eliminar_tildes(str(x)).replace('-', ' ') if isinstance(x, str) else x)
    
    #Se eliminan las filas vacias, se setea cada tipo de dato segun corresponda
    tabla = tabla.dropna()
    tabla = tabla.convert_dtypes()

    #Se exporta el archivo en formato pkl, ya limpios
    archivoPkl = nombre + '.pkl'
    tabla.to_pickle(RAIZ + RutaDatosLimpios + archivoPkl)
    print(archivoPkl)
    print(tabla)
    print('-----------------')
