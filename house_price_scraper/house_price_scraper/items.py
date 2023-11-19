# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HousePriceScraperItem(scrapy.Item):
    # define the fields for your item here like:
    html_content = scrapy.Field()
    url = scrapy.Field()
    progress_bar = scrapy.Field()

