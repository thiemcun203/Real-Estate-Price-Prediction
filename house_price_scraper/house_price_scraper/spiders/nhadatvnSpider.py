import scrapy
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))
from  house_price_scraper.items import HousePriceScraperItem
from scrapy.crawler import CrawlerProcess
from news_scraper.settings import MAX_PAGES

class nhadatvnSpider(scrapy.Spider):
    name = "nhadatvnSpider"
    allowed_domains = ["nhadatvn.com.vn"]
    start_urls = ["https://nhadatvn.com.vn/nha-dat-ban-kv-ha-noi.html"]
    num_page = 1
    max_pages = MAX_PAGES  # Set the maximum number of pages you want to scrape

    def parse(self, response):
        bds_links = response.css('.ten a::attr(href)').extract()
        for links in bds_links:
            url = links
            yield response.follow(url, callback=self.parse_bds_page)

        if bds_links and self.num_page <= self.max_pages:
            self.num_page += 1
            next_page_url = self.start_urls[0] + "?page=" + str(self.num_page)
            yield response.follow(next_page_url, callback=self.parse)

    def parse_bds_page(self, response):
        item = HousePriceScraperItem()
        item['html_content'] = response.text
        item['url'] = response.url
        yield item

if __name__ == "__main__":
    
    process = CrawlerProcess(settings={
        
        "FEEDS": {
            "cafef.csv": {"format": "csv"},
        },
        
    })
    
    process.crawl(nhadatvnSpider)
    process.start()