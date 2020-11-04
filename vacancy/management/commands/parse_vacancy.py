import requests
import bs4
import urllib.parse
import datetime

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from vacancy.models import Product


class VacancyParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
            'accept': '*/*',
        }

    def get_page(self, page: int = None):
        params = {
            'L_is_autosearch': 'false',
            'area': 1002,
            'clusters': 'true',
            'enable_snippets': 'true',
            'text': 'python',
            'page': 5,

        }
        if page and page > 0:
            params['page'] = page

        url = 'https://rabota.by/search/vacancy'
        r = self.session.get(url, params=params)
        return r.text

    @staticmethod
    def parse_date(item: str):
        params = item.strip().split()
        if len(params) == 2:
            day, month_param = params
            day = int(day)
            months_dict = {
                'января': 1,
                'февраля': 2,
                'марта': 3,
                'апреля': 4,
                'мая': 5,
                'июня': 6,
                'июля': 7,
                'августа': 8,
                'сентября': 9,
                'октября': 10,
                'ноября': 11,
                'декабря': 12,
            }
            month = months_dict.get(month_param)
            today = datetime.date.today()
            return datetime.date(day=day, month=month, year=today.year)
        return 'не смогли разобрать дату'

    def parse_block(self, item):
        url_block = item.select_one('a.bloko-link.HH-LinkModifier')
        if not url_block:
            raise CommandError('bad "url_block" css')

        url = url_block.get('href')

        title_block = item.select_one('a.bloko-link.HH-LinkModifier')
        if not title_block:
            raise CommandError('bad "title_block" css')
        title = title_block.string.strip()

        company_block = item.select_one('a.bloko-link.bloko-link_secondary')
        if not company_block:
            raise CommandError('bad "company_block" css')
        company = company_block.string.strip()

        date = None
        date_block = item.select_one('span.vacancy-serp-item__publication-date')
        if not date_block:
            raise CommandError('bad "date_block" css')
        absolute_date = date_block.string.strip()
        if absolute_date:
            date = self.parse_date(item=absolute_date)

        try:
            p = Product.objects.get(link=url)
            p.title = title
            p.company = company
            p.date = date
            p.save()
        except Product.DoesNotExist:
            p = Product(
                title=title,
                company=company,
                date=date,
                link=url,
            ).save()
        print(f'Product {p}')


    def get_pagination_limit(self):
        text = self.get_page()
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select('a.bloko-button')
        last_bottom = container[-1]
        href = last_bottom.get('href')
        if not href:
            return 1

        r = urllib.parse.urlparse(href)
        params = urllib.parse.parse_qs(r.query)
        return int(params['page'][0])

    def get_blocks(self, page: int = None):
        text = self.get_page(page=page)
        soup = bs4.BeautifulSoup(text, 'lxml')

        container = soup.select('div.vacancy-serp-item')
        for item in container:
            block = self.parse_block(item=item)
            print(block)

    def parse_all(self):
        limit = self.get_pagination_limit()
        print(f'Всего страниц {limit}')
        for i in range(1, limit + 1):
            self.get_blocks(page=i)


class Command(BaseCommand):
    help = "Parsing rabota.tut.by"

    def handle(self, *args, **options):
        p = VacancyParser()
        p.parse_all()
        