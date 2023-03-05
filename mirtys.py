import numpy as np
import pandas as pd
import dataframe_image as dfi
import matplotlib.pyplot as plt
#nusiskaitau csv faila
df = pd.read_csv(r"C:\Users\jbuin\Desktop\usa_mirtys\mirtys_statistika.csv")

#1. tiesiog kaip atrodo duomenys; pasiimam pirmus 10
df.head(10)

#2.statistine lentele
df_info = df.describe()
#print(df_info)
#dfi.export(df_info, 'df_info.png')

#3.mirciu priezastys
priezastys = df.loc[:,"cause"]
#print(priezastys)
#dfi.export(priezastys, 'priezastys.jpg')

#4.Kiek vidutiniškai mirė žmonių visu laikotarpiu
df_cause = df.groupby('cause').agg({'val': ['mean']})
df_cause['val']['mean'].sort_values(ascending = False)
#print(df_cause)
#dfi.export(df_cause, 'df_cause.png')
#grafikas
#df_cause.plot()
#plt.savefig('df_cause_gr.png')

#5.mirčių kiekį kiekvienos ligos atveju per visą laikotarpį
df_pivot = df.pivot_table(values='val', index='year', columns='cause', aggfunc='mean',
                      margins=False, dropna=True, fill_value=None) 
#print(df_pivot)
#dfi.export(df_pivot, 'mirciu_sk_per visalaika.png')
#grafikas
df_pivot.plot(kind="bar")
#plt.savefig('mirciu_sk_per visalaika_gr.png')

#6.mirties priezastys pagal lyti: kiek moteru ir kiek vytu pagal visas mirties priezastis, paimam 2019metus, vidutiniskai skaiciuojam
#tam sukursime atskiras df
vyrai_moterys = df[(df['sex'].isin(['Male','Female'])) & (df['year'] == 2019)].pivot_table(values='val', 
                index='cause', columns='sex', aggfunc='mean',
                fill_value=None, margins=False, dropna=True)
#print(vyrai_moterys)
dfi.export(vyrai_moterys, 'vyrai_moterys.png')
#grafikas
vyrai_moterys.plot(kind = 'bar')
plt.ylabel('mirtys per 100 000 žmonių')
plt.title('mirtys pagal lytį')
#plt.savefig('vyrai_moterys_gr.png')

#6.rusiavimas nuo didz iki maziausio
nuo_didz = df.sort_values(['val'], ascending = False)
#print(nuo_didz)

top_didziausi = df.nlargest(10,'val')
#print(top_didziausi)
#grafikai
top_didziausi.plot(x="location", y=[ "val"], kind="bar", figsize=(9, 8))
#plt.savefig('plot_image_did.png')
#plt.show()

#issaugau kaip nuotrauka
#dfi.export(top_didziausi, 'top10.png')

top_maziausi = df.nsmallest(10, 'val')
#dfi.export(top_maziausi, 'top10maz.png')

top_maziausi.plot(x="location", y=[ "val"], kind="bar", figsize=(9, 8))
#plt.savefig('plot_image.png')
#plt.show()

#7.nuo sirdies ligu 2019m
cardio=df[(df["sex"] == "Both") & (df["cause"] == "Cardiovascular diseases") & (df["year"] == 2019)]
cardio_top10=cardio.nlargest(10,'val')
#print(cardio_top10)
#dfi.export(cardio_top10, 'cardio.png')
#grafikas
pie_grafikas=cardio_top10.groupby(['location']).sum().plot(kind='pie',title='mirtys procentais 2019 metais', y='val', autopct='%1.0f%%')
#plt.savefig( 'pie.png')
#plt.show()

#8.sirdies ligos 2000metais
cardio2000 =df[(df["sex"] == "Both") & (df["cause"] == "Cardiovascular diseases") & (df["year"] == 2000)].nlargest(10,'val')
#print(cardio2000)
#dfi.export(cardio2000, 'cardio2000.png')
#grafikas
cardio2000.groupby(['location']).sum().plot(kind='pie',title='mirtys procentais 2000metai', y='val', autopct='%1.0f%%')
#plt.savefig( 'cardio_pie_2000.png')
#plt.show()

#9.visos mirties priezastys - abi lytis, per visa laikotarpi
df_gender = df.groupby(['cause', 'sex']).agg({'val': ['mean']})
#dfi.export(df_gender, 'sirdis_pagal_lyti.png')
#print(df_gender)

#10.mirtys transporto avarijose
transporto_avarijos = df_gender.xs('Transport injuries', level = 'cause')
#dfi.export(transporto_avarijos, 'transporto_avarijos.png')
#print(transporto_avarijos)
#grafikas
bar_plot = transporto_avarijos.plot(kind='bar', title = 'vidutiniškai mirčių transporto avarijose pagal lytį')
bar_plot.legend(loc='upper left')
#bar_plot.grid()
#plt.savefig( 'avarijos_pagal_lyti.png')

