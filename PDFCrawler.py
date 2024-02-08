from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import validators
import os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


from PageSourceScraper import PageSourceScraper
class PDFURLCrawler(PageSourceScraper):
    def __init__(self) -> None:
        print("initializing Crawler")
        super().__init__()
        self.pdfs = set()
        self.hrefs = set()
        self.parsed_urls = set()
        self.session = requests.Session()
        retry = Retry(
            total=0,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.blacklisturls = [
    'https://www.instagram.com',
    'https://www.facebook.com',
    'https://www.twitter.com',
    'https://www.linkedin.com',
    'https://www.pinterest.com',
    'https://www.snapchat.com',
    'https://www.reddit.com',
    'https://www.tiktok.com',
]
        self.wrong_status_codes = [403,400]
    
    def check_url_status(self,url):
        response = self.session.get(url, allow_redirects=True)
        return response.status_code
    def crawl(self,url, limit, base_url):
            response = None
            if limit <= 0:
                return self.pdfs
            try:
                if url not in self.blacklisturls:
                    response = self.session.get(url, allow_redirects=True)
                    print(response)
                    # time.sleep(5)

                else:
                    response = None
            except Exception as e:
                print("Exception: ",str(e))
            finally:
                if response:
                    if response.status_code == 200:
                        soup = self.download_and_parse(url)
                        anchor_tags = soup.find_all('a')
                        for anchor in anchor_tags:
                            
                            href = anchor.get('href') 
                            # Check if the anchor is not None
                            if href is not None:
                                if '.pdf' in href:
                                    if href.startswith('https://'):
                                        # print("PDF Found: " + href)
                                        self.pdfs.add(href)
                                    else:
                                        abs_link = urljoin(base_url, href)
                                        self.pdfs.add(abs_link)
                                        # print("PDF Found without https " + abs_link)
                                if not href.startswith('https://'):
                                    if href not in self.hrefs:
                                        self.hrefs.add(href)
                                        #print("Reference Links:", href)
                                        absolute_link = urljoin(base_url, href)
                                        self.crawl(absolute_link, limit - 1, base_url)
                                if href.startswith('https://'):
                                    self.crawl(href, limit - 1, base_url)

                    elif response.status_code in self.wrong_status_codes:
                        print("Request Forbidden!")
                        print("Problematic URL: ", url)
                    else:
                        print("Stopped because invalid URL")
                        print("Problematic URL: ", url)
                    
                
            return list(self.pdfs)

if __name__ == "__main__":
    crawler = PDFURLCrawler()
    pdfs = crawler.crawl(url = "https://abc.xyz/investor/", limit=1, base_url="https://abc.xyz/investor/")
    print(pdfs)
    
 