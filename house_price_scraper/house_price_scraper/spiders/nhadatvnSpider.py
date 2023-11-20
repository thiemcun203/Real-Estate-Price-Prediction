
import scrapy
from scrapy.crawler import CrawlerProcess
from tqdm import tqdm
import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))
from house_price_scraper.items import HousePriceScraperItem

# scrapy crawl nhadatvnSpider
class nhadatvnSpider(scrapy.Spider):
    name = "nhadatvnSpider"
    allowed_domains = ["nhadatvn.com.vn"]

    custom_settings = {
        'LOG_FILE': "nhadatvnSpider.log",
    }

    def __init__(self, *args, **kwargs):
        super(nhadatvnSpider, self).__init__(*args, **kwargs)
        #Find "Processing page" in log file to fill value for number of pages. To make sure that all pages are crawled, we can take value found minus 1. But it takes more time to crawl again.
        self.num_page = 1130 - 1
        # self.original_urls = "https://nhadatvn.com.vn/nha-dat-ban-kv-ha-noi.html"
        self.start_urls = ['https://batdongsan.com.vn/ban-nha-rieng-ha-noi']
        # self.start_urls = [self.original_urls + "?page=" + str(self.num_page)]
        self.progress_bar = []
           
    def parse(self, response):
        bds_links = response.css('.ten a::attr(href)').extract()
        self.logger.info(f"Processing page: {self.num_page}")
        
        # Estimate time to crawl all pages, sometimes it's not accurate because of retrying requests
        self.progress_bar.append(tqdm(total=len(bds_links), desc=f"Processing and saving page: {self.num_page}"))
        for links in bds_links:
            url = links
            yield response.follow(url, callback=self.parse_bds_page)
        
        if bds_links:
            self.num_page += 1
            next_page_url = self.original_urls + "?page=" + str(self.num_page)
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
            "nhadatvn.csv": {"format": "csv"},
        },
    })

    process.crawl(nhadatvnSpider)
    process.start()
