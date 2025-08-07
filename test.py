from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import time
import pandas as pd
from tqdm import tqdm
import logging
import collections
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

logger = logging.getLogger("apartment_parser")
logger.setLevel(logging.INFO)  
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class CianPasrer:
    config = BaseConfig()
    max_pages = config.MAX_PAGES

    def __init__(self):
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

    def create_driver(config):
        options = Options()
        options.binary_location = config.CHROMIUM_PATH
        service = Service(config.CHROMEDRIVER_PATH)
        return webdriver.Chrome(
            service=service, 
            options=options
        )

    #Loading page and extracting html from it.
    def load_page(self, i=1):
        driver = self.create_driver(self.config)
        wait = WebDriverWait(driver, self.config.WAIT_TIMEOUT)



    #Will pfrse html that we got in load function.
    def parse_page(self, html: str):
        pass
    #parses insides of every offer using parsed url
    def parse_page_offer(self, html_offer):
        pass
    
    #parses every "card" listed on a page
    def parse_block(self, block):
        pass
        

if __name__ == "__main__":
    options = Options()
    config = BaseConfig()
    options.binary_location = config.CHROMIUM_PATH
    service = Service(config.CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(
        service=service, 
        options=options
    )
    driver.get("https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&region=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room7=1&room9=1&type=4")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    title = driver.find_element(By.CSS_SELECTOR, "Title")
    time.sleep(3)
    print(title.get_attribute("outerHTML"))