'''Spider Helpers'''
IMG_DOMAIN = 'https://bitco.in/forum/'

def fix_image_url(img):
    '''Fix relative download links'''
    if 'http' not in img:
        return IMG_DOMAIN + img
    return img

def get_images(res):
    '''Download images through image pipeline'''
    images = res.css('img::attr(src)').getall()
    if images:
        return [fix_image_url(img) for img in images]
    return None

def clean_markup(markup):
    '''Remove \r and \n from markup before saving'''
    markup = markup.replace('\r', '').replace('\n', '').replace('\t', '')
    return markup

def get_selector(response, selector):
    '''General getter with fallback'''
    value = response.css(selector).get()
    if value:
        return value
    return None

def check_conditions(link):
    '''Check conditions for generator'''
    return link and not isinstance(link, str) and link.css('::text').get() == 'Next >'

def next_link(res):
    '''Get next link'''
    if res:
        links = [link for link in res if check_conditions(link)]
        if links:
            href = links[0].css('::attr(href)').get()
            if href:
                return href
    return None

def get_post_id(res):
    '''Gets post id from the url string'''
    all_links = res.css('.titleBar #pageDescription a::attr(href)').getall()
    if all_links:
        last_link = all_links[len(all_links)-1]
        if '.' in last_link:
            pid = last_link.replace('/', '').split('.')
            if pid and pid[1]:
                return int(pid[1])
    return None

def get_author_info(res, sel):
    '''Get author info'''
    selector = res.css(sel)
    author_href = get_selector(selector, '::attr(href)')
    if author_href:
        name_long = get_selector(selector, '::text')
        name = author_href.split('/')[1].split('.')
        if name and name[0] and name[1] and name_long:
            return {
                'user_id': int(name[1]),
                'user_name': name[0],
                'user_link': author_href,
                'user_name_long': name_long,
            }
    return None
