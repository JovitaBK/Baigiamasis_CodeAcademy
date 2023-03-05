import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import sys
import pandas as pd


headers = {"User-Agent":"Mozilla/5.0 (platform; rv:gecko version) Gecko/gecko trail app name/app version Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion appname/appversion"}

#sudeti i viena vieta
#soderma nuskaitymas

prekes_pavadinimai=[]  #susidedu i masyva pavadinimus
prekes_kaina=[]
def nuskaityti(url):
    #prekes_pavadinimai=[]  #susidedu i masyva pavadinimus
    #prekes_kaina=[]
    puslapis=requests.get(url, headers=headers)
    soup=BeautifulSoup(puslapis.text,'html.parser')
    pavadinimas = soup.find('h1',class_= 'product_title entry-title' ).get_text() #pavadinimo nuskaitymas
    kaina = soup.find('span',class_= 'woocommerce-Price-amount amount' ).get_text() #kainos nuskaitymas
    prekes_pavadinimai.append(pavadinimas)
    prekes_kaina.append(kaina)

    print(prekes_pavadinimai)
    print(prekes_kaina)

nuskaityti("https://soderma.lt/preke/guinot-bioxygene-skaistinamasis-serumas-30-ml/")
nuskaityti("https://soderma.lt/preke/guinot-lift-firming-stangrinamoji-skaistinamoji-kauke-4x19ml/")
nuskaityti("https://soderma.lt/preke/guinot-anti-ageing-sun-priesraukslines-idegio-kapsules-30-vnt/")
nuskaityti("https://soderma.lt/preke/comfort-zone-hydramemory-drekinamoji-gaivinamoji-paakiu-zele-15-ml/")
nuskaityti("https://soderma.lt/preke/acglicolic-s-drekinamasis-gelis-50-ml/")


#noriu gauti kaina kaip float, nes negaliu kitaip sujungti dvieju grafiku
#pirma panaikinu simbolius
kaina_be_simboliu=[]
for kaina in prekes_kaina:
    kaina_be_simboliu.append(kaina.replace("€",""))
    
kaina_be_kablelio = [] #bet kaip stringas
for kaina in kaina_be_simboliu:    
    kaina_be_kablelio.append(kaina.replace(",", "."))
#print(kaina_be_kablelio)

#paverciu i floata
kaina_galutine=[]
for kaina in kaina_be_kablelio:
    kaina_galutine.append(float(kaina))
#print(kaina_galutine)

#padarau dictionary
rez=zip(prekes_pavadinimai, kaina_galutine)
rezultatas = dict(rez)
#print(rezultatas)

#grafikas Soderma
#grafikas is stulpeliu

produktas = list(rezultatas.keys())
verte = list(rezultatas.values())
  
fig, ax = plt.subplots(figsize =(8, 4))

ax.barh(prekes_pavadinimai, kaina_galutine)

# Remove axes splines
for s in ['top', 'bottom', 'left', 'right']:
    ax.spines[s].set_visible(False)
 
# Remove x, y Ticks
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')
 
# Add padding between axes and labels
ax.xaxis.set_tick_params(pad = 5)
ax.yaxis.set_tick_params(pad = 10)
 
# Add x, y gridlines
ax.grid(b = True, color ='grey',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2)
 
# Show top values
ax.invert_yaxis()
 
# Add annotation to bars
for i in ax.patches:
    plt.text(i.get_width()+0.2, i.get_y()+0.5,
             str(round((i.get_width()), 2)),
             fontsize = 10, fontweight ='bold',
             color ='grey')
 
# Add Plot Title
ax.set_title('Soderma kainos',
             loc ='left', )
 
# Add Text watermark
fig.text(0.9, 0.15, 'kainu palyginimas', fontsize = 8,
         color ='grey', ha ='right', va ='bottom',
         alpha = 0.7)
 
# Show Plot
#plt.savefig('plot_soderma.png')
#plt.show()

#pie grafikas
explode = (0.1, 0.0, 0.2, 0.3, 0.0)
 
# Creating color parameters
colors = ( "orange", "cyan", "brown",
          "grey", "indigo")
 
# Wedge properties
wp = { 'linewidth' : 1, 'edgecolor' : "green" }
 
# Creating autocpt arguments
def func(pct, allvalues):
    absolute = int(pct / 100.*np.sum(allvalues))
    return "{:.1f}%\n({:d} g)".format(pct, absolute)
 
