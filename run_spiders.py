'''xenForo Backup Scraper'''
import datetime
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def get_data_dir():
    '''Get the data directory'''
    parent_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))
    return os.path.join(parent_dir, 'data')

def cleanup():
    '''Cleanup backup files'''
    full_data_dir = get_data_dir()
    os.system('rm -rf ' + full_data_dir)

def get_zipfile_name():
    '''Get zipfile name'''
    return datetime.datetime.now().strftime("%Y-%d-%d_%H-%M-%S") + '.zip'

def zip_files():
    '''Compress backup in a zip'''
    zip_command = 'zip -r backups/' + get_zipfile_name() + ' data'
    if zip_command:
        print('Zipping: ', zip_command)
        os.system(zip_command)
        cleanup()

def main():
    '''Run the spiders'''
    process = CrawlerProcess(get_project_settings())
    process.crawl('backup_posts')
    process.crawl('backup_comments')
    process.crawl('backup_users')
    process.start()
    zip_files()

main()
