import random
import time
import re
from datetime import datetime
import pandas as pd
import requests
from requests import RequestException
from lxml import etree


now = time.strftime("%Y/%m/%d")
proxies = {'http': 'http://127.0.0.1:10809', 'https': 'http://127.0.0.1:10809'}
UserAgent_List = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
]
headers = {
    'User-agent': random.choice(UserAgent_List)
}


def get_page(url):
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        return response.text
    except RequestException:
        return None


def get_comment(url):
    blog_page = get_page(url)
    # print(url)
    detail_tree = etree.HTML(blog_page)
    post_time = detail_tree.xpath('.//div[@class="author-by-line"]/div/p/text()')[0]
    # print(post_time)
    # print(detail_tree.xpath('//*[@id="comments"]/div/div[@class="embedded-forum-wrapper"]'))
    if detail_tree.xpath('//*[@id="comments"]/div/div[@class="embedded-forum-wrapper"]'):
        data_forum_id = detail_tree.xpath('//*[@id="comments"]/div/div[@class="embedded-forum-wrapper"]/@data-forum-id')[0]
        data_forum_thread_id = detail_tree.xpath('//*[@id="comments"]/div/div[@class="embedded-forum-wrapper"]/@data-forum-thread-id')[0]
        comment_url = 'https://www.etsy.com/api/v3/ajax/public/forums/{}/threads/%20{}'.format(data_forum_id, data_forum_thread_id)
        print('comment_url', comment_url)
        comment_page = get_page(comment_url)
        post_count = int(re.findall(r'post_count.*?(\d+?),', comment_page)[0])
        # print(post_count)
        return [post_time, post_count]
    else:
        post_count = 0
        return [post_time, post_count]


def parse_first_page(html):
    detail_tree = etree.HTML(html)
    product_info_list = []
    first_title = detail_tree.xpath('//*[@id="content"]/div[3]/div/div[1]/p[1]/a/text()')[0]
    first_url = 'https://www.etsy.com' + detail_tree.xpath('//*[@id="content"]/div[3]/div/div[1]/p[1]/a/@href')[0]
    blog_comment_first_time = get_comment(first_url)[0]
    blog_comment_first_count = get_comment(first_url)[1]
    product_info_list.append([first_title, first_url, blog_comment_first_time, blog_comment_first_count])
    blog_tree = detail_tree.xpath('//*[@id="content"]/div[4]/div')
    for div in blog_tree:
        if blog_tree.index(div) == 6:
            blog_title = div.xpath('.//p[contains(@class, "wt-text-heading-02 wt-text-black wt-pb-xs-2 wt-pt-xs-2 article-title")]/a/text()')[0]
            blog_url = 'https://www.etsy.com' + div.xpath('.//p[contains(@class, "wt-text-heading-02 wt-text-black wt-pb-xs-2 wt-pt-xs-2 article-title")]/a/@href')[0]
            blog_comment_time = get_comment(blog_url)[0]
            blog_comment_count = get_comment(blog_url)[1]
            print(blog_title, blog_url, blog_comment_time, blog_comment_count)
            product_info_list.append([blog_title, blog_url, blog_comment_time, blog_comment_count])
        else:
            blog_title = div.xpath('.//a[@class="wt-text-link-no-underline"]/p/text()')[0]
            blog_url = 'https://www.etsy.com' + div.xpath('.//a[@class="wt-text-link-no-underline"]/@href')[0]
            blog_comment_time = get_comment(blog_url)[0]
            blog_comment_count = get_comment(blog_url)[1]
            print(blog_title, blog_url, blog_comment_time, blog_comment_count)
            product_info_list.append([blog_title, blog_url, blog_comment_time, blog_comment_count])
    return product_info_list