# Creating plot
fig, ax = plt.subplots(figsize =(10, 7))
wedges, texts, autotexts = ax.pie(kaina_galutine,
                                  autopct = lambda pct: func(pct, kaina_galutine),
                                  explode = explode,
                                  labels = prekes_pavadinimai,
                                  shadow = True,
                                  colors = colors,
                                  startangle = 90,
                                  wedgeprops = wp,
                                  textprops = dict(color ="magenta"))
 
# Adding legend
ax.legend(wedges, prekes_pavadinimai,
          title ="prekes",
          loc ="center left",
          bbox_to_anchor =(1, 0, 0.5, 1))
 
plt.setp(autotexts, size = 8, weight ="bold")
ax.set_title("Soderma kainos")
 
#plt.show()
#plt.savefig('Soderma kainos_pie.png')



#sugihara
prekes_pavadinimai=[]  #susidedu i masyva
prekes_kaina_nesutvarkyta=[]

url1="https://sugihara.lt/e-parduotuve/guinot/guinot-bioxygene-serum-skaistinamasis-veido-serumas-30-ml"
puslapis1=requests.get(url1, headers=headers)
soup1=BeautifulSoup(puslapis1.text,'html.parser')
pavadinimas1 = soup1.find(class_= 'product-info').find("h1").text
kaina1 = soup1.find('div',class_= 'price' ).get_text()
prekes_pavadinimai.append(pavadinimas1)
prekes_kaina_nesutvarkyta.append(kaina1)

url2="https://sugihara.lt/e-parduotuve/guinot/guinot-eclat-lifting-mask-stangrinamoji-skaistinamoji-kauke-4-19-ml"
puslapis2=requests.get(url2, headers=headers)
soup2=BeautifulSoup(puslapis2.text,'html.parser')
pavadinimas2 = soup2.find(class_= 'product-info').find("h1").text
kaina2 = soup2.find('div',class_= 'price').get_text()
prekes_pavadinimai.append(pavadinimas2)
prekes_kaina_nesutvarkyta.append(kaina2)

url3="https://sugihara.lt/e-parduotuve/guinot/guinot-anti-ageing-sun-priesraukslines-idegio-kapsules-30-vnt"
puslapis3=requests.get(url3, headers=headers)
soup3=BeautifulSoup(puslapis3.text,'html.parser')
pavadinimas3 = soup3.find(class_= 'product-info').find("h1").text
kaina3 = soup3.find('div',class_= 'price').get_text()
prekes_pavadinimai.append(pavadinimas3)
prekes_kaina_nesutvarkyta.append(kaina3)

url4="https://sugihara.lt/e-parduotuve/comfort-zone/comfort-zone-hydramemory-drekinamoji-gaivinamoji-paakiu-zele"
puslapis4=requests.get(url4, headers=headers)
soup4=BeautifulSoup(puslapis4.text,'html.parser')
pavadinimas4 = soup4.find(class_= 'product-info').find("h1").text
kaina4 = soup4.find('span',class_= 'new').get_text()
prekes_pavadinimai.append(pavadinimas4)
prekes_kaina_nesutvarkyta.append(kaina4)

url5="https://sugihara.lt/e-parduotuve/sesderma451/sesderma-acglicolic-s-drekinamasis-gelis-50-ml"
puslapis5=requests.get(url5, headers=headers)
soup5=BeautifulSoup(puslapis5.text,'html.parser')
pavadinimas5 = soup5.find('div',class_= 'product-info').find("h1").text
kaina5 = soup5.find('div',class_= 'price').get_text()
prekes_pavadinimai.append(pavadinimas5)
prekes_kaina_nesutvarkyta.append(kaina5)

#kadangi gaunu kaina netvarkinga, turiu pasalinti nereikalingus simbolius

prekes_kaina=[]
kaina_be_tarpu=[]
kaina_integer=[] #sudedu kolkas kaip stringa, bet versiu i integer
for kaina in prekes_kaina_nesutvarkyta:
    prekes_kaina.append(kaina.replace("\n",""))  #pasalinu simbolius

for kaina in prekes_kaina:
    kaina_be_tarpu.append(kaina.strip())  #pasalinu tarpus, gaunu kaina kaip stringa su simboliu

for kaina in kaina_be_tarpu:
    kaina_integer.append(kaina.replace("€","")) #pasalinu simbolius, kaina kaip stringas

