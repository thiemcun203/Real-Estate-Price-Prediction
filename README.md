# Real-Estate-Price-Prediction

## Documentation

### Running the Crawler

To run the crawler, follow these steps:

1. Navigate to the `house_price_scraper` directory using the command: `cd house_price_scraper`
2. Run the crawler using the command: `scrapy crawl {spider_name}`
3. Ensure that you have set the appropriate extraction logic, start page index to crawl, start link, DEPTH_LIMIT (max pages) in `settings.py`, name of output file like `nhadatvn.csv`(uncomment in Spider file to export) and a new name log file (sometime need to reset) for your own spider.

Note: The `test.py` file can be used to check the URL and HTML content existence. The output will be saved in `output.html`.
With alonhadatvnSpider, please uncomment `'house_price_scraper.middlewares.ScrapeOpsProxyMiddleware': 250,` in `settings.py`. Other spiders is just need 


