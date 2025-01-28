from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from medium_blog_scraper.spiders.blog_scraper_spider import BlogScraperSpider

# Get existing settings
settings = get_project_settings()

# Update the settings with the new FEEDS configuration for file output
settings.set('FEEDS', {
    'output.json': {
        'format': 'json',
        'indent': 4,
        'fields': ['search_term', 'title', 'subtitle', 'summary', 'tags', 'member_only',
                   'author', 'publication', 'claps', 'comments', 'publish_date', 'read_length', 'link'],
        'overwrite': True,
    },
})

# Create a CrawlerProcess with the updated settings
process = CrawlerProcess(settings)

# Add the spider to the process with parameters
process.crawl(
    BlogScraperSpider,
    keywords={
        "Artificial Intelligence": 10,
        "Machine Learning": 15,
        "Data Science": 5
    }
)

# Start the process
process.start()
