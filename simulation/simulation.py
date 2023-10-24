import powercomponents
import cplex
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

total_segundos=24
#lista_tiempo_segundos = list(range(total_segundos))
df = pd.read_excel('C:/Users/karla/OneDrive/Documentos/GitHub/case-simulation/simulation/data.xlsx')
df1 = pd.DataFrame({'Tiempo(segundos)':range(total_segundos)})
df2 = df.drop('Fecha/Hora',axis=1)
df['Fecha/hora'] = df1

#Realizar interpolación lineal para 'glb' y 'carga' en los nuevos
# valores de 'Fecha/hora'

glb_interpolados = np.interp(df['Fecha/hora'], df['glb(W/m2)'])
carga_interpolados = np.interp(df['Fecha/hora'], df['carga(pu)'])

df_interpolados = pd.DataFrame({'Fecha/Hora': df1, 'glb_interpolado': glb_interpolados, 'carga_interpolado':carga_interpolados})
df_interpolados.to_excel('C:/Users/karla/OneDrive/Documentos/GitHub/case-simulation/simulation/data.xlsx',index=False)
