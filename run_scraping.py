import asyncio
import codecs
import os, sys
import datetime as dt

from django.contrib.auth import get_user_model
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "myfirst.settings"

import django
django.setup()

from scraping.parsers import hh, hh_js
from scraping.models import Vacancy, Error, Url

User = get_user_model()

parsers = (
    (hh, 'hh'),
    (hh_js, 'hh')
)
jobs, errors = [], []


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dct[pair]
        urls.append(tmp)
    return urls


async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    jobs.extend(job)

settings = get_settings()
url_list = get_urls(settings)

loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
             for data in url_list
             for func, key in parsers]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])

#for data in url_list:

    #for func, key in parsers:
        #url = data['url_data'][key]
        #j, e = func(url, city=data['city'], language=data['language'])
        #jobs += j
        #errors += e

loop.run_until_complete(tasks)
loop.close()

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    er = Error(data=errors).save()


#h = codecs.open('hh.txt', 'w', 'utf-8')
#h.write(str(jobs))
#h.close()
ten_days_ago = dt.date.today() - dt.timedelta(10)
Vacancy.objects.filter(timestamp__lte=ten_days_ago).delete()