def parse_next_page(html):
    detail_tree = etree.HTML(html)
    product_info_list = []
    blog_tree = detail_tree.xpath('//*[@id="content"]/div')
    for div in blog_tree:
        if blog_tree.index(div) == 0 or blog_tree.index(div) == 7:
            blog_title = div.xpath('.//p[contains(@class, "wt-text-heading-02 wt-text-black wt-pb-xs-2 wt-pt-xs-2 article-title")]/a/text()')[0]
            blog_url = 'https://www.etsy.com' + div.xpath('.//p[contains(@class, "wt-text-heading-02 wt-text-black wt-pb-xs-2 wt-pt-xs-2 article-title")]/a/@href')[0]
            blog_comment_time = get_comment(blog_url)[0]
            blog_comment_count = get_comment(blog_url)[1]
            print(blog_title, blog_url, blog_comment_time, blog_comment_count)
            product_info_list.append([blog_title, blog_url, blog_comment_time, blog_comment_count])
        else:
            blog_title = div.xpath('.//a[@class="wt-text-link-no-underline"]/p/text()')[0]
            blog_url = 'https://www.etsy.com' + div.xpath('.//a[@class="wt-text-link-no-underline"]/@href')[0]
            blog_comment_time = get_comment(blog_url)[0]
            blog_comment_count = get_comment(blog_url)[1]
            print(blog_title, blog_url, blog_comment_time, blog_comment_count)
            product_info_list.append([blog_title, blog_url, blog_comment_time, blog_comment_count])
    return product_info_list


def write_to_file(content, type):
    data = pd.DataFrame(content, columns=['博客标题', '博客url', '发博时间', '评论数'])
    data['发博时间'] = data['发博时间'].apply(lambda x: datetime.strptime(x, "%b %d, %Y").date())
    data['采集日期'] = datetime.strptime(str(now), '%Y/%m/%d').date()
    data.to_excel('blog_data' + type + str(time.strftime("%Y-%m-%d")) + '.xlsx', index=False)


def set_url_home_and_living(page_type, page=1):
    if page_type == 'first':
        url0 = 'https://www.etsy.com/blog/category/home-and-living?ref=blog'
        return url0
    else:
        url = 'https://www.etsy.com/blog/paginated-articles/{}?category=home-and-living'.format(page)
        return url


def set_url_shopping_guides(page_type, page=1):
    if page_type == 'first':
        url0 = 'https://www.etsy.com/blog/category/shopping-guides?ref=blog'
        return url0
    else:
        url = 'https://www.etsy.com/blog/paginated-articles/{}?category=shopping-guides'.format(page)
        return url


def set_url_gift_ideas(page_type, page=1):
    if page_type == 'first':
        url0 = 'https://www.etsy.com/blog/category/gift-ideas?ref=blog'
        return url0
    else:
        url = 'https://www.etsy.com/blog/paginated-articles/{}?category=gift-ideas'.format(page)
        return url


def set_url_weddings(page_type, page=1):
    if page_type == 'first':
        url0 = 'https://www.etsy.com/blog/category/weddings?ref=blog'
        return url0
    else:
        url = 'https://www.etsy.com/blog/paginated-articles/{}?category=weddings'.format(page)
        return url


def set_url_style(page_type, page=1):
    if page_type == 'first':
        url0 = 'https://www.etsy.com/blog/category/style?ref=blog'
        return url0
    else:
        url = 'https://www.etsy.com/blog/paginated-articles/{}?category=style'.format(page)
        return url


def main():
    page_type = ['first', 'next']
    product_detail_info = []
    url_func = set_url_weddings
    for type in page_type:
        if type == 'first':
            url = url_func(type)
            print(url)
            data_info = parse_first_page(get_page(url))
            print(data_info)
            product_detail_info = data_info
            print(product_detail_info)
        else:
            for i in range(23):
                print('第', i+1, '页')
                url = url_func(type, i+1)
                print(url)
                data_info = parse_next_page(get_page(url))
                if len(data_info) > 0:
                    product_detail_info += data_info
                else:
                    continue
                print(product_detail_info)
                # return product_detail_info
    write_to_file(product_detail_info, 'weddings')
    # return product_detail_info
    # url = set_url(page_type)
    # html = get_page(url)
    # data_info = parse_first_page(html)

main()
