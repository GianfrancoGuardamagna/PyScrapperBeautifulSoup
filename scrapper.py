import json
from bs4 import BeautifulSoup
import requests


dataJson = './ods.json'

itemsExistentes = []
itemsInexistentes = []
descripciones = []

with open(dataJson) as json_file:
    datos = json.load(json_file)

    for objeto in datos:
        codigo = objeto.get('codigo')
        if codigo:

            url = f'https://www.maquinariayhosteleria.es/buscar/{codigo}/'

            respuesta = requests.get(url)
            html = respuesta.text

            soup = BeautifulSoup(html, 'html.parser')
                
            condicionPrimera = soup.find_all('p', class_='no-disponible')
            condicionSegunda = soup.find_all('article', class_='celda-listado-productos')

            if condicionPrimera:
                itemsInexistentes.append(codigo)
            elif condicionSegunda:
                for link in soup.find_all('a', class_='imagen-producto'):
                    itemsExistentes.append(codigo)
                    
                    pieza = link.get('href')
                        
                    url = f'https://www.maquinariayhosteleria.es{pieza}'
                        
                    respuesta = requests.get(url)

                    html = respuesta.text
                        
                    soup = BeautifulSoup(html, 'html.parser')
                        
                    descripcion = soup.find('ul', id='descripcionmovil' , class_='list')

                    data = {"link": url,"descripcion":str(descripcion)}
                        
                    data = json.dumps(data)
                        
                    with open(f'{codigo}.txt', 'a') as file:
                            file.write(data)

with open('Codigos Inexistentes.txt', 'a') as file:
    for code in itemsInexistentes:
        file.write(code + '\n')

print("Se finalizó el proceso señor Miyagi")