kaina_galutine1 =[]
for kaina in kaina_integer:
    kaina_galutine1.append(float(kaina))
#print(kaina_galutine1)

#padarau dictionary
rez2=zip(prekes_pavadinimai, kaina_galutine1)
rezultatas2 = dict(rez2)
#print(rezultatas2)

#grafikas Sugiharos
produktas2 = list(rezultatas2 .keys())
verte2 = list(rezultatas2 .values())
  
fig, ax = plt.subplots(figsize =(8, 4))

ax.barh(prekes_pavadinimai, kaina_galutine1)


# Remove axes splines
for s in ['top', 'bottom', 'left', 'right']:
    ax.spines[s].set_visible(False)
 
# Remove x, y Ticks
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')
 
# Add padding between axes and labels
ax.xaxis.set_tick_params(pad = 5)
ax.yaxis.set_tick_params(pad = 10)
 
# Add x, y gridlines
ax.grid(b = True, color ='grey',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2)
 
# Show top values
ax.invert_yaxis()
 
# Add annotation to bars
for i in ax.patches:
    plt.text(i.get_width()+0.2, i.get_y()+0.5,
             str(round((i.get_width()), 2)),
             fontsize = 10, fontweight ='bold',
             color ='grey')
 
# Add Plot Title
ax.set_title('Sugihara kainos',
             loc ='left', )
 
# Add Text watermark
fig.text(0.9, 0.15, 'kainu palyginimas', fontsize = 8,
         color ='grey', ha ='right', va ='bottom',
         alpha = 0.7)
 #plt.savefig('plot_sugihara.png')
#plt.show()

#pridedu produktu kainas is gamintoju 
prekes_pavadinimai_gamintojas=[]  #susidedu i masyva pavadinimus
prekes_kaina=[] #susidedu i masyva kainas
url1="https://www.guinot.com/en_US/products-for-treatment/face/radiance-skincare/bioxygene-serum"
puslapis1=requests.get(url1, headers=headers)
soup1=BeautifulSoup(puslapis1.text,'html.parser')
pavadinimas1 = soup1.find('h2',class_= 'h4' ).get_text() #pavadinimo nuskaitymas
kaina1 = soup1.find('span',class_= 'ui huge header txt-label-l' ).get_text() #kainos nuskaitymas
prekes_pavadinimai_gamintojas.append(pavadinimas1)
prekes_kaina.append(kaina1)

url2="https://www.guinot.com/en_US/products-for-treatment/face/firming-skincare/eclat-lifting-mask"
puslapis2=requests.get(url2, headers=headers)
soup2=BeautifulSoup(puslapis2.text,"html.parser")
pavadinimas2 = soup2.find('h1' ).get_text()
kaina2 = soup2.find('span',id= 'product-price' ).get_text()
prekes_pavadinimai_gamintojas.append(pavadinimas2)
prekes_kaina.append(kaina2)

#print(prekes_pavadinimai_gamintojas)
#print(prekes_kaina)

url3="https://www.guinot.com/en_US/products-for-treatment/sun/preparation-repair/anti-ageing-sun-capsules"
puslapis3=requests.get(url3, headers=headers)
soup3=BeautifulSoup(puslapis3.text,'html.parser')
pavadinimas3 = soup3.find('h1' ).get_text() #pavadinimo nuskaitymas
kaina3 = soup3.find('span',id= 'product-price' ).get_text() #kainos nuskaitymas
prekes_pavadinimai_gamintojas.append(pavadinimas3)
prekes_kaina.append(kaina3)

#print(prekes_pavadinimai_gamintojas)
#print(prekes_kaina)

url4="https://it.comfortzoneskin.com/products/hydramemory-eye-gel"
puslapis4=requests.get(url4, headers=headers)
soup4=BeautifulSoup(puslapis4.text,'html.parser')
pavadinimas4 = soup4.find('span',class_= 'name' ).get_text() #pavadinimo nuskaitymas
kaina4 = soup4.find('span',class_= 'current_price' ).get_text() #kainos nuskaitymas
prekes_pavadinimai_gamintojas.append(pavadinimas4)
prekes_kaina.append(kaina4)

#print(prekes_pavadinimai_gamintojas)
#print(prekes_kaina)

