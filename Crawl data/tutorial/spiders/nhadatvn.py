# https://nhadatvn.com.vn/ban-nha-mat-tien-kv-ha-noi.html
# https://nhadatvn.com.vn/ban-nha-ngo-hem-kv-ha-noi.html
import scrapy
from scrapy.crawler import CrawlerProcess
#define each spider for each news website
class CafefSpider(scrapy.Spider):
    name = "cafef"
    def start_requests(self):
        print(1)
        URL = 'https://cafef.vn/thi-truong-chung-khoan/5/10/2023.chn'
        yield scrapy.Request(url=URL, callback=self.response_parser)

    def response_parser(self, response):
        # print(response.xpath('/html/body/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/div/h3/a/').extract())
        yield response.xpath('/html/body/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/div/h3/a').extract()
        
if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "items.json": {"format": "json"},
        },
    })

    process.crawl(CafefSpider)
    process.start()
    