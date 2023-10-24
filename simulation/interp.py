import powercomponents
import pandas as pd
import numpy as np

ruta_excel = 'C:/Users/karla/OneDrive/Documentos/GitHub/case-simulation/simulation/data.xlsx'

df = pd.read_excel(ruta_excel)

#Modificar la columna Fecha/hora

total_segundos = 50

tiempo = pd.DataFrame({'Tiempo (seg)':range(total_segundos)})
tiempo1 = tiempo 
df['Fecha/Hora'] = tiempo1
print(df)


#Definir los nuevos valores de Fecha/Hora para la interpolación

Fecha_Hora_nuevos = np.linspace(df['Fecha/Hora'].min(), df['Fecha/Hora'].max(), 24)
print(df)

#Realizar interpolación lineal para 'glb (W/m2)' y Carga (pu)'

glb_interpolados = np.interp(Fecha_Hora_nuevos, df['Fecha/Hora'], df['glb (W/m2)'])
carga_interpolados = np.interp(Fecha_Hora_nuevos, df['Fecha/Hora'], df['Carga (pu)'] )

#Crear un nuevo DataFrame con los resultados de la interpolación

df_interpolados = pd.DataFrame({'Fecha/Hora': Fecha_Hora_nuevos, 'glb_interpolado': glb_interpolados, 'carga_interpolado': carga_interpolados})

# Guardar los resultados en un nuevo archivo Excel

df_interpolados.to_excel('datos_interpolados.xlsx', index=False)

print(df_interpolados.head())


