import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint

__all__ = ('hh')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    ]


#Функция для парсинга сайта
def hh(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://hh.ru'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'vacancy-serp'})
            div_lst = main_div.find_all('div', attrs={'class': 'vacancy-serp-item'})
            for div in div_lst:
                title = div.find('div', attrs={'class': 'vacancy-serp-item__row_header'})
                href = title.a['href']
                cont = div.find('div', attrs={'class': 'g-user-content'})
                content = cont.text
                company = 'No name'
                a = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'})
                if a:
                    company = a.text
                jobs.append({'title': title.text, 'url': href,
                            'description': content, 'company': company,
                             'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


if __name__ == '__main__':
    url = 'https://hh.ru/search/vacancy?area=2&fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post'
    jobs, errors = hh(url)
    h = codecs.open('hh.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
