'''
Scrapy Models
'''
import scrapy

class PostItem(scrapy.Item):
    '''Posts'''
    post_id = scrapy.Field()
    post_title = scrapy.Field()
    post_url = scrapy.Field()
    post_category = scrapy.Field()
    post_created = scrapy.Field()
    post_author_info = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
    post = scrapy.Field()

class CommentItem(scrapy.Item):
    '''Comments'''
    post_id = scrapy.Field()
    comment_number = scrapy.Field()
    comment_author = scrapy.Field()
    comment_date = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
    comment = scrapy.Field()

class UserItem(scrapy.Item):
    '''Users'''
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    user_name_long = scrapy.Field()
    user_link = scrapy.Field()
    user_extra_info = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
