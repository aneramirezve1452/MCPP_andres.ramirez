# -*- coding: utf-8 -*-
# Importamos todas las librerias que vamos a usar

from selenium import webdriver # para manejar el navegador
from selenium.webdriver.common.keys import Keys # para enviar comandos de tecla al navegador
import time # para enviar tiempos de espera al navegador
import urllib
import parser
import re # para regular expressions 
import pandas as pd
#import numpy as np
import requests
from bs4 import BeautifulSoup as bs # para extraer la información de las paginas


# Como primera medida declaramos una version que me va a utilizar el driver de chrome

## NOTA: el driver debe ser compatible con la version del navegador
## NOTA: se debe especificar la ruta donde queda el driver

driver = webdriver.Chrome(executable_path=r"C:\Driver_Chrome\chromedriver.exe")


## definimos una funcion que permitira abrir la pagina deseada en el navegador una vez se 
## proporciona el link
def abrir_pagina(link):
    driver.get(link)
    driver.maximize_window()

## definimos una funcion que solicita la url para le proceso 2015. Una vez se ha situado en la pagina segun corporacion
## departamento y municipio.
## NOTA: Tiene un parametro de "link" ya que a traves de esta funcion se llama la funcion abrir pagina    
def solicitar_url(corp,depto,muni,link):
    
    abrir_pagina(link)
    
    corporacion = driver.find_element_by_id("combo1_chosen")
    corporacion.click()
    buscador = driver.find_element_by_xpath('//div[@id="combo1_chosen"]/div[@class="chosen-drop"]/div[@class="chosen-search"]/input')
    buscador.send_keys(corp)
    buscador.send_keys(Keys.ENTER)

    departamento = driver.find_element_by_id("combo2_chosen")
    departamento.click()
    buscador = driver.find_element_by_xpath('//div[@id="combo2_chosen"]/div[@class="chosen-drop"]/div[@class="chosen-search"]/input')
    buscador.send_keys(depto)
    buscador.send_keys(Keys.ENTER)

    municipio = driver.find_element_by_id("combo3_chosen")
    municipio.click()
    buscador = driver.find_element_by_xpath('//div[@id="combo3_chosen"]/div[@class="chosen-drop"]/div[@class="chosen-search"]/input')
    buscador.send_keys(muni)
    buscador.send_keys(Keys.ENTER)


    url = driver.current_url

#    time.sleep(3)
    return(url)

## definimos una funcion que solicita la url para le proceso 2019. Una vez se ha situado en la pagina segun corporacion
## departamento y municipio.
## NOTA: Tiene un parametro de "link" ya que a traves de esta funcion se llama la funcion abrir pagina    
def solicitar_url_2019(corp,dpto,muni,link,inicio):
    
    
    if corp.lower() == "concejo":
        corpin = "//a[contains(@href,'concejo')]"
    else:
        corpin = "//a[contains(@href,'alcaldia')]"
       
    if inicio == 0:
        abrir_pagina(link)
        global urld
        if corp.lower() == "alcaldia":
            driver.find_element_by_xpath("//div[contains(@class,'input-field col s12 m4')]").click()
            time.sleep(3)
            urld = driver.current_url
            print("puse la url")
            driver.find_element_by_partial_link_text(dpto).click()
           
        else:
            corporacion = driver.find_element_by_xpath("//div[contains(@class,'input-field col s12 m8')]")
            corporacion.click()
            time.sleep(3)
            corporacion = driver.find_element_by_xpath(corpin)
            corporacion.click()
            urld = driver.current_url
            print("puse la url")
            time.sleep(3)
            departamento = driver.find_element_by_partial_link_text(dpto)
            departamento.click()
    else:
        global dptod
        global urldd
        
        if dptod[0] != dptod[1]:
            abrir_pagina(urld)
#            time.sleep(3)
            departamento = driver.find_element_by_partial_link_text(dpto)
            departamento.click()
            urldd = driver.current_url
            dptod[1] = dptod[0]
            
        else:
