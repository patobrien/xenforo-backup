'''Backup Users'''
import scrapy
from ..items import UserItem
from ..helpers import get_images, get_selector, next_link, get_author_info, check_run_count

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

def get_users(res):
    '''Get users'''
    for row in res.css('.InlineModForm ol.messageList>li'):
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
    href = next_link(res.css('.pageNavLinkGroup .PageNav a.text'))
    if href and href:
        yield res.follow(href, get_users)

class BackupUsersSpider(scrapy.Spider):
    '''Start Scraping process'''

    name = 'backup_users'
    allowed_domains = ['bitco.in']
    start_urls = ['https://bitco.in/forum/']
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'data/backup_users.json',
        'ITEM_PIPELINES': {
            'forumbackup.pipelines.DuplicateUsersPipeline': 200,
        }
    }
    if check_run_count():
        custom_settings['ITEM_PIPELINES'] = {
            'scrapy.pipelines.images.ImagesPipeline': 100,
        }

    def post_list(self, res):
        '''Find post urls from category pages'''
        for post in res.css('.discussionList .discussionListItems .discussionListItem'):
            href = get_selector(post, '.main h3.title a::attr(href)')
            if href:
                yield res.follow(href, get_users)
        # follow pagination 'Next >' to additional post lists
        href = next_link(res.css('.afterDiscussionListHandle .PageNav a.text'))
        if href:
            yield res.follow(href, self.post_list)

    def parse(self, response):
        '''Initial spider parse. Loops through categories and subcategories'''
        for category in response.css('.mainContent ol.section li.level_1 ol.nodeList li.level_2'):
            href = category.css('.nodeText h3 a::attr(href)').get()
            if href:
                yield response.follow(href, self.post_list)
            # follow subcategories
            for subhref in category.css('ol.subForumList li h4 a::attr(href)'):
                yield response.follow(subhref, self.post_list)
