# Real-Estate-Price-Prediction

## Documentation

### Running the Crawler

To run the crawler, follow these steps:

1. Navigate to the `house_price_scraper` directory using the command: `cd house_price_scraper`
2. Run the crawler using the command: `scrapy crawl {spider_name}`
3. Ensure that you have set the appropriate extraction logic, start page index to crawl, link, name of the collection in Firebase, DEPTH_LIMIT (max pages) in `settings.py`, name of output file like `nhadatvn.csv`(uncomment in `settings.py` to export) and a new name log file (sometime need to reset) for your own spider.

Note: The `test.py` file can be used to check the URL and HTML content existence. The output will be saved in `output.html`.

### Accessing the data

To access the data, follow these steps:

1. Make a copy of the get_data_nhadatvn.py file
2. Follow the comments to make changes where necessary. You can make all file names standardized by following the example done on nhadatvn.
3. Implement the correct scraping logic for your webpage.
4. While running, if an error occurs, MAKE SURE TO MAKE THESE TWO CHANGES BEFORE RUNNING THE FILE AGAIN
   * Change `last_processed_identifier` to the url of the final page processed.
   * Change `idx_offset` to the final index in the log file, plus 1.
   * Obtain these information in the log file