#            time.sleep(3)
            abrir_pagina(urldd)
            dptod[1] = dptod[0]
            
            
    time.sleep(1)
    
    if muni != "BOGOTA D.C.":
#        time.sleep(1)
        municipio = driver.find_element_by_link_text(muni)
        municipio.click()

    url = driver.current_url
    return(url,urld)

# Se define una funcion que a traves de Beautiful Soup pide la información de partidos, votos absoulos y en porcentaje para el 2015
# NOTA: esta funcion llama a la funcion de solicitar url (las funciones estan anidadas)
def solicitar_datos(corp,depto,muni,link):
    
    page = requests.get(solicitar_url(corp,depto,muni,link))
    data = page.text
    page_soup = bs(data,'html.parser')

    partidos = page_soup.find_all(class_='nomc')
    votos_abs = page_soup.find_all(class_='abs')
    votos_porc = page_soup.find_all(class_='prc')
    
    curules = []
    
    # Hallamos el numero de candidatos/partidos y el % de participación
    if corp.lower() == "concejo":
        Num_partidos_concejo_2015.append(len(partidos))  
        Participacion_concejo_2015.append(page_soup.find_all(class_='porcentajesCajas')[1].text)
    else:
        Num_partidos_alcaldia_2015.append(len(partidos))  
        Participacion_alcaldia_2015.append(page_soup.find_all(class_='porcentajesCajas')[1].text)
      
    
    if corp.lower() == "concejo":
        curules_todo = page_soup.find_all(class_='numcur')
         
        for i in range(len(curules_todo)):
            a = re.findall(r"\d",curules_todo[i].text)
            if a!=[]:
                curules.append(a)
             
                    
    # Limpiamos los datos:
    for i in range(0,len(partidos)):
        
        if corp.lower() == "concejo": 
            Partidos.append(partidos[i].text.strip("\n+"))
            Curules.append(curules[i][0])
          
        else:
            Partidos.append(partidos[i].text.strip("\n+").replace("\n"," - "))
            Curules.append("N/A")
        
        
        Votos_abs.append(votos_abs[i].text)
        Votos_porc.append(votos_porc[i].text)
                      

    return(Partidos,Votos_abs,Votos_porc,Curules)

# Se define una funcion que a traves de Beautiful Soup pide la información de partidos, votos absoulos y en porcentaje para el 2015
# NOTA: esta funcion llama a la funcion de solicitar url (las funciones estan anidadas)
def solicitar_datos_2019(corp,dpto,muni,link,i):
    page = requests.get(solicitar_url_2019(corp,dpto,muni,link,i)[0])
    data = page.text
    page_soup = bs(data,'html.parser')

    #Se hallan los partidos/candidatos:
    partidos_2019 = page_soup.find_all(class_='subtitle')
    
    #se hallan los votos  absolutos y en porcentaje
    a = page_soup.find_all('table')[3].text
    votos_abs_2019 = re.findall("\d.*[\d]\nP",a)
    votos_porc_2019 = re.findall("\d.*%",a)
    
    #Se halla la participacion:
    b = page_soup.find_all('table')[1].find_all('td')
    c = b[len(b)-1].text
   
    if corp.lower() == "concejo":
        Num_partidos_concejo_2019.append(int(len(partidos_2019)/2)) 
        #Se halla la participacion:
        b = page_soup.find_all('table')[1].find_all('td')
        c = b[len(b)-1].text
        c = c.replace(".",",")
        Participacion_concejo_2019.append(c)
    else:
        Num_partidos_alcaldia_2019.append(int(len(partidos_2019)/2))  
        #Se halla la participacion:
        b = page_soup.find_all('table')[1].find_all('td')
        c = b[len(b)-1].text
        c = c.replace(".",",")
        Participacion_alcaldia_2019.append(c)
          
                    
    # Limpiamos los datos:
    for i in range(0,int(len(partidos_2019)/2)):
        
        Partidos_2019.append(" ".join(partidos_2019[i].text.split()))
        Votos_abs_2019.append(votos_abs_2019[i].strip("\nP"))
        Votos_porc_2019.append(votos_porc_2019[i])
                      
    return(Partidos_2019,Votos_abs_2019,Votos_porc_2019)

