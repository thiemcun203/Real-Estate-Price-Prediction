
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

class batdongsanSpider(scrapy.Spider):
    name = "batdongsanSpider"
    allowed_domains = ["batdongsan.com.vn"]

    custom_settings = {
        'LOG_FILE': "batdongsanSpider.log",
    }

    def __init__(self, *args, **kwargs):
        super(batdongsanSpider, self).__init__(*args, **kwargs)
        self.num_page = 1
        self.original_url = "https://batdongsan.com.vn/ban-can-ho-chung-cu-ha-noi?cIds=362,41,325,163,575,361,40,283,44,562,45,48"
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
        
        # self.driver.set_page_load_timeout(2)
        self.driver.get(response.url)
        time.sleep(3)  # Wait for the page to load

        # Create a Selector from the Selenium response
        with open('/Users/nguyenbathiem/Documents/GitHub/StockBot/Real-Estate-Price-Prediction/house_price_scraper/house_price_scraper/spiders/test.html', 'w', encoding='utf-8') as f:
            f.write(self.driver.page_source)
        sel = Selector(text=self.driver.page_source)

        bds_links = sel.css('a.js__product-link-for-product-id::attr(href)').getall()
        self.logger.info(f"Processing page: {self.num_page}")

        # Progress bar logic
        self.progress_bar.append(tqdm(total=len(bds_links), desc=f"Processing and saving page: {self.num_page}"))
        print(bds_links)
        for link in bds_links:
            time.sleep(random.uniform(1, 3))
            # yield scrapy.Request(clean_link(url), callback=self.parse_bds_page)
            url = "https://batdongsan.com.vn" + link
            self.driver.get(url)
            item = HousePriceScraperItem()
            item['html_content'] = self.driver.page_source
            item['url'] = url
            item['progress_bar'] = self.progress_bar[-1]
            yield item
            
        if bds_links:
            self.num_page += 1
            link = sel.css('a.re__pagination-icon::attr(href)').get()
            next_page_url = 'https://batdongsan.com.vn'+ link 
            self.driver.quit()
            yield response.follow(next_page_url, callback=self.parse)
            
                
    # def closed(self, reason):
    #     self.driver.quit()

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "batdongsan.csv": {"format": "csv"},
        },
    })

    process.crawl(batdongsanSpider)
    process.start()