#11.kiek zuvo avarijose Lietuvoje
transporto_mirtis_lietuvoje=df[(df['location'].isin([ 'Lithuania'])) & (df['cause'] ==  'Transport injuries')].nlargest(10,'val')
#print(transporto_mirtis_lietuvoje)
dfi.export(transporto_mirtis_lietuvoje, 'transporto_mirtis_lietuvoje.png')
#grafikas
transporto_mirtis_lietuvoje.plot(x="year", y=[ "val"], kind="barh", color = "b", figsize=(9, 8))
#plt.savefig( 'transporto_mirtis_lietuvoje_gr.png')

#12.kiek žmonių mirė nuo klastingos ŽIV ligos
ziv=df[df["cause"].str.contains("HIV")]
top10_ziv=ziv.nlargest(10,'val')
#dfi.export(top10_ziv, 'top10_ziv.png')
#print(top10_ziv)
#grafikas

#13.kiek vidutiniškai žmonių mirė Lietuvoje nuo ŽIV
df_pivot = df.pivot_table(values='val', index=['location','year'], columns='cause', aggfunc='mean',
                      margins=False, dropna=True, fill_value=None)
lt_ziv= df_pivot.loc['Lithuania','HIV/AIDS and sexually transmitted infections']
#dfi.export(lt_ziv, 'lt_ziv.png')
#print(lt_ziv)

#grafikas
df[(df['location'] == 'Lithuania') & (df['cause'] == 'HIV/AIDS and sexually transmitted infections') &
  (df['sex'] == 'Both')].pivot_table(values='val', index='year', columns='sex', aggfunc='mean',
                                          fill_value=None, margins=False, dropna=True).plot(kind = 'line')

plt.ylabel('mirčių per 100 000 ')
plt.title('Mirtys nuo HIV/AIDS  Lietuvoje')
plt.savefig( 'ziv_Lietuvoje.png')
#plt.show()

#14.Pabaltijis;nuo sirdies ligu;nepriklausomai nuo lyties ir per visa laikotarpi
pb_cardio_top15=df[(df['location'].isin([ 'Latvia', 'Lithuania', 'Estonia'])) & (df['cause'] ==  'Cardiovascular diseases')].nlargest(15,'val')
#print(pb_cardio_top15)
#dfi.export(pb_cardio_top15, 'pb_cardio_top15.png')

cardio_pabaltijis=df[(df['location'].isin([ 'Latvia', 'Lithuania', 'Estonia'])) &(df['sex'] == 'Both') & (df['cause'] ==  'Cardiovascular diseases')].nlargest(10,'val')
#print(cardio_pabaltijis)
#dfi.export(cardio_pabaltijis, 'cardio_pabaltijis.png')
cardio_pabaltijis.plot(kind = 'scatter', x = 'location', y = 'val', color = 'red')
#plt.savefig('cardio_pabaltijis_gr.png')

#15.Kiek Baltijos šalyse miršta transporto avarijose.
tr_avarijos_pabaltijis=df[(df['location'].isin([ 'Latvia', 'Lithuania', 'Estonia'])) &(df['sex'] == 'Both') & (df['cause'] ==  'Transport injuries')] .nlargest(15,'val')
#print(tr_avarijos_pabaltijis)
dfi.export(tr_avarijos_pabaltijis, 'tr_avarijos_pabaltijis.png')
#grafikas
tr_avarijos_pabaltijis.plot(kind = 'bar', x = 'location', y = 'val', color = 'red')
#plt.show()
plt.savefig( 'tr_avarijos_pabaltijis_gr.png')

#16.Mirtingumas nuo Živ Baltijos šalyse top15
ziv_pabaltijis=df[(df['location'].isin([ 'Latvia', 'Lithuania', 'Estonia'])) &(df['sex'] == 'Both') & (df['cause'] ==  'HIV/AIDS and sexually transmitted infections')].nlargest(15,'val')
#print(ziv_pabaltijis)
dfi.export(ziv_pabaltijis, 'ziv_pabaltijis.png')
#grafikas
ziv_pabaltijis.plot(kind = 'bar', x = 'location', y = 'val', color = 'c')
#plt.show()
plt.savefig( 'ziv_pabaltijis_gr.png')



#Širdies ir kraujagyslių ligos pagal lyti mire vidutiniskai
df_gender = df.groupby(['cause', 'sex']).agg({'val': ['mean']})
#dfi.export(df_gender, 'sirdis_pagal_lyti.png')
#print(df_gender)


#nuo sirdies ligu pagal metus Lietuvoje
cardio_lt=df_pivot.loc['Lithuania','Cardiovascular diseases']
#dfi.export(cardio_lt, 'cardio_lt.png')
#print(cardio_lt)

#pabaltijis
#pb_cardio_top15=df[(df['location'].isin([ 'Latvia', 'Lithuania', 'Estonia'])) & (df['cause'] ==  'Cardiovascular diseases')].nlargest(15,'val')
#print(pb_cardio_top15)