url5="https://www.sesderma.com/at_en/acglicolic-s-gel-40000009.html"
puslapis5=requests.get(url5, headers=headers)
soup5=BeautifulSoup(puslapis5.text,'html.parser')
pavadinimas5 = soup5.find('h1',itemprop= 'name' ).get_text() #pavadinimo nuskaitymas
kaina5 = soup5.find('span',class_= 'value' ).get_text() #kainos nuskaitymas
prekes_pavadinimai_gamintojas.append(pavadinimas5)
prekes_kaina.append(kaina5)

#print(prekes_pavadinimai_gamintojas)
#print(prekes_kaina)

kaina_be_kablelio = [] #bet kaip stringas
for kaina in prekes_kaina:    
    kaina_be_kablelio.append(kaina.replace(",", "."))
#print(kaina_be_kablelio)

kaina_be_n=[]
for kaina in kaina_be_kablelio:
    kaina_be_n.append(kaina.replace("\n",""))
#print(kaina_be_n)


kaina_be_simboliu=[]
for kaina in kaina_be_n:
    kaina_be_simboliu.append(kaina.replace("€",""))

#print(kaina_be_simboliu)

kaina_be_tarpu=[]
for kaina in kaina_be_simboliu:
    kaina_be_tarpu.append(kaina.strip())

#print(kaina_be_tarpu)

#paverciu kaina i floata
kaina_galutine_gamintojo=[]
for kaina in kaina_be_tarpu:
    kaina_galutine_gamintojo.append(float(kaina))
#print(kaina_galutine_gamintojo)

#padarau dictionary
rez_gamintojas=zip(prekes_pavadinimai_gamintojas, kaina_galutine_gamintojo)
rezultatas_gamintojas = dict(rez_gamintojas)
print(rezultatas_gamintojas)

#grafikas gamintoju
#grafikas is stulpeliu
produktas_gamintojas = list(rezultatas_gamintojas.keys())
verte_gamintojas = list(rezultatas_gamintojas.values())
  
fig, ax = plt.subplots(figsize =(8, 4))

ax.barh(prekes_pavadinimai_gamintojas, kaina_galutine_gamintojo)

# Remove axes splines
for s in ['top', 'bottom', 'left', 'right']:
    ax.spines[s].set_visible(False)
 
# Remove x, y Ticks
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')
 
# Add padding between axes and labels
ax.xaxis.set_tick_params(pad = 5)
ax.yaxis.set_tick_params(pad = 10)
 
# Add x, y gridlines
ax.grid(b = True, color ='grey',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2)
 
# Show top values
ax.invert_yaxis()
 
# Add annotation to bars
for i in ax.patches:
    plt.text(i.get_width()+0.2, i.get_y()+0.5,
             str(round((i.get_width()), 2)),
             fontsize = 10, fontweight ='bold',
             color ='grey')
 
# Add Plot Title
ax.set_title('Gamintojo kainos',
             loc ='left', )
 
# Add Text watermark
fig.text(0.9, 0.15, 'Gamintojo kainos', fontsize = 8,
         color ='grey', ha ='right', va ='bottom',
         alpha = 0.7)
 
# Show Plot
#plt.savefig('plot_maker.png')
#plt.show()

#bendras grafikas visu triju
barWidth = 0.25
fig = plt.subplots(figsize =(12, 8))
 
# set height of bar
#IT = [12, 30, 1, 8, 22]
#ECE = [28, 6, 16, 5, 10]
#CSE = [29, 3, 24, 25, 17]
 
# Set position of bar on X axis
br1 = np.arange(len(kaina_galutine))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
 
# Make the plot
plt.bar(br1, kaina_galutine, color ='r', width = barWidth,
        edgecolor ='grey', label ='Soderma kaina')
plt.bar(br2, kaina_galutine1, color ='g', width = barWidth,
        edgecolor ='grey', label ='Sugiharos kaina')
plt.bar(br3, kaina_galutine_gamintojo, color ='b', width = barWidth,
        edgecolor ='grey', label ='Gamintojo kaina')
 
# Adding Xticks
plt.xlabel('produktai', fontweight ='bold', fontsize = 10)
plt.ylabel('kaina', fontweight ='bold', fontsize = 10)
plt.xticks([r + barWidth for r in range(len(kaina_galutine))],
        produktas_gamintojas)
 
plt.legend()
#plt.savefig('plot_visi3.png')
#plt.show()



















