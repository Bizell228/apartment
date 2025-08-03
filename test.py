# apartment_parser.py

from seleniumwire import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import time
import pandas as pd
from tqdm import tqdm

def create_driver(config):
    options = Options()
    options.binary_location = config.CHROMIUM_PATH
    options.add_argument("--headless")
    
    seleniumwire_options = {
        'proxy': {
            'http': f'socks5://{config.PROXY_USER}:{config.PROXY_PASS}@{config.PROXY_HOST}:{config.PROXY_PORT}',
            'https': f'socks5://{config.PROXY_USER}:{config.PROXY_PASS}@{config.PROXY_HOST}:{config.PROXY_PORT}',
        }
    }
    
    service = Service(config.CHROMEDRIVER_PATH)
    return webdriver.Chrome(
        service=service, 
        options=options, 
        seleniumwire_options=seleniumwire_options
    )
    


if __name__ == '__main__' :
    from config.private_config import ProdConfig
    config=ProdConfig()
    driver = create_driver(config)
    wait = WebDriverWait(driver, config.WAIT_TIMEOUT)
    driver.get(config.URL)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-item")))
    card = driver.find_element(By.CLASS_NAME, 'a-images')
    link = card.get_attribute('href')
    driver.get(link)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'product-image-section')))
    first = driver.find_element(By.CLASS_NAME, 'prominent')
    info_first = first.find_elements(By.CSS_SELECTOR, '.prominent span')
    info_text = [inf.text for inf in info_first]
    print(info_text)
