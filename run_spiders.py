'''xenForo Backup Scraper'''
import datetime
import os
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

STATUS_FILENAME = 'status.json'

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

def save_count(previous_count):
    '''Increment and save'''
    previous_count = int(previous_count) + 1
    with open(STATUS_FILENAME, 'w+') as json_file:
        json.dump({'run_count': previous_count}, json_file)

def update_count():
    '''Increment the run_count var so that we only download files every 5th backup.'''
    if os.path.isfile(STATUS_FILENAME):
        with open(STATUS_FILENAME) as json_file:
            data = json.load(json_file)
            run_count = data['run_count'] if data and data['run_count'] else 0
            json_file.close()
            save_count(run_count)
    else:
        json_file = open(STATUS_FILENAME, 'w+')
        json.dump({'run_count': 0}, json_file)

def main():
    '''Run the spiders'''
    process = CrawlerProcess(get_project_settings())
    process.crawl('backup_posts')
    process.crawl('backup_comments')
    process.crawl('backup_users')
    process.start()
    update_count()

main()
