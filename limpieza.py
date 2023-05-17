#se importan las librerias
import pandas
import re

#se setean las rutas
# RAIZ = 'C:\Users\AlejandroGuerra\Desktop\TabajoManuela\Trabajo-final-analisis-de-datos'
RutaDatosLimpios = '/Cleansed/'
RutaDatosAux = './carpetaAux/'

rutas = { 
    'ActFijos': './Landing/ActFijos.csv',
    'BasesDeActividad': './Landing/BasesDeActividad.csv',
    'BDEmpleados': './Landing/BDEmpleados.csv',
    'InfoEstadísticaEmpresa': './Landing/InfoEstadísticaEmpresa.csv',
    'InventariosIniciales': './Landing/InventariosIniciales.csv',
    'MvtoAlmacénV2': './Landing/MvtoAlmacénV2.csv',
    'OtrosRecursos': './Landing/OtrosRecursos.csv',
    'Precios': './Landing/Precios.csv',
    'PrestamosHoras': './Landing/PrestamosHoras.csv',
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

def convertir_valor(valor):
    if isinstance(valor, float):
        return valor
    try:
        if '.' in valor:
            valor = int(valor.replace('.', ''))
        elif ',' in valor:
            valor = float(valor.replace(',', '.'))
    except ValueError:
        pass
    
    return valor

for nombre, ruta in rutas.items():
    archivoCsv = ruta
    print(archivoCsv)
    tabla = pandas.read_csv(archivoCsv, sep = ";", encoding='latin1')
    #se recore la tabla para eliminar la columna unnamed
    for col in tabla.columns:
        if 'Unnamed' in col:
            tabla = tabla.drop(columns=[col])
    
    #Se limpian los datos usando la funcion eliminar tildes, respetando mayusculas y minusculas
    #Se cambian los espacios vacios por string vacios para mejor manejo
    for col in tabla.select_dtypes(include='object'):
        tabla[col] = tabla[col].apply(lambda x: eliminar_tildes(str(x)).replace('-', ' ') if isinstance(x, str) else x)
        tabla[col] = tabla[col].apply(convertir_valor)
    
    #Se eliminan las filas vacias, se setea cada tipo de dato segun corresponda
    tabla = tabla.dropna()
    tabla = tabla.infer_objects()

    archivoCSV = nombre + '.csv'
    tabla.to_csv(RutaDatosAux + archivoCSV, index=False)
    print(tabla)
    print('-----------------')