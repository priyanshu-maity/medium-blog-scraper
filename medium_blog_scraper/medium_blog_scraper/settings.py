BOT_NAME = "medium_blog_scraper"

# Modules where spiders are located
SPIDER_MODULES = ["medium_blog_scraper.spiders"]
NEWSPIDER_MODULE = "medium_blog_scraper.spiders"

# Playwright settings for headless browsing
PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
}
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# Logging configuration
LOG_LEVEL = "INFO"

# Crawler behavior settings
ROBOTSTXT_OBEY = False  # Ignore robots.txt restrictions
CONCURRENT_REQUESTS = 5  # Maximum concurrent requests

# Retry strategy
RETRY_ENABLED = True
RETRY_TIMES = 3  # Number of retry attempts before giving up
RETRY_DELAY = 5  # Delay between retries in seconds
RETRY_BACKOFF = 2  # Exponential backoff multiplier for retries

# Request throttling
DOWNLOAD_DELAY = 1  # Delay between requests to prevent overloading the server

# Middleware configurations
DOWNLOADER_MIDDLEWARES = {
    "medium_blog_scraper.middlewares.RandomHeadersMiddleware": 543,  # Middleware for random headers
}

# Item pipelines for post-processing
ITEM_PIPELINES = {
   "medium_blog_scraper.pipelines.DataValidationPipeline": 300,  # Pipeline to validate and transform data
}

# Advanced Scrapy settings
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"  # Request fingerprinting for caching
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"  # Async reactor
REACTOR_THREADPOOL_MAXSIZE = 100  # Maximum size of the reactor thread pool

# Feed export settings
FEED_EXPORT_ENCODING = "utf-8"  # Encoding for exported data
