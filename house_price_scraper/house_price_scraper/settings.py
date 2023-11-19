# Scrapy settings for house_price_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "house_price_scraper"

SPIDER_MODULES = ["house_price_scraper.spiders"]
NEWSPIDER_MODULE = "house_price_scraper.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "house_price_scraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
FEEDS = {
    'nhadatvn.csv': {'format':'csv', 'overwrite':True},
}
DEPTH_LIMIT =  6000

LOG_LEVEL = 'INFO'
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
#    "house_price_scraper.middlewares.HousePriceScraperSpiderMiddleware": 543,
    'house_price_scraper.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware': 200,
}
SCRAPEOPS_API_KEY = 'b8c5d96d-e82f-488e-b155-b433f278e029' # signup at https://scrapeops.io
SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = 'https://headers.scrapeops.io/v1/user-agents'
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 10

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "house_price_scraper.middlewares.HousePriceScraperDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "house_price_scraper.pipelines.HousePriceScraperPipeline": 300,
   "house_price_scraper.pipelines.FirebasePipeline": 400,
  #  "house_price_scraper.pipelines.ProgressBarPipeline":500,
}

firebase_key = {
  "type": "service_account",
  "project_id": "house-price-prediction-20231",
  "private_key_id": "04be6c75d5abdecfcb8adde8677c02be74d5dced",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDYDNC/AQrXhE50\nVxb6stq5eC1eXnnG2w72VSwjHZ2OF7CNi/+Wxx4pYd6uYgnxXI6TxorW1uw0fU27\nVQQTjSXNRQu/xfsvAWnVV9v3QMRJa+Hgw5nc6VjsQ5hscGH2ZgdFWcqSRriZdOGP\n090dvxG0TqgGd4rIJFtDlbffznKNziNymRd8bPphWHfSdJAZy1n5HNHDgDn0M9Xq\n8eJgy4doalcOKpvGBeEte3w56K2lfgAP7pnci8r0RhEOD7jdWcZ3SXBmCFgKR7d1\nmL4ALF28Gc7i9fKFOkdxClhPKmbgVDlXW244a2hjjODDWxJ21uOKOX6a4mdfBXG+\nE6ci1kKzAgMBAAECggEAWr2rMQXZjWIi52cqnhnflrVcbL3GbNhVpO1p78fBBEx7\n2T97FlNEHkJeWiSQI4Dp2zQw3QIAzBzyuGMBJssKHPhKcn3PPVNdJX9UwjjAGExI\n3vOYXHnfYMAVNTpQUsJQfHa1h5FPeBhoolVsEdHNuEqu9KRhtCTc9fpcc5IMd/Td\n3Dcut3K2jV6XQSoiPVnEPsKQU9x4sbNLXfUHppHOMmW2jh4pNOXUKMxwzGb9t+Ch\nS2DR272DTlwzsK7u3NFj48sowxIA0hlP6/+edXkipzdcc1eKN+JrlHA5Or0gCkwv\nnrF6tR1KxREZnF20PifJrMP48CXSBPoiVVimWjjQ3QKBgQD7f5fohoEONKspnHL4\n0hgX4ULBorNEV308VMni/umySddPanpG1lrMFxMw/0lpn+H6jo7HHj7lXgOYBPeb\nXUJ/Jkm9gb1phFo8n4imZXd0zjj4uyIptVtfPh1RuVz5kfVYdjk/y4mCeua5/YIB\ncDjAxXkn4BYRC+6Rptd1wtAoLQKBgQDb6sq61qPd//WA/mi4VYZ67ZZt33UY7wlW\nFgiyJBvenQKnjG5T9+mu67QQWWUJ/PwUbFl7lV7Gy1ZcgxZX024YtJVHFoITQSBP\ns88RgctkgFGSEwNPKtBmDKzFmmhUC/olVi3RMSGuh8zBjAAwGst3xjqN6IHw84yD\nmjpLMcMCXwKBgBa12OPYcYL04pfpVsB9SEuvvbV6mbGMLPTruydSWYwN+vFi7hPD\ne4N+ee8svlZZZ7CWevIkGw3fRXfOywUukLimnnYMZyxGFVfwGAjelMDpdl+PlnAp\nvkyFcWRV1r16nqsUUese2BX+PyOAbuLuXVGbA2vEYnm7mBly9XXe16kpAoGBAI9U\n9hDUODVGz+Hk7qfFxkJ0e2jdDVrU4Mbk0YIZmrh6qPI+yuGbYQkKwm8tdHcQFdPR\n0niDoCP8/yqInZVcThN4DxsoBls6RS7tSHZmnAPCxmdoUO3WP8FjXW/k9T5iGAUh\np/cCCKvSApfbAXxY2mgUILHA6n/6nIhhisDbi/gNAoGAbw23xFirYXyZxzYQxLKG\na1dJj64BsTjR1X6b785Xqm5DssAnPG9U0HILZ2lnR1YcVIZlhzs+m+QBylJr5Nvr\nUkpHwi7gXZQWWJhtMNWeYjRoyRDlT/En3hSdAkULL+u7lGZjHiXCdlRJyr1V1zPh\nd59KiNHUYumNXkNpPntwpvc=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-akwfj@house-price-prediction-20231.iam.gserviceaccount.com",
  "client_id": "104204028462038712681",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-akwfj%40house-price-prediction-20231.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
project_id = 'house-price-prediction-20231'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
