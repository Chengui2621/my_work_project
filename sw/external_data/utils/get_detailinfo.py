import random
import time
import re
import requests
from requests import RequestException
from lxml import etree

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
        if response.status_code == 200:
            print('连接成功')
            return response.text
        return None
    except RequestException:
        return None


def parse_original_page(html):
    detail_tree = etree.HTML(html)
    product_info_list = []
    if len(detail_tree.xpath('//*[@id="listing-page-cart"]//a[@class="wt-text-link-no-underline"]/span/text()'))>0:
        shop_name = detail_tree.xpath('//*[@id="listing-page-cart"]//a[@class="wt-text-link-no-underline"]/span/text()')[
            0].strip().replace('\n', '')
    else:
        shop_name = ''
    if len(detail_tree.xpath(
            '//*[@id="listing-page-cart"]/div[1]/div/div/div/span[@class="wt-text-caption"]/text()')) > 0:
        sales = \
            detail_tree.xpath('//*[@id="listing-page-cart"]/div[1]/div/div/div/span[@class="wt-text-caption"]/text()')[
                0].strip().replace(' ', '').replace('\n', '').replace('sales', '').replace(',', '').replace('sale', '')
    else:
        sales = ''
    if len(detail_tree.xpath('//*[@id="listing-page-cart"]/div[2]/h1/text()')) > 0:
        product_name = detail_tree.xpath('//*[@id="listing-page-cart"]/div[2]/h1/text()')[0].strip().replace('\n', '')
    else:
        product_name = ''
    # # 产品图片
    # if len(detail_tree.xpath('//*[@id="listing-right-column"]/div/div[1]/div[1]/div/div/div/div/div[1]/ul/li[1]/img/@src'))>0:
    #     product_picture = detail_tree.xpath('//*[@id="listing-right-column"]/div/div[1]/div[1]/div/div/div/div/div[1]/ul/li[1]/img/@src')[0]
    # else:
    #     product_picture = ''
    if len(detail_tree.xpath('//*[@id="listing-page-cart"]/div[3]/div[1]/div[1]/div[1]/div/div[1]/p[1]//text()')) > 1:
        print(detail_tree.xpath('//*[@id="listing-page-cart"]/div[3]/div[1]/div[1]/div[1]/div/div[1]/p[1]//text()'))
        name_score_list_string = ",".join(detail_tree.xpath('//*[@id="listing-page-cart"]/div[3]/div[1]/div[1]/div[1]/div/div[1]/p[1]//text()'))
        score_list = re.findall(r"\d+.*?\d+", name_score_list_string)
        product_price = score_list[0]
    elif len(detail_tree.xpath('//*[@id="listing-page-cart"]/div[3]/div[1]/div[1]/div[1]/div/div[1]/p[1]//text()')) == 1:
        product_price = \
            detail_tree.xpath('//*[@id="listing-page-cart"]/div[3]/div[1]/div[1]/div[1]/div/div[1]/p[1]//text()')[
                0].strip().replace(' ', '').replace('\n', '').replace('$', '').replace('+', '')
    else:
        product_price = '采集有误！'
    item_reviews = detail_tree.xpath('//*[@id="same-listing-reviews-tab"]/span/text()')
    # shop_reviews = detail_tree.xpath('//*[@id="shop-reviews-tab"]/span/text()')
    only_shop_reviews = detail_tree.xpath('//*[@id="reviews"]/div[1]/div/div[1]/h2/text')
    if item_reviews:
        item_reviews = item_reviews[0].strip().replace(' ', '').replace('\n', '')
    else:
        item_reviews = ''
    # if shop_reviews:
    #     shop_reviews = shop_reviews[0].strip().replace(' ', '').replace('\n', '')
    # else:
    #     shop_reviews = ''
    shop_url = 'https://www.etsy.com/shop/' + shop_name
    product_info_list.append(shop_name)
    product_info_list.append(sales)
    product_info_list.append(product_name)

    # product_info_list.append(product_picture)
    product_info_list.append(product_price)
    product_info_list.append(item_reviews)
    product_info_list.append(shop_url)
    return product_info_list


def write_to_file(content):
    with open('detail_info.txt', 'w', encoding='utf-8') as f:
        f.write(content)
        f.close()

# url = 'https://www.etsy.com/listing/559423145/red-leather-hobo-bag-big-hobo-bag-large?click_key=134e73afaedf2fa8b6816affa82a058426cb5fd0%3A559423145&click_sum=634f7d42&ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=&ref=sr_gallery-8-31&pro=1&frs=1'

def main(url):
    # url = 'https://www.etsy.com/listing/472207308/grey-crossbody-felt-purse-felt-bag?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=&ref=sr_gallery-1-8&pro=1&frs=1'
    html = get_page(url)
    product_detail_info = []
    data_info = parse_original_page(html)
    product_detail_info.append(data_info)
    print(product_detail_info)
    return product_detail_info


# main(url)
url = 'https://www.etsy.com/blog/category/home-and-living?ref=blog'
print(get_page(url))

