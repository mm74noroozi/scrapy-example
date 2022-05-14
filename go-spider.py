from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from dohamdam.spiders.main import QuotesSpider


process = CrawlerProcess(get_project_settings())
process.crawl(QuotesSpider)
process.start()