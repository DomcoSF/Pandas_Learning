# -*- coding: utf-8 -*-
"""Relatorio.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1F1eGp8t_5NHnjG6Kv9GUrs0os8U1ctG6
"""

#!pip install xlwt
#!pip install openpyxl

#import openpyxl

from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.pyplot import figure
from scipy.interpolate import make_interp_spline
import matplotlib as mpl
import matplotlib.dates as dates
import pandas as pd
import numpy as np


#!pip install pmdarima
#from pmdarima import auto_arima
#from statsmodels.tsa.arima.model import ARIMA

df = pd.read_csv('/content/drive/MyDrive/Produtividade macro outubro 2023.csv',sep = ";",header = 2,parse_dates=True,encoding='windows-1252')
df

df = df.drop('Cognome e nome paziente',axis=1)
df = df.drop('Numero cartella clinica',axis=1)
df = df.drop('Numero blocc. totali',axis=1)
#df = df.drop('Operatore',axis=1)
#df = df.drop('ID esame',axis=1)
df

df = df.rename(columns={"ID esame":"IdExame","Data chiusura macro":"Data","Operatore":"Funcionario","Numero blocc. chiusura":"NBlocos"})
df

#df2 = df[(df['Data'] >= "01/07/2023") & (df['Data'] <= "31/07/2023")]
#df2

#df2['FuncionarioNome'] = df2['Funcionario'].apply(lambda x:x.upper().split(" ")[0].replace("\t",'') )
df['FuncionarioNome'] = df['Funcionario'].apply(lambda x:x.strip().upper().split(" ")[0] )
df

df_order = df.sort_values(by=['FuncionarioNome','Data'], ascending=[False,True])
df_order

df_order['Data'] = pd.to_datetime(df_order['Data'],dayfirst=True)
df_order['Data'] = pd.to_datetime(df_order['Data'].dt.strftime('%d/%m/%Y %X'))

df_order['Data2'] = pd.to_datetime(df_order['Data'], dayfirst=True)
df_order['Data2'] = pd.to_datetime(df_order['Data'].dt.strftime('%d/%m/%Y'))

df_order.info()

#df_order['BlocosTotalDia'] = df_order.groupby(df_order.Data.dt.day)['NBlocos'].sum()
#df_order
#df_order['BlocosTotal'] = df_order.groupby(df_order.Data)['NBlocos'].sum().reset_index()
#df_order.groupby(df_order.Data.dt.day)['NBlocos'].sum()

#df_order['Total'] = df_order.groupby(pd.to_datetime(df_order.Data).dt.date).agg({'NBlocos': 'sum'}).reset_index()

# Grouping dates and counting them

#df_order.groupby(['Funcionario', 'Data2'])['NBlocos'].agg('sum')
df_order['TotalBlocosDia']=df_order.groupby(['FuncionarioNome','Data2']).NBlocos.transform('sum')
df_order['TotalExamesDia']=df_order.groupby(['FuncionarioNome','Data2']).NBlocos.transform('count')
df_order['TotalBlocosMes']=df_order.groupby(['FuncionarioNome']).NBlocos.transform('sum')
df_order['TotalExamesMes']=df_order.groupby(['FuncionarioNome']).NBlocos.transform('count')
df_order

df_order.to_excel('/content/drive/MyDrive/produtividade macro agosto.xlsx', sheet_name='new_sheet_name')

plot_df_exames_dia = df_order.groupby(by=["Data2"]).count()
plot_df_exames_dia = pd.DataFrame(plot_df_exames_dia)
plot_df_exames_dia.TotalExamesDia

plot_df_exames = pd.DataFrame(df_order[['FuncionarioNome','TotalExamesMes']], columns=['FuncionarioNome','TotalExamesMes'])
plot_df_exames = plot_df_exames.groupby(['FuncionarioNome']).max()
plot_df_exames.TotalExamesMes

#dept = df.department.value_counts().reset_index()
# x = df_order['TotalBlocosDia']=df_order.groupby(['Funcionario','Data2']).NBlocos.transform('sum')
plot_df = df_order.groupby(by=["FuncionarioNome"]).sum()
plot_df = pd.DataFrame(plot_df)
plot_df.NBlocos

