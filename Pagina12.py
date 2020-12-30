import requests
from bs4 import BeautifulSoup
import lxml.html as html

class articulo:
    def __init__(self, seccion, url,fecha,titulo,reseña,resumen,imagen_src):
        self.seccion=seccion
        self.url=url
        self.fecha=fecha
        self.titulo=titulo
        self.reseña=reseña
        self.resumen=resumen
        self.imagen_src=imagen_src
        
    def print_articulo(self):
        print(self.seccion)
        print(self.url)
        print(self.fecha,'\n')

def list_new_secciones(links):
    news=BeautifulSoup(links.text,'html.parser')
    bajadas=news.find_all('div', attrs={'class':'article-item__content'})
    links_h2_noticias=[f.h2.a.get('href') for f in bajadas if f.h2]
    links_h3_noticias=[f.h3.a.get('href') for f in bajadas if f.h3]
    links_h4_noticias=[f.h4.a.get('href') for f in bajadas if f.h4]
    return links_h2_noticias +links_h3_noticias+links_h4_noticias

def traer_fecha(articulo_url):
    try:
        s_articulo=requests.get(articulo_url)
        if s_articulo.status_code== 200:
            s_articulo2=BeautifulSoup(s_articulo.text,'html.parser')
            fecha=s_articulo2.find('span', attrs={'pubdate':'pubdate'})
            date=fecha.get('datetime')
        else:
            date=None
    except  ValueError as ve:
            print("Hubo un error en la request")
            print(ve)
            print("\n")    
    return date

def run():
    url= 'https://www.pagina12.com.ar/'
    p12= requests.get(url)
    if p12.status_code== 200:
        s=BeautifulSoup(p12.text,'html.parser')
        secciones=s.find('ul', attrs={'class':'horizontal-list main-sections hide-on-dropdown'}).find_all('li')
        links_secciones=[seccion.a.get('href') for seccion in secciones]
        lista_de_articulos=[]
        sec=[]
        s=[]
        i=0
        n=len(links_secciones)
        print(n)
        while i<n:
            a=secciones[i].a.get_text()
            sec=links_secciones[i]
            try:
                print(a)
                s=s+list_new_secciones(requests.get(sec))
                for art in s:
                    lista_de_articulos.append(articulo(a,art,'','','','',''))                
            except  ValueError as ve:
                print("Hubo un error en la request")
                print(ve)
                print("\n")        
            i=i+1
        for obj in lista_de_articulos:
            a_url=obj.url
            obj.fecha= traer_fecha(a_url)
            obj.print_articulo()
        print(len(lista_de_articulos))

if __name__=='__main__':
    run()