'''Testing'''
import scrapy
from ..items import UserItem
from ..helpers import get_images, get_author_info, next_link

def get_extra_user_info(res):
    '''Get extra user info'''
    info = {}
    for d_l in res.css('.extraUserInfo dl'):
        d_t = d_l.css('dt::text').get()
        d_sel = d_l.css('dd')
        d_text = d_sel.css('::text').get()
        d_d_a = d_sel.css('a::text').get()
        if d_t:
            info[d_t] = d_d_a if d_d_a else d_text
    return info

class BackupUsersTestSpider(scrapy.Spider):
    '''Start Scraping process'''

    name = 'test'
    allowed_domains = ['bitco.in']
    start_urls = ['https://bitco.in/forum/threads/buip124-new-members-for-election-13.23917/']
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'test.json',
    }

    def parse(self, response):
        '''Initial spider parse. Loops through categories and subcategories'''
        for row in response.css('.InlineModForm ol.messageList>li'):
            user_selector = row.css('.messageUserInfo')
            user = UserItem()
            # Get user info
            user_info = get_author_info(user_selector, '.userText a.username')
            if user_info and user_info['user_id']:
                user['user_id'] = user_info['user_id']
            if user_info and user_info['user_name']:
                user['user_name'] = user_info['user_name']
            if user_info and user_info['user_link']:
                user['user_link'] = user_info['user_link']
            if user_info and user_info['user_name_long']:
                user['user_name_long'] = user_info['user_name_long']
            # Get user avatar
            avatar = get_images(row.css('.avatarHolder .avatar'))
            if avatar:
                user['image_urls'] = avatar
            # Get user extra info, looping through dd and dt items
            extra_info = get_extra_user_info(user_selector)
            if extra_info:
                user['user_extra_info'] = extra_info
            yield user
        # follow pagination 'Next >' to additional comments
        href = next_link(response.css('.pageNavLinkGroup .PageNav a.text'))
        if href and href:
            yield response.follow(href, self.parse)