#dept = df.department.value_counts().reset_index()
# x = df_order['TotalBlocosDia']=df_order.groupby(['Funcionario','Data2']).NBlocos.transform('sum')
plot_df_date = df_order.groupby(by=["Data2"]).sum()
plot_df_date = pd.DataFrame(plot_df_date)
plot_df_date.NBlocos

fig, ax = plt.subplots(figsize=(8, 10))

#plt.plot(plot_df.index,plot_df.NBlocos)
ax.bar(plot_df.index, plot_df.NBlocos,align='center',color=mcolors.TABLEAU_COLORS)
# Setting the label spacing by using labelpad parameter
plt.xlabel('Funcionario', labelpad=10)
plt.ylabel('Blocos', labelpad=10)
plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
plt.title("Produtividade Macroscopia por Mês")
plt.grid(True)
plt.show()
#fig.savefig('/content/drive/MyDrive/PorData.png', dpi=fig.dpi)

date_time = plot_df_date.index
date_time = pd.to_datetime(date_time)
data = plot_df_date.NBlocos


min_date = mpl.dates.date2num(date_time.min())
max_date = mpl.dates.date2num(date_time.max())
x_new = np.linspace(min_date, max_date, 1000)

#print(f'min_date: {data.index.min()} -> {min_date}')
#print(f'max_date: {data.index.max()} -> {max_date}')

a_BSpline = make_interp_spline(data.index.map(mpl.dates.date2num), data.values)
y_new = a_BSpline(x_new)

# Get values for the trend line analysis
x_dates = date_time
x_num = dates.date2num(x_dates)

# Calculate a fit line
trend = np.polyfit(x_num, data, 1)
fit = np.poly1d(trend)

DF = pd.DataFrame()
DF['value'] = data
DF = DF.set_index(date_time)
plt.subplots(figsize=(10, 5))
plt.title("Produtividade Macro por Mês")
plt.xlabel("Dias")
plt.ylabel("Blocos")
# Adicionar Media e Mediana
plt.axhline(np.mean(data), linestyle='dashed', color='g',label="Média")
plt.axhline(np.median(data), linestyle='dashed', color='r',label="Mediana")

x_fit = np.linspace(x_num.min(), x_num.max())
plt.plot(dates.num2date(x_fit), fit(x_fit), "b", label="Tendência")

plt.plot(DF,label="Produção")

plt.gcf().autofmt_xdate()
plt.legend()
plt.show()
#fig.savefig('/content/drive/MyDrive/ProdutividadeDiaria.png', dpi=fig.dpi)

fig, ax = plt.subplots(figsize=(8, 10))

#plt.plot(plot_df.index,plot_df.NBlocos)
ax.bar(plot_df_exames.index , plot_df_exames.TotalExamesMes,align='center',color=mcolors.TABLEAU_COLORS)
# Setting the label spacing by using labelpad parameter
plt.xlabel('Funcionario', labelpad=10)
plt.ylabel('Exames', labelpad=10)
plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
plt.title("Produtividade Macroscopia Exames por Mês")
plt.grid(True)
plt.show()
#fig.savefig('/content/drive/MyDrive/PorData.png', dpi=fig.dpi)

date_time = plot_df_exames_dia.index
date_time = pd.to_datetime(date_time)
data = plot_df_exames_dia.TotalExamesDia

min_date = mpl.dates.date2num(date_time.min())
max_date = mpl.dates.date2num(date_time.max())
x_new = np.linspace(min_date, max_date, 1000)

print(f'min_date: {data.index.min()} -> {min_date}')
print(f'max_date: {data.index.max()} -> {max_date}')

a_BSpline = make_interp_spline(data.index.map(mpl.dates.date2num), data.values)
y_new = a_BSpline(x_new)

# Get values for the trend line analysis
x_dates = date_time
x_num = dates.date2num(x_dates)

# Calculate a fit line
trend = np.polyfit(x_num, data, 1)
fit = np.poly1d(trend)


