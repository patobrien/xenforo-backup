'''Backup Comments'''
import scrapy
from ..items import CommentItem
from ..helpers import get_images, clean_markup, get_selector, \
next_link, get_post_id, get_author_info, check_run_count

def get_comment_number(res):
    '''Get the comment number'''
    comment_number = get_selector(res, '.messageInfo .messageDetails .postNumber::text')
    if comment_number:
        comment_number = int(comment_number.replace('#', ''))
        return comment_number
    return None

def get_comments(res):
    '''Get post data and comments'''
    for comment_row in res.css('ol.messageList>li'):
        comment = CommentItem()
        comment['post_id'] = get_post_id(res)
        comment['comment_number'] = get_comment_number(comment_row)
        comment['comment_author'] = get_author_info(comment_row, \
            '.messageUserInfo .messageUserBlock a.username')
        comment['comment_date'] = get_selector(comment_row, \
            '.messageInfo .messageDetails .DateTime::attr(title)')
        images = get_images(comment_row.css('.messageInfo article'))
        if images:
            comment['image_urls'] = images
        comment['comment'] = clean_markup(get_selector(comment_row, '.messageInfo article'))
        yield comment
    # follow pagination 'Next >' to additional comments lists
    href = next_link(res.css('.pageNavLinkGroup .PageNav a.text'))
    if href:
        yield res.follow(href, get_comments)

class BackupCommentsSpider(scrapy.Spider):
    '''Start Scraping process'''

    name = 'backup_comments'
    allowed_domains = ['bitco.in']
    start_urls = ['https://bitco.in/forum/']
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'data/backup_comments.json',
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
                yield res.follow(href, get_comments)
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
