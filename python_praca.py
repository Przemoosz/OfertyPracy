import os
import re
import requests
import datetime
from bs4 import BeautifulSoup
def strona(URL,page):
    if page == 1:
        return URL
    else:
        url_list=URL.split(".html")
        URL = url_list[0]+"_"+str(page) + '.html'+url_list[1]
        return URL

    pass
def praca_pl_scrap():
    page = 1
    # warunek petli
    var = True
    # zmienna przechowujaca pierwsze wyszukanie na stronie praca.pl
    first_for_praca = ""
    while True:
        try:
            url = strona("https://www.praca.pl/s-programista,python,poznan.html?p=Programista+Python&m=Pozna%C5%84%2C+",page)
            # Pobranie tekstu HTML ze strony Pracuj.pl
            html_text = requests.get(url).text
        except Exception:
            print("Do not received 200 OK from page")
            return False

        soup = BeautifulSoup(html_text, 'lxml')
        # szukanie listy ofert
        for job in soup.find_all('li', class_="listing__item"):
            # jeśli pierwsza oferta sie powtarza wyjdz z petli
            if job == first_for_praca and page != 1:
                return True
            if "s-programista" in url and var == True:
                first_for_praca = job
                var = False
                # szukanie nazwy stanowiska
            if job.find('a', class_="listing__offer-title job-id") == None:
                pass
            else:
                name = job.find('a', class_="listing__offer-title job-id").text
                link = "https://www.praca.pl"+job.find('a', href=True).attrs['href']
            if job.find('button', class_="listing__offer-title job-id listing__region-toggler") == None:
                pass
            else:
                name = job.find('button', class_="listing__offer-title job-id listing__region-toggler").text
                link = "https://www.praca.pl"+job.find('a', href=True).attrs['href']
                # szukanie nazwy pracodawcy
            if job.find('a', class_="listing__info listing__info--name") == None:
                if job.find('a', class_="listing__info listing__info--name listing__info--link") != None:
                    company = job.find('a', class_="listing__info listing__info--name listing__info--link").text
                else:
                    company = None
            else:
                company = job.find('a', class_="listing__info listing__info--name").text
                # szukanie wymagan
            if job.find('div', class_="listing__tab listing__tab--job-level") == None:
                pass
            else:
                wymagania = job.find('div', class_="listing__tab listing__tab--job-level").text
            print(f"Nazwa: {name}\n"
                  f"Pracodowaca: {company}\n"
                  f"Wymagania: {wymagania}\n"
                  f"Link: {link}\n")
            save(name,wymagania,link,company)
        page+= 1
def olx_scrap():
    try:
        url = "https://www.olx.pl/praca/q-programista-python/"
        html_text = requests.get(url).text
    except Exception:
        print("Do not received 200 OK from page")
        return False
    soup = BeautifulSoup(html_text, 'lxml')
    for jobs in soup.find_all('tr',class_="wrap"):
        name = jobs.find('h3')
        wymagania = jobs.find('small', class_="breadcrumb breadcrumb--job-type x-normal")
        #link = jobs.find('a', href = re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href']
        link = jobs.find('a',href=True).attrs['href']
        print(name.text.strip(),wymagania.text.strip(),link,sep=" ")
        #print(jobs)
        save(name.text.strip(), wymagania.text.strip(), link)
def pracuj_pl_scrap():
    try:
        url = "https://www.pracuj.pl/praca/programista%20python;kw/poznan;wp?rd=50"
        html_file = requests.get(url).text
    except Exception:
        print()
        print("Do not received 200 OK from page")
        return False
    soup = BeautifulSoup(html_file,'lxml')
    for job in soup.find_all('li',class_="results__list-container-item"):
        if job.find('h2') == None:
            return None
        else:
            name = job.find('h2').text.strip()
        company = job.find('span',class_="offer-company__wrapper").text.strip()
        #link = job.find('a',class_="offer-details__title-link",href=True).attr['href'
        link = job.find('a', href=True).attrs['href']
        #wymagania = job.find('div',class_="offer-labels__wrapper")
        #print(wymagania)
        #wymagania = wymagania_p.find('li',class_="offer-labels__item").text.strip()
        #link = None
        # print(f"Nazwa: {name}\n"
        #     f"Pracodowaca: {company}\n"
        #     f"Link: {link}\n")
        save(name=name,wymagania=None,link=link,company=company)
        if "staż" in name or "praktykant" in name or "praktyka" in name:
            save_staz(name=name,wymagania=None,link=link,company=company)



def save(name,wymagania,link,company=None):
    file_name = str(datetime.date.today())+".txt"
    with open(file_name,'a',encoding="UTF_8") as file:
        file.write("Name: {name}\n".format(name=name))
        file.write("Company: {name}\n".format(name=company))
        file.write("Wymiar pracy: {name}\n".format(name=wymagania))
        file.write("Link: {name}\n".format(name=link))
        file.write("\n")
        if wymagania == None or wymagania == str(None):
            return None
        if "staż" in wymagania or "praktykant" in wymagania or "praktyka" in wymagania:
            save_staz(name,wymagania,link,company)
def save_staz(name,wymagania,link,company=None):
    file_name = str(datetime.date.today()) +"_staż"+ ".txt"
    with open(file_name,'a',encoding="UTF_8") as file:
        file.write("Name: {name}\n".format(name=name))
        file.write("Company: {name}\n".format(name=company))
        file.write("Wymiar pracy: {name}\n".format(name=wymagania))
        file.write("Link: {name}\n".format(name=link))
        file.write("\n")
def first_open():
    file_name = str(datetime.date.today()) + ".txt"
    with open(file_name,'w') as file:
        pass
    file_name = str(datetime.date.today()) +"_staż"+ ".txt"
    with open(file_name, 'w') as file:
        pass
def main():
    first_open()
    praca_pl_scrap()
    olx_scrap()
    pracuj_pl_scrap()
    print(datetime.date.today())
    pass

if __name__ == '__main__':
    main()
