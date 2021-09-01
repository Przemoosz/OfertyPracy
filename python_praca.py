import os

import requests
from bs4 import BeautifulSoup


def main():
    try:
        # Pobranie tekstu HTML ze strony Pracuj.pl
        html_text = requests.get("https://www.praca.pl/s-elektryk,poznan.html?p=elektryk&m=Pozna%C5%84%2C").text
        #"https://www.praca.pl/s-programista,python,poznan.html?p=Programista+Python&m=Pozna%C5%84%2C+"
    except Exception:
        exit("Do not received 200 OK from page")

    soup = BeautifulSoup(html_text, 'lxml')
    for job in soup.find_all('li', class_="listing__item"):
        if job.find('a', class_="listing__offer-title job-id") == None:
            pass
        else:
            name = job.find('a', class_="listing__offer-title job-id").text
        if job.find('button', class_="listing__offer-title job-id listing__region-toggler") == None:
            pass
        else:
            name = job.find('button', class_="listing__offer-title job-id listing__region-toggler").text
        if job.find('a', class_="listing__info listing__info--name") == None:
            company = None
        else:
            company = job.find('a', class_="listing__info listing__info--name").text
        if job.find('div', class_="listing__tab listing__tab--job-level") == None:
            pass
        else:
            wymagania = job.find('div', class_="listing__tab listing__tab--job-level").text
        print(f"Nazwa: {name}\n"
              f"Pracodowaca: {company}\n"
              f"Wymagania: {wymagania}\n")
        # wym = job.find('div', class_="listing__tab listing__tab--job-level")
        # print(wym.text)
    pass


if __name__ == '__main__':
    main()
