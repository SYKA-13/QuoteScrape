from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

HUB_URL = 'http://selenium-hub:4444/wd/hub'  # URL of the Selenium Grid Hub

# MongoDB setup
client = MongoClient('mongodb+srv://Kalam1:syha2654@cluster1.4lpgqtp.mongodb.net/?retryWrites=true&w=majority')
db = client['mcs_assignment']
collection = db['quotes']

def scrape_page(page_number):
    try:
        options = Options()
        options.set_capability('browserName', 'chrome')

        driver = webdriver.Remote(
            command_executor=HUB_URL,
            options=options
        )

        driver.get(f"http://quotes.toscrape.com/page/{page_number}")

        for i in range(1, 11):
            quote_xpath = f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[1]"
            author_xpath = f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[2]/small"
            quote_element = driver.find_element(By.XPATH, quote_xpath)
            quote_text = quote_element.text
            author_element = driver.find_element(By.XPATH, author_xpath)
            author_name = author_element.text
            print("Quote:", quote_text)
            print("Author:", author_name)
            print()
            document = {
                'quote_id': (page_number-1) * 10 + i,
                'quote': quote_text,
                'author': author_name
            }
            collection.insert_one(document)
    except Exception as e:
        print(f"Error on page {page_number}: {e}")
    finally:
        driver.quit()


with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(scrape_page, range(1, 11))
