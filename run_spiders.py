'''xenForo Backup Scraper'''
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# todo: save files to timestamped folder

PROCESS = CrawlerProcess(get_project_settings())
PROCESS.crawl('backup_posts')
PROCESS.crawl('backup_comments')
PROCESS.crawl('backup_users')
PROCESS.start()