# Se define una funcion que limpia las listas
def limpiar():
    
    Partidos.clear()
    Votos_abs.clear()
    Votos_porc.clear()
    Curules.clear()
    Partidos_2019.clear()
    Votos_abs_2019.clear()
    Votos_porc_2019.clear()

# Se define una funcion que iguala tamaños de las listas que van a ser usadas para realizar los data frames
def igualar_tamanos(lista1,lista2):
    if len(lista1)>len(lista2):
        for i in range(len(lista1)-len(lista2)):
            lista2.append("N/A")
    else:
        for i in range(len(lista2)-len(lista1)):
            lista1.append("N/A")
            
    
    return(lista1,lista2)

# Se define una función que solicita la información de los procesos 2015 y 2019 para un archivo de entrada DATA
# una corporacion "Corpo" y lo guarda en un archivo "nombredoc" y en otro "docAumento". Esto a traves de los links: "link1" y "link2"
def barrido_info(Data,Corpo,nombreDoc,docAumento,link1,link2):
    DeparAu = []  # Departamentos para hacer data frame de aumento
    MuniAu = [] # Municipios para hacer data frame de aumento
    global dptod
    for i in range(0,len(Data)):
        Depar = Data[i][1]
        dptod[0] = Depar
        DeparAu.append(Data[i][1])
        Muni = Data[i][2]
        MuniAu.append(Data[i][2])
        solicitar_datos(Corpo,Depar,Muni,link1)
        solicitar_datos_2019(Corpo,Depar,Muni,link2,i)
    
        igualar_tamanos(Partidos,Partidos_2019)
        igualar_tamanos(Votos_abs, Votos_abs_2019)
        igualar_tamanos(Votos_porc,Votos_porc_2019)    
        df1 = pd.DataFrame({"Departamento":Depar,"Municipio":Muni,"Corporación":Corpo,"Partido 2015":Partidos,"Votos Absolutos 2015":Votos_abs,"Porcentaje 2015":Votos_porc,"Partido 2019":Partidos_2019,"Votos Absolutos 2019":Votos_abs_2019,"Porcentaje 2019":Votos_porc_2019})
        df1.to_csv(nombreDoc,mode = 'a', encoding = 'latin',index = False,sep=";",header=False)
        limpiar()
    
    if Corpo.lower() == "alcaldia":
    
        for i in range(len(Participacion_alcaldia_2019)):
            a = int("".join(re.findall("[\d.*\d]",Participacion_alcaldia_2015[i])))      
            b = int("".join(re.findall("[\d.*\d]",Participacion_alcaldia_2019[i])))
            c = Num_partidos_alcaldia_2015[i]
            d = Num_partidos_alcaldia_2019[i]
            if b>a:
                Aumento_Alcaldia.append("AUMENTÓ")
            elif b<a:
                Aumento_Alcaldia.append("DISMINUYÓ")
            elif b==a:
                Aumento_Alcaldia.append("SE MANTUVO")
            
            if d>c:
                Aumento_P_Alcaldia.append("AUMENTÓ")
            elif d<c:
                Aumento_P_Alcaldia.append("DISMINUYÓ")
            elif d==c:
                Aumento_P_Alcaldia.append("SE MANTUVO")
    
    else:
            
        for i in range(len(Participacion_concejo_2019)):
            a = int("".join(re.findall("[\d.*\d]",Participacion_concejo_2015[i])))      
            b = int("".join(re.findall("[\d.*\d]",Participacion_concejo_2019[i])))
            c = Num_partidos_concejo_2015[i]
            d = Num_partidos_concejo_2019[i]
            
            if b>a:
                Aumento_Concejo.append("AUMENTÓ")
            elif b<a:
                Aumento_Concejo.append("DISMINUYÓ")
            elif b==a:
                Aumento_Concejo.append("SE MANTUVO")  
            
            if d>c:
                Aumento_P_Concejo.append("AUMENTÓ")
            elif d<c:
                Aumento_P_Concejo.append("DISMINUYÓ")
            elif d==c :
                Aumento_P_Concejo.append("SE MANTUVO") 

        
    if Corpo.lower() == "concejo":
        df2 = pd.DataFrame({"Departamento":DeparAu,"Municipio":MuniAu,"Corporación":Corpo,"Participación 2015":Participacion_concejo_2015,"Participación 2019":Participacion_concejo_2019,"Conclusión 1":Aumento_Concejo,"# Partidos 2015":Num_partidos_concejo_2015,"# Partidos 2019":Num_partidos_concejo_2019,"Conclusión 2":Aumento_P_Concejo})
        df2.to_csv(docAumento,mode = 'a', encoding = 'latin',index = False,sep=";",header=False)
    else:
        df3 = pd.DataFrame({"Departamento":DeparAu,"Municipio":MuniAu,"Corporación":Corpo,"Participación 2015":Participacion_alcaldia_2015,"Participación 2019":Participacion_alcaldia_2019,"Conclusión 1":Aumento_Alcaldia,"# Candidatos 2015":Num_partidos_alcaldia_2015,"# Candidatos 2019":Num_partidos_alcaldia_2019,"Conclusión 2":Aumento_P_Alcaldia})
        df3.to_csv(docAumento,mode = 'a', encoding = 'latin',index = False,sep=";",header=False)
         
    return()


