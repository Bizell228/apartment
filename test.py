import requests
from bs4 import BeautifulSoup
import collections
import csv
import transliterate
import re
from config.public_config import BaseConfig

apartmentInfo = collections.namedtuple(
    'apartmentInfo',
    [
        'price',
        'rooms',
        'street',
        'district',
        'subway_station_time',
        'floor',
        'floors_total',
        'square_meters',
        'commissions',
        'author',
        'building_year',
        'living_space',
        'kitchen_meters',
        'link'
    ]
)

max_pages = BaseConfig.MAX_PAGES

class CianPasrer:
    def __init__(self):
        self.session = requests.Session()
        self.sesion.headers = {
            'User-Agent' : f'Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0', 
            'Accept-Language': 'ru'
        }
        self.result = []
        self.result.append(apartmentInfo(
            price = 'price',
            rooms = 'rooms',
            street = 'street',
            district = 'district',
            subway_station_time = 'subway_station_time',
            floor = 'floor',
            floors_total = 'floors_total',
            square_meters = 'square_meters',
            commissions = 'commissions',
            author = 'author',
            building_year = 'building_year',
            living_space = 'living_space',
            kitchen_meters = 'kitchen_meters',
            link = 'link'
             ))

    #Loading page    
    def load_page(self, i=1):
        pass

    #will get html
    def parse_page(self, html: str):
        pass
    
    #parse
    def parse_page_offer(self, html_offer):
        pass
    
    #
    def parse_block(self, block):
        pass

