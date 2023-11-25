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

DEPTH_LIMIT = 6000

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
    # 'house_price_scraper.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware': 200,
    'house_price_scraper.middlewares.ScrapeOpsProxyMiddleware': 250,
}
SCRAPEOPS_API_KEY = 'b8c5d96d-e82f-488e-b155-b433f278e029' # signup at https://scrapeops.io
SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = 'https://headers.scrapeops.io/v1/user-agents'
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 10
## settings.py

SCRAPEOPS_PROXY_ENABLED = True





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

# ---------- OLD FIREBASE KEY ----------
"""
firebase_key = {
  "type": "service_account",
  "project_id": "house-price-prediction-20231",
  "private_key_id": "f9ec162ae28eef699ab9cc47b3009230d9246047",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCX3+hcVhY6jb7p\nRQFYqvPheAIXJ3RSP0AxOJWBxYlExDgerU+y0uxvQWAl2hkWmcN590+UdPBPwLOG\nv9EtVg3ujYuIXQ/8VunyJHhbR9kkHR/cBz24N6BMzUZh+XA680+ZHQNS8X1FPMaj\n9RogvGM4ehrFOChjwboCuAGjAcsPuJj/WwWhMt6E/QYYvCrs0jABaYlxqQ4YTpbq\naLw9LQD9LX2FjK4Jtc+FoO4lkW+7ixx+QkC1pjuaj7L0/2b9TwlA3wfXN7iFvwsk\nymjI4c81bvgclQGGC15F61fEsEe//dBbbvyD0/nhXFWXeF9ZaICJ2O30g5uhggKg\nmA5fmnLVAgMBAAECggEAAVlFsPw6uk5j8aJhPq5V+ByeuCHrkIdrRISiH0Ln0yqC\n7RLQ8F+bJenIts1XB7JZ4A1oMYNQVwT5EytE6kgnW4T6Rj29VJpY/YOBZh4fOYjg\nrY2K6MXlsIjqJRiX/I4ImO1/CA+I80J06SPWFZBWuTusXTAAe9JOmpOTwCTV7s/L\nWydzLLUxtNlXy8B1ujuROOMqDHEfnFK9f5PqtQE4/ISQCGMzhKKiou2BK4gLQomE\n9+R85c+FTGMqICtQ50NxfvW66cHheodJfM+EbfUaGBqjDeSM9n0ibOFUIK/t3uNJ\nlH69CZLuv+PmN4zpmW+0I4GZ/eDCJxLW/Y2Qd7dlwQKBgQDKmS0pqlFZgmynrw3P\nrZ1mHDzkOwkQtKdZ2oRjANrLheBJ3N/De2Mbn2JZxbJSiGwe3+/nCJ4Ln8zO7+mF\nFIe20t7h3k/9E3tlpTCSPEfCwzL6fJJGR0OyySqAEV1NJoJLSzlUpmIQ62/hEeFN\n6ZRdMqemt9BtO35amKXxByi5WQKBgQC/6AYgg3mHoVUkv8gY9n/OGAdJA/cPOibg\njRH4D3xwhZNWbhIgSoRJpRUwgobLIS8LEq9A6YyJwH7tHDQzeAVyzVnvp58NFK00\n2cVHYpS/YTKvGLTwc4VJ1NWDPWp8cIF418RgeEouGNPGlAxyDZskkV5ddY1W8JMF\n/SUhLkbZ3QKBgFw5eDaUQm3VkjKO3GGibZkS16EpQoopQlkDwOn0dKTa72uQMQgi\nfc4QMswc030Afv9a/zETWiZ+etPkoE+lNdZCjZUSByV0HeL6XG7lI+GDzAv8cvWs\n8SNMsZ0Uyn0ZP4yY1KM1DkUXd5lj80TtRE1chra8zBM9VtpUzI04rhAZAoGAX4Mx\nmXkWQYTwhYvWIWZ+Easv5Q1OJ4v/0X8k1FuQycgRntDFwMCVurmpJC2yvOLVMSOp\nihszUVQ3V/fTm1I/E/ZUrsy0gqQp2MYSRAcylVXhDfi0BYDZc/e0FM+6chjkt6pc\nGM+FzA+bR5hj4VgYQUkAuG9LW1v9MNvfYPZRWRkCgYBQNqVrAxefObj1akEGdOx/\nicJANfc455/pVfXR93P2LSdRbxM30iWypaekaqN5kHntQJ8zwk+B2n5X4DkefPO3\nje+N17PlBkWrqiD2mxUTZFE/l7zXS4MbiKap2M5EfhV05QhV0OjAIdMB5brXcsxX\nPqhw8KibCtBVaSsyJt6OSg==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-akwfj@house-price-prediction-20231.iam.gserviceaccount.com",
  "client_id": "104204028462038712681",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-akwfj%40house-price-prediction-20231.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
""" 
# ---------- OLD FIREBASE KEY ----------

