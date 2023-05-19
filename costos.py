import pandas as pd
import numpy as np

RAIZ = "C:/Dev/test/Trabajo-final-analisis-de-datos"
ruta_datos_procesados = "./Business/"

# se importan los archivos base
baseActividad = pd.read_csv("./Cleansed/BasesDeActividad.csv")
infoEstadistica = pd.read_csv("./Cleansed/InfoEstadísticaEmpresa.csv")

otros_costos = baseActividad.copy()

# Se filtra por areas operativas
filtro_operativas = infoEstadistica["Dependencia"].isin(["LAVADO Y DESINFECCION", "EMPAQUE", "ALMACEN"])
tabla_areas_operativas = infoEstadistica.loc[filtro_operativas]

# Se filtra por areas no operativas
filtro_no_operativas = ~infoEstadistica["Dependencia"].isin(["LAVADO Y DESINFECCION", "ALMACEN", "EMPAQUE"])
tabla_areas_no_operativas = infoEstadistica.loc[filtro_no_operativas]


# Elimino tildes las columnas de ambos filtros para mejor manejo
tabla_areas_operativas.columns = (
    tabla_areas_operativas.columns.str.normalize("NFKD")
    .str.encode("ascii", errors="ignore")
    .str.decode("utf-8")
)
tabla_areas_no_operativas.columns = (
    tabla_areas_no_operativas.columns.str.normalize("NFKD")
    .str.encode("ascii", errors="ignore")
    .str.decode("utf-8")
)

# Añado la columna costos 
arrCostos = []
for columna, serie in tabla_areas_operativas[otros_costos["BaseDeActividad"]].iteritems():
    serie_float = serie.astype(float)
    suma = serie_float.sum() 
    if columna == 'Personas':
        suma = suma / 104 * suma
    arrCostos.append(suma)
otros_costos["Costos"] = arrCostos

# Añado la columna gastos 
arrGastos = []
for columna, serie in tabla_areas_no_operativas[otros_costos["BaseDeActividad"]].iteritems():
    serie_float = serie.astype(float)
    suma = serie_float.sum()
    if columna == 'Personas':
        suma = suma / 104 * suma
    arrGastos.append(suma)    
otros_costos["Gastos"] = arrGastos

# exporto
otros_costos.to_csv(ruta_datos_procesados + 'otros_costos.csv', index=False)