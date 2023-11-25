
import scrapy
from scrapy.crawler import CrawlerProcess
from tqdm import tqdm
import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))
from house_price_scraper.items import HousePriceScraperItem

# scrapy crawl ibatdongsanSpider
class ibatdongsanSpider(scrapy.Spider):
    name = "ibatdongsanSpider"
    allowed_domains = ["i-batdongsan.com"]

    custom_settings = {
        'LOG_FILE': "ibatdongsanSpider.log",
        # 'FEEDS' : {
        #     'ibatdongsan.csv': {'format':'csv', 'overwrite':True},
        # },
    }

    def __init__(self, *args, **kwargs):
        super(ibatdongsanSpider, self).__init__(*args, **kwargs)
        #Find "Processing page" in log file to fill value for number of pages. To make sure that all pages are crawled, we can take value found minus 1. But it takes more time to crawl again.
        self.num_page = 1
        self.original_url = "https://i-batdongsan.com/can-ban-nha-dat/ha-noi-t1.htm"
        self.start_urls = ["https://i-batdongsan.com/can-ban-nha-dat/ha-noi-t1.htm"]
        # self.start_urls = [self.original_urls + "?page=" + str(self.num_page)]
        self.progress_bar = []
           
    def parse(self, response):
        bds_links = response.css('div.ct_title > a::attr(href)').extract()
        self.logger.info(f"Processing page: {self.num_page}")
        
        # Estimate time to crawl all pages, sometimes it's not accurate because of retrying requests
        self.progress_bar.append(tqdm(total=len(bds_links), desc=f"Processing and saving page: {self.num_page}"))
        for link in bds_links:
            url = "https://i-batdongsan.com" + link
            yield response.follow(url, callback=self.parse_bds_page)
        
        if bds_links:
            self.num_page += 1
            next_page_url = self.original_url[:-4] + "/p" + str(self.num_page) + ".htm"
            yield response.follow(next_page_url, callback=self.parse)

    def parse_bds_page(self, response):
        
        item = HousePriceScraperItem()
        item['html_content'] = response.text
        item['url'] = response.url
        item['progress_bar'] = self.progress_bar[-1]
        yield item

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "ibatdongsan.csv": {"format": "csv"},
        },
    })

    process.crawl(ibatdongsanSpider)
    process.start()
