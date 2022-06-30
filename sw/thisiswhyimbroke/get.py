import re
import datetime
import requests
import os
import pandas as pd
import time
import random
import urllib3
import logging

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
    'cookie': '_ga=GA1.2.1257227822.1654658564; _gid=GA1.2.1709850730.1654658564; visited=1; subtag_session_v2=%7B%22referrer%22%3A%22direct%22%2C%22session_type%22%3A%22first%20time%22%7D; _fbp=fb.1.1654658565609.283234806; session_id_v2=116708800; user_id=50215190; __gads=ID=3928b81deeb8967b-223ab4e3d0d30047:T=1654658514:RT=1654658514:S=ALNI_Ma3nBOIP0VFFfWgOnMQ_G89pg3bqw; __gpi=UID=000006736d209a7f:T=1654658514:RT=1654658514:S=ALNI_MZ3TjsLfDe6131gA5AzhaLPFk94gg; nsfw=0; _gat=1',
    'User-agent': random.choice(UserAgent_List)
}
params = {
    'max': '200',
    'min': '20'
    # 'country': 'cn',
    # 'store': 'all'
}

original_data_path = './采集结果/原始数据/'
final_data_path = './采集结果/导入数据/'
dir_list = [original_data_path, final_data_path]


# 批量创建文件夹
def create_dir(dir_list):
    for output_dir in dir_list:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)


def get_page(url):
    logging.captureWarnings(True)
    response = requests.get(url, headers=headers, proxies=proxies, json=params, verify=False)
    if response.status_code == 200:
        print('连接成功')
        response.encoding = 'utf-8'
        return response.json()
    return '连接失败'


def parse_html(html, product_type):
    item = {}
    item_content = pd.DataFrame()
    post_content = html['posts']
    for one in post_content:
        item['产品类别'] = product_type
        item['产品id'] = str(one['id'])
        item['产品标题'] = one['title']
        item['slug'] = one['slug']
        item['产品描述'] = one['content'].replace('\n', '')
        item['产品美元价格'] = one['price']
        item['产品图片'] = one['image']
        # item['large_image'] = one['large_image']
        item['发布日期'] = datetime.datetime.strptime(re.sub('T.*', '', one['published']).replace('-', '/'), '%Y/%m/%d')
        item['点赞数'] = str(one['saves'])
        item['产品链接'] = one['link']
        item['产品外链'] = 'https://www.thisiswhyimbroke.com/search/' + re.sub(' ', '%20', one['title'])
        item['排序方式'] = one['sort']
        item['采集日期'] = datetime.datetime.strptime(str(now), '%Y/%m/%d').date()
        item_content = item_content.append(item, ignore_index=True)
    return item_content


# 导出数据
def write_to_file(content):
    path = original_data_path + '商品信息' + str(time.strftime("%Y-%m-%d")) + '.xlsx'
    content.to_excel(path, index=False)
    # 筛选需要的列导出最终数据
    final_path = final_data_path + '导入数据' + str(time.strftime("%Y-%m-%d")) + '.xlsx'
    original_data = pd.read_excel(path)
    header = ['产品类别', '产品id', '产品标题', '产品描述', '产品美元价格', '点赞数', '发布日期','产品图片', '产品链接', '产品外链','排序方式', '采集日期']
    input_data = original_data[header]
    input_data.to_excel(final_path, index=False)


def url_select(order_num, page_num):
    url_list = [
        'https://www.thisiswhyimbroke.com/api/lists/new/{}/?max=200&min=20&country=cn&store=all'.format(page_num),
        'https://www.thisiswhyimbroke.com/api/lists/popular/{}/?max=200&min=20&country=cn&store=all'.format(page_num),
        'https://www.thisiswhyimbroke.com/api/gifts/gifts-for-men/new/{}/?max=200&min=20&country=cn'.format(page_num),
        'https://www.thisiswhyimbroke.com/api/gifts/gifts-for-men/popular/{}/?max=200&min=20&country=cn'.format(page_num),
        'https://www.thisiswhyimbroke.com/api/gifts/gifts-for-women/new/{}/?max=200&min=20&country=cn'.format(page_num),
        'https://www.thisiswhyimbroke.com/api/gifts/gifts-for-women/popular/{}/?max=200&min=20&country=cn'.format(page_num),

        'https://www.thisiswhyimbroke.com/api/gifts/gifts-for-mom/new/{}/?&max=200&min=20'.format(page_num),
        'https://www.thisiswhyimbroke.com/api/gifts/gifts-for-mom/popular/{}/?&max=200&min=20'.format(page_num)
        ]
    return url_list[order_num]



# 选择排序方式
# order_type_list = ['popular', 'newest']
product_type = ['首页', 'men', 'women', 'mom']


def main():
    global final_data, final_data_df
    create_dir(dir_list)
    final_data_df = pd.DataFrame()
    for url_num in range(8):
        if url_num in [0, 2, 4, 6]:
            type = product_type[int(url_num/2)]
        else:
            type = product_type[int((url_num-1)/2)]
        print(type)
        for i in range(25):
            print('开始采集第', i + 1, '页')
            url = url_select(url_num, i+1)
            print(url)
            page = get_page(url)
            final_data = parse_html(page, type)
            final_data_df = final_data_df.append(final_data)
        print(len(final_data_df), final_data_df)
    write_to_file(final_data_df)


main()
