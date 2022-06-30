import requests
import re
from requests import RequestException
import pandas as pd
import time

proxies = {'http': 'http://127.0.0.1:10809', 'https': 'http://127.0.0.1:10809'}
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
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


def parse_original_page(html, page_num):
    filt = 'love(.*?)discover'
    filt_url = re.compile(filt, re.S).findall(html)[0]
    url_regex = 'data-palette-listing-image.*?href="(.*?)".*?data-listing-card-listing-image.*?src="(.*?)"'
    items = re.compile(url_regex, re.S).findall(filt_url)
    print(items)
    print(len(items))
    for item in items:
        yield {
            'page_num': page_num,
            'product_url': item[0],
            'product_picture': item[1]
        }


def write_to_file(name, content):
    save = pd.DataFrame(content)
    save.to_csv(name + ' product_url.csv', mode='a', header=None, index=False)


product_type = ["Women's Shoes", "Men's Shoes", "Storage & Organization", "Kitchen & Dining", "Lights & Ceiling Fans",
                "Backpacks", "Handbags", "luggage-and-travel", "Totes"]
url_list = ['https://www.etsy.com/c/shoes/womens-shoes?ref=pagination&page=',
            'https://www.etsy.com/c/shoes/mens-shoes?ref=pagination&page',
            'https://www.etsy.com/c/home-and-living/storage-and-organization?ref=pagination&page=',
            'https://www.etsy.com/c/home-and-living/kitchen-and-dining?ref=pagination&page=',
            'https://www.etsy.com/c/home-and-living/lights-and-ceiling-fans?ref=pagination&page=',
            'https://www.etsy.com/c/bags-and-purses/backpacks?ref=pagination&page=',
            'https://www.etsy.com/c/bags-and-purses/handbags?ref=pagination&page=',
            'https://www.etsy.com/c/bags-and-purses/luggage-and-travel?ref=pagination&page=',
            'https://www.etsy.com/c/bags-and-purses/totes?ref=pagination&page=']


def main(type_name, url_num):
    for i in range(10):
        print('开始采集第', i + 1, '页')
        url = url_list[url_num] + str(i)
        html = get_page(url)
        item = parse_original_page(html, i)
        write_to_file(type_name, item)
        print('第', i + 1, '页采集完成！')





# if __name__ == '__main__':
#     for i in range(10):
#         print('开始采集第', i + 1, '页')
#         main(i + 1)
#         print('第', i + 1, '页采集完成！')
#         time.sleep(3)
