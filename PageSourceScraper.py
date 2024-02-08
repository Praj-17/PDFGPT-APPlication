
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from requests_html import HTMLSession
from bs4 import BeautifulSoup


class PageSourceScraper:
    def __init__(self) -> None:
        # self.driver_path = "assets/chromedriver.exe"
        service = Service()    
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(), service=service)
    def get_url_source(self,url):
        try:
            self.driver.get(url)
            return BeautifulSoup(self.driver.page_source, 'html.parser')
        except Exception as e:
            print("Exception: ", str(e))
        finally:
            self.driver.quit()
    
    def download_and_parse(self,url):
        session = HTMLSession()

        response = session.get(url)

        # response.html.render(timeout = 20)

        # Get the rendered HTML content
        page_source = response.html.html
        # Close the HTML session

        session.close()

        # Use BeautifulSoup to parse the HTML
        return BeautifulSoup(page_source, 'html.parser')