'''Backup Posts'''
import scrapy
from ..items import PostItem
from ..helpers import get_images, clean_markup, get_selector, \
next_link, get_post_id, get_author_info

def get_posts(res):
    '''Get post info'''
    post = PostItem()
    post['post_id'] = get_post_id(res)
    post['post_title'] = get_selector(res, '.titleBar h1::text')
    post['post_url'] = res.url
    post['post_category'] = get_selector(res, '.titleBar #pageDescription a::text')
    post['post_created'] = get_selector(res, '.titleBar .DateTime::attr(title)')
    post['post_author_info'] = get_author_info(res, '.titleBar a.username')
    images = get_images(res.css('.InlineModForm ol.messageList li .messageContent article'))
    if images:
        post['image_urls'] = images
    post['post'] = \
        clean_markup(get_selector(res.css('.InlineModForm ol.messageList li')[0], \
        '.messageContent article'))
    yield post

class BackupPostsSpider(scrapy.Spider):
    '''Start Scraping process'''

    name = 'backup_posts'
    allowed_domains = ['bitco.in']
    start_urls = ['https://bitco.in/forum/']
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'data/backup_posts.json',
    }

    def post_list(self, res):
        '''Find post urls from category pages'''
        for post in res.css('.discussionList .discussionListItems .discussionListItem'):
            href = get_selector(post, '.main h3.title a::attr(href)')
            if href:
                yield res.follow(href, get_posts)
        # follow pagination Next link to additional post lists
        href = next_link(res.css('.afterDiscussionListHandle .PageNav a.text'))
        if href:
            yield res.follow(href, self.post_list)

    def parse(self, response):
        '''Initial spider parse. Loops through categories and subcategories'''
        for category in response.css('.mainContent ol.section li.level_1 ol.nodeList li.level_2'):
            href = category.css('.nodeText h3 a::attr(href)').get()
            if href:
                yield response.follow(href, self.post_list)

            for subhref in category.css('ol.subForumList li h4 a::attr(href)'):
                yield response.follow(subhref, self.post_list)