DF = pd.DataFrame()
DF['value'] = data
DF = DF.set_index(date_time)
plt.subplots(figsize=(10, 5))
plt.title("Produtividade Macroscopia Exames Diario")
plt.xlabel("Dias")
plt.ylabel("Exames")
# Adicionar Media e Mediana
plt.axhline(np.mean(data), linestyle='dashed', color='g',label="Média")
plt.axhline(np.median(data), linestyle='dashed', color='r',label="Mediana")

x_fit = np.linspace(x_num.min(), x_num.max())
plt.plot(dates.num2date(x_fit), fit(x_fit), "b", label="Tendência")

plt.plot(DF,label="Produção")
plt.gcf().autofmt_xdate()

plt.legend()
plt.show()
#fig.savefig('/content/drive/MyDrive/ProdutividadeDiaria.png', dpi=fig.dpi)

date_time = plot_df_exames_dia.index
date_time = pd.to_datetime(date_time)
data = plot_df_exames_dia.TotalExamesDia

min_date = mpl.dates.date2num(date_time.min())
max_date = mpl.dates.date2num(date_time.max())
x_new = np.linspace(min_date, max_date, 1000)

#print(f'min_date: {data.index.min()} -> {min_date}')
#print(f'max_date: {data.index.max()} -> {max_date}')

a_BSpline = make_interp_spline(data.index.map(mpl.dates.date2num), data.values)
y_new = a_BSpline(x_new)

# Get values for the trend line analysis
x_dates = date_time
x_num = dates.date2num(x_dates)

# Calculate a fit line
trend = np.polyfit(x_num, data, 1)
fit = np.poly1d(trend)


DF = pd.DataFrame()
DF['value'] = data
DF = DF.set_index(date_time)
plt.subplots(figsize=(10, 5))
plt.title("Produtividade Macroscopia Exames Diario")
plt.xlabel("Dias")
plt.ylabel("Exames")
# Adicionar Media e Mediana
plt.axhline(np.mean(data), linestyle='dashed', color='g',label="Média")
plt.axhline(np.median(data), linestyle='dashed', color='r',label="Mediana")

# Not really necessary to convert the values back into dates
#but added as a demonstration in case one wants to plot non-linear curves
x_fit = np.linspace(x_num.min(), x_num.max())
plt.plot(dates.num2date(x_fit), fit(x_fit), "b", label="Tendência")


plt.plot(DF,label="Produção")
plt.gcf().autofmt_xdate()
plt.legend()
plt.show()
#fig.savefig('/content/drive/MyDrive/ProdutividadeDiaria.png', dpi=fig.dpi)

import matplotlib.dates as dates

date_time = plot_df_exames_dia.index
date_time = pd.to_datetime(date_time)
data = plot_df_exames_dia.TotalExamesDia

min_date = mpl.dates.date2num(date_time.min())
max_date = mpl.dates.date2num(date_time.max())
x_new = np.linspace(min_date, max_date, 1000)

print(f'min_date: {data.index.min()} -> {min_date}')
print(f'max_date: {data.index.max()} -> {max_date}')

a_BSpline = make_interp_spline(data.index.map(mpl.dates.date2num), data.values)
y_new = a_BSpline(x_new)

# Get values for the trend line analysis
x_dates = date_time
x_num = dates.date2num(x_dates)

# Calculate a fit line
trend = np.polyfit(x_num, data, 1)
fit = np.poly1d(trend)


DF = pd.DataFrame()
DF['value'] = data
DF = DF.set_index(date_time)
plt.subplots(figsize=(10, 5))
plt.title("Produtividade Macroscopia Exames Diario")
plt.xlabel("Dias")
plt.ylabel("Exames")
# Adicionar Media e Mediana
plt.axhline(np.mean(data), linestyle='dashed', color='g',label="Média")
plt.axhline(np.median(data), linestyle='dashed', color='r',label="Mediana")

# Not really necessary to convert the values back into dates
#but added as a demonstration in case one wants to plot non-linear curves
x_fit = np.linspace(x_num.min(), x_num.max())
plt.plot(dates.num2date(x_fit), fit(x_fit), "b", label="Tendência")


plt.plot(DF,label="Produção")
plt.gcf().autofmt_xdate()
plt.legend()
plt.show()
#fig.savefig('/content/drive/MyDrive/ProdutividadeDiaria.png', dpi=fig.dpi)