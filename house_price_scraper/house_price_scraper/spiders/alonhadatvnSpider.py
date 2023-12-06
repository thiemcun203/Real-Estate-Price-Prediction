
import scrapy
from scrapy.crawler import CrawlerProcess
from tqdm import tqdm
import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))
from house_price_scraper.items import HousePriceScraperItem
import time
import random
# scrapy crawl alonhadatvnSpider
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from scrapy.selector import Selector

# class alonhadatvnSpider(scrapy.Spider):
#     name = "alonhadatvnSpider"
#     allowed_domains = ["alonhadat.com.vn"]

#     custom_settings = {
#         'LOG_FILE': "alonhadatvnSpider.log",
#         # 'FEEDS' : {
#         #     'alonhadatvn.csv': {'format':'csv', 'overwrite':True},
#         # },
#         # 'REDIRECT_ENABLED': False,

#         # 'REDIRECT_MAX_TIMES': 2
#     }


#     def __init__(self, *args, **kwargs):
#         super(alonhadatvnSpider, self).__init__(*args, **kwargs)
#         #Find "Processing page" in log file to fill value for number of pages. To make sure that all pages are crawled, we can take value found minus 1. But it takes more time to crawl again.
#         self.num_page = 24 - 1
#         self.original_url = "https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/1/ha-noi.html"
#         self.start_urls = ["https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/1/ha-noi.html"]
#         # self.start_urls = [self.original_urls + "?page=" + str(self.num_page)]
#         self.progress_bar = []
    
#     def parse(self, response):

#         bds_links = response.css('div.ct_title > a::attr(href)').extract()
#         self.logger.info(f"Processing page: {self.num_page}")
        
#         # Estimate time to crawl all pages, sometimes it's not accurate because of retrying requests
#         self.progress_bar.append(tqdm(total=len(bds_links), desc=f"Processing and saving page: {self.num_page}"))
#         for link in bds_links:
#             time.sleep(random.uniform(1, 3))
#             url = "https://alonhadat.com.vn" + link
#             yield response.follow(url, callback=self.parse_bds_page)
        
#         if bds_links:
#             self.num_page += 1
#             next_page_url = self.original_url[:-5] + "/trang--" + str(self.num_page) + ".html"
#             yield response.follow(next_page_url, callback=self.parse)

#     def parse_bds_page(self, response):
        
#         item = HousePriceScraperItem()
#         item['html_content'] = response.text
#         item['url'] = response.url
#         item['progress_bar'] = self.progress_bar[-1]
#         yield item

def clean_link(link):
    # Define the part to be removed from the link
    part_to_remove = "xac-thuc-nguoi-dung.html?url=/"

    # Check if the link contains the part to remove
    if part_to_remove in link:
        # Remove the part and return the cleaned link
        return link.replace(part_to_remove, "")
    else:
        # If the part is not in the link, return the link unchanged
        return link
class alonhadatvnSpider(scrapy.Spider):
    name = "alonhadatvnSpider"
    allowed_domains = ["alonhadat.com.vn"]

    custom_settings = {
        'LOG_FILE': "alonhadatvnSpider.log",
    }

    def __init__(self, *args, **kwargs):
        super(alonhadatvnSpider, self).__init__(*args, **kwargs)
        self.num_page = 25 - 1
        self.original_url = "https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/1/ha-noi.html"
        self.start_urls = [self.original_url]
        self.progress_bar = []

       

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={'handle_httpstatus_all': True})

    def parse(self, response):
         # Selenium setup
        webdriver_path = '/Users/nguyenbathiem/Documents/GitHub/StockBot/Real-Estate-Price-Prediction/house_price_scraper/house_price_scraper/spiders/chromedriver'  # Change this to your Chromedriver path
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument("--incognito")
        self.driver = webdriver.Chrome(service=Service(webdriver_path), options=chrome_options)
        self.driver.get(clean_link(response.url))
        time.sleep(3)  # Wait for the page to load

        # Create a Selector from the Selenium response
        with open('/Users/nguyenbathiem/Documents/GitHub/StockBot/Real-Estate-Price-Prediction/house_price_scraper/house_price_scraper/spiders/test.html', 'w', encoding='utf-8') as f:
            f.write(self.driver.page_source)
        sel = Selector(text=self.driver.page_source)

        bds_links = sel.css('div.ct_title > a::attr(href)').extract()
        self.logger.info(f"Processing page: {self.num_page}")

        # Progress bar logic
        self.progress_bar.append(tqdm(total=len(bds_links), desc=f"Processing and saving page: {self.num_page}"))
        while not bds_links:
            for link in bds_links:
                time.sleep(random.uniform(1, 3))
                # yield scrapy.Request(clean_link(url), callback=self.parse_bds_page)
                url = "https://alonhadat.com.vn" + link
                self.driver.get(url)
                item = HousePriceScraperItem()
                item['html_content'] = self.driver.page_source
                item['url'] = url
                item['progress_bar'] = self.progress_bar[-1]
                yield item
            
        if bds_links:
            self.num_page += 1
            next_page_url = self.original_url[:-5] + "/trang--" + str(self.num_page) + ".html"
            self.driver.quit()
            yield response.follow(next_page_url, callback=self.parse)
            
                
    # def closed(self, reason):
    #     self.driver.quit()

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "alonhadatvn.csv": {"format": "csv"},
        },
    })

    process.crawl(alonhadatvnSpider)
    process.start()