#Creamos las listas a usar:    
Partidos = [] #Contiene los partidos o candidatos de la corporación a consultar en 2015
Num_partidos_alcaldia_2015 = [] # Número de candidatos a la alcaldia 2015 en el territorio a consultar
Num_partidos_concejo_2015 = [] # Número de partidos al concejo 2015 en el territorio a consultar
Partidos_2019 = [] # #Contiene los partidos o candidatos de la corporación a consultar en 2019
Num_partidos_alcaldia_2019 = []
Num_partidos_concejo_2019 = [] 
Participacion_alcaldia_2015 = [] 
Participacion_concejo_2015 = [] 
Participacion_alcaldia_2019 = [] 
Participacion_concejo_2019 = [] 
Aumento_Alcaldia = [] 
Aumento_P_Alcaldia = [] 
Aumento_Concejo = [] 
Aumento_P_Concejo = []
Votos_abs = [] 
Votos_abs_2019 = [] 
Votos_porc = [] 
Votos_porc_2019 = [] 
Curules = [] 
Datos = [] 
urld = ""
urldd = ""
dptod = ["",""]

# Damos el nombre de archivo de municipios a consultar
archivo = 'Lista_Municipios.csv'


#Importamos los datos a python
Datos = pd.read_csv(archivo,header=0,encoding = 'latin')
#Pasamos los datos de dataframe a lista y los organizamos en columnas:
Datos = Datos.values.tolist()
for i in  range(len(Datos)):
    Datos[i] = Datos[i][0].split(";")


#Creamos los archivos csv donde vamos a alojar toda la información recopilada
#DocumentoAlcaldia = "Final_Alcaldia.csv"
#Documento_AumentoAlcaldia = "AumentoAlcaldia.csv"
DocumentoConcejo = "Final_Concejo.csv"
Documento_AumentoConcejo = "AumentoConcejo.csv"


# links de las paginas donde se va a realizar web scraping:

link1 = "https://elecciones.registraduria.gov.co:81/esc_elec_2015/99AL/DALZZZZZZZZZZZZZZZZZ_L1.htm"
link2 = "https://www.colombia.com/elecciones/2019/regionales/"


    
# Sacamos información de los municipios:
barrido_info(Datos,"CONCEJO",DocumentoConcejo,Documento_AumentoConcejo,link1,link2)   
#barrido_info(Datos,"ALCALDIA",DocumentoAlcaldia,Documento_AumentoAlcaldia,link1,link2)

#Cerramos el navegador:
driver.close()  

