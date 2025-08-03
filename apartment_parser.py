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
import logging

logger = logging.getLogger("apartment_parser")
logger.setLevel(logging.INFO)  
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def create_driver(config):
    options = Options()
    options.binary_location = config.CHROMIUM_PATH
    
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

def parse_apartments(config):
    driver = create_driver(config)
    wait = WebDriverWait(driver, config.WAIT_TIMEOUT)
    apartments = {}
    
    try:
        logger.info("Loading page...")
        driver.get(config.URL)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "central-content")))

        for page_count in tqdm(range(config.MAX_PAGES), desc="Parsing pages"):
            logger.info(f"Parsing page #{page_count}")
            
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "central-content")))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            cards = driver.find_elements(By.CLASS_NAME, "product-item")
            logger.info(f"Cards found: {len(cards)}")
            
            for card in cards:
                try:
                    # Price
                    price = "N/A"
                    try:
                        price_element = card.find_element(By.CSS_SELECTOR, ".central-feature i")
                        price = price_element.text.strip()
                    except:
                        pass
                    
                    # Address
                    address = "N/A"
                    try:
                        location_items = card.find_elements(By.CSS_SELECTOR, ".subtitle-places li")
                        if location_items:
                            address_parts = [item.text.strip() for item in location_items[1:]]
                            address = ", ".join(address_parts)
                    except:
                        pass
                    
                    # Details
                    squares = "N/A"
                    rooms = "N/A"
                    floor = "N/A"
                    
                    try:
                        details = card.find_elements(By.CLASS_NAME, "value-wrapper")
                        if details:
                            squares = details[0].text.split('\n')[0].strip() if len(details) > 0 else "N/A"
                            rooms = details[1].text.split('\n')[0].strip() if len(details) > 1 else "N/A"
                            floor = details[2].text.split('\n')[0].strip() if len(details) > 2 else "N/A"
                    except:
                        pass
                    
                    key = (address, price)
                    if key not in apartments:
                        apartments[key] = {
                            "Price": price,
                            "Address": address,
                            "Squares": squares,
                            "Rooms": rooms,
                            "Floor": floor
                        }
                        logger.info(f"Note added: {address} | {price}")
                
                except (NoSuchElementException, StaleElementReferenceException) as ex:
                    logger.warning(f"Error parsing card: {ex}")
                    continue
            
            # Pagination
            try:
                next_btn = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "a.page-link.next")
                ))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
                driver.execute_script("arguments[0].click();", next_btn)
                logger.info(f"Moving to page #{page_count + 1}")
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "central-content")))
                
            except (NoSuchElementException, TimeoutException):
                logger.info("Last page reached")
                break
            except Exception as ex:
                logger.error(f"Pagination error: {ex}")
                break

        # Save results
        if apartments:
            df = pd.DataFrame(list(apartments.values()))
            df.to_csv(config.OUTPUT_PARSER_PATH, index=False)
            logger.info(f"\nData saved to: {config.OUTPUT_PARSER_PATH}")
            logger.info(f"Total records: {len(apartments)}")
            return df
        else:
            logger.warning("No data collected")
            return None

    except Exception as ex:
        logger.critical(f"Critical error: {ex}")
        return None
    finally:
        driver.quit()
        logger.info("Driver closed")

if __name__ == '__main__' :
    logger.setLevel(logging.INFO)
    try:
        from config.private_config import ProdConfig
        config=ProdConfig()
        
        class ParserTestConfig:
            CHROMEDRIVER_PATH = config.CHROMEDRIVER_PATH
            CHROMIUM_PATH = config.CHROMIUM_PATH

            # Proxy settings
            PROXY_HOST = config.PROXY_HOST
            PROXY_PORT = config.PROXY_PORT
            PROXY_USER = config.PROXY_USER
            PROXY_PASS = config.PROXY_PASS

            # Parser parameters
            URL = config.URL
            MAX_PAGES = 3
            OUTPUT_PARSER_PATH = "test/resultsTest.csv"
            WAIT_TIMEOUT = config.WAIT_TIMEOUT
            logger.info("Running apartment parser in test mode...")
    except ImportError:
        from config.public_config import BaseConfig
        class SafeTestConfig(BaseConfig):
            CHROMEDRIVER_PATH = "/path/to/chromedriver"
            CHROMIUM_PATH = "/path/to/chromium"
            PROXY_HOST = None
            PROXY_PORT = None
            PROXY_USER = None
            PROXY_PASS = None

        config = SafeTestConfig()
        logger.warning("Running in safe test mode without proxy")

    result = parse_apartments(ParserTestConfig)
    logger.info("test completed")