# ---------- NEW FIREBASE KEY ----------
firebase_key = {
  "type": "service_account",
  "project_id": "house-price-prediction-20231",
  "private_key_id": "caf093aa56fbbc94cae534c679d951a59e57d8ca",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCkII0M0o1tMHjR\n+/h2f56IZLizudUSGs99Sagyqpo5XB7f30pvm5n/Xf1OTG1CRFxdx0zDLTD7EIQp\nWQd0ojahcaryuOxH6jj4N6nJNLpoEMEE5q1R3dM6Llexzi39t763yPwLprnJvxVB\n7XrxL2ACHYQFGg60joVxfTebUD/f+P2MEA1zpf8KyRKKaSo143Zd6+6vuXjqFum7\nJJ2+6TiX3DXmLiatrzRLSwZX5ZQsOVZTBVvvQ9o5VejR8Ko0O25mAEHn4BQfbde/\nuj0Z2x0STsV5UkLKzDHmrBSN+o3bcOLxTwdKD/Qg5ZyaN530L4REUE2soMwDKITq\nZVRUCs3nAgMBAAECggEAEmNdOi8Kzk1sc+Y9h5Uzv0c9lFFBKHadgYVzlT2c6slB\n4kYjkk6GGeC/ZPrWEOMU0CLonENfZfmLPRCu76fO5BaWlvwV6Na6jEC8QoEoU0lx\nPqnTiEUIic+wXojhiTgBY5jeeDW1Qf+pE4pWSFhM8t+4r1OkiyEenUDwrnN2vJJ8\nYJ4z8SMV8TpSPr6SpgHY5KgA0UfuNlmdHbu97Xc8AqkCtRc0tjvuNDogrxVUF/KQ\nEHatEO5IlPE+spXgd1JqLiJziVTjuFBHk6b1+3iY7QZVpleGQ0nneU3wHyVh/ypc\n3ui8/PScDvJBOUftxexPlHHRBWlv8UauiNI4N6pb0QKBgQDY40Lt3+O4daA73pj+\nnbf+Gxov596xeFzx/I9oJWDbpIODJcBx+epGlKAICbWCWNFcWzEGKCIcdftpJDo1\nJOlIyEc9fhEEamloufaaZcnFBCqQ0FgACpCB71Q4kv0XeSayjX+IOZddZthbx34V\nHdmiSfuRzXQZz/i6/lJ80BfIMQKBgQDBuZGbGAUuCzjuEEjTfIn+Xv6H6O7ue9xm\nC/0+EJe9Vwa3dHof99JfEsDtSKBUlWjq2lwVOHwcupdDssh2qB+FqzqAdHZ71dxT\nIeqymrw0u3LkHVXL5qG2Te9M2sYyFKqpHqIxM/F8BJDdVUpvBkXKzQJq5/ZPnDts\nSm2hWxoJlwKBgEm0GSd7AQjLODOANp+3+zGoBiMneZ73lyZIvHcY1KxvYJ2ts5NH\n6Vwo36U7n2n3QtZOyv8bnlPrqA8X14v9yiUIomT8NU451y5Wm73mP0XrX4estWr2\nLBtruEQtd0KF0ie1PBSP9acw7u9pgKguZ6nl2E648e5fpVfuWxu9H4fRAoGBAJBo\nWQ7oz+urt+tWPkNQIbl5bHk5fOpPcFKte0BJtCMS/VHBxMuRu8LdQu1eZw3GNmhj\nD6NN8M6llN6FJgO1fZHxuvFIX44eNFfP/5jV2ZfhZ1p+N5eAO2mfHNQIfReV6kWZ\nLURKOSe+a5Jh4tNyNJJhUf0JHsXnazBlJuXR+E3PAoGBAMewzgQCFaMiqJUa1TGz\n3Qg97hYNDctvXxnOyo25ZLumFCdZu8WyCmR/Ujtubpt4h8SgBZHjBSLAmSYMsTGR\nZimDno8vTs69keyDW/tqNFdeMSPBqtr57Hjmc3FWcmHPctRg8Ofqmili0pJZi+/t\nuAzr8G9MmyRUxG1zRFsjWK7z\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-akwfj@house-price-prediction-20231.iam.gserviceaccount.com",
  "client_id": "104204028462038712681",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-akwfj%40house-price-prediction-20231.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
# ---------- NEW FIREBASE KEY ----------
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
