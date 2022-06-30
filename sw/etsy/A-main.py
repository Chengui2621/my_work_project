import os
import re
import time
from utils import get_detailinfo
from utils import get_comments
from utils import get_url
import datetime
import pandas as pd

now = datetime.datetime.strptime(str(time.strftime("%Y/%m/%d")), '%Y/%m/%d').date()
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


### 添加产品类别！！！
product_num = 8
current_type = product_type[product_num]


def write_to_file(content, path):
    content = pd.DataFrame(content)
    old_path = path + '.csv'
    if not os.path.exists(old_path):
        content.to_csv(old_path, mode='a', index=False)
    else:
        content.to_csv(old_path, mode='a', index=False, header=None)


# 采集url
def get_product_url(num):
    get_url.main(product_type[num], num)


# 采集信息
def get_data(num):
    url_df = pd.read_csv(product_type[num] + " product_url.csv", names=['page', 'product_url', 'product_picture'])
    # url_df = pd.read_excel(product_type[num] + " product_url.xlsx")
    product_url = pd.DataFrame(url_df)
    # columns = ['产品类别', '店铺名称', '店铺销售量', '产品标题', '产品图片0', '产品美元价格', '产品评论数', '店铺评论数0', '采集日期', '产品url', '产品图片']
    columns = ['产品类别', '店铺名称', '店铺销售量', '产品标题', '产品美元价格', '产品评论数', '店铺url', '店铺评论数', '最新评论日期', '最早评论日期', '采集日期', '产品url', '产品id', '产品图片']
    file_path = current_type + '商品数据'
    for i in range(1, 641, 1):
        url = product_url['product_url'][i-1]
        product_id = re.search(r'listing/(\d+?)/', url).group(1)
        picture = product_url['product_picture'][i-1]
        print(product_num, current_type ,'开始采集第', i, '/', str(len(product_url)), '条：')
        print(url)
        try:
            product_info = get_detailinfo.main(url)
            product_comment = get_comments.main(url)
        except:
            product_info = get_detailinfo.main(url)
            product_comment = [['错', '错', '错']]
        full_info = product_info[0]
        full_info.insert(0, current_type)
        full_info = full_info + product_comment[0]
        full_info.append(now)
        full_info.append(url)
        full_info.append(product_id)
        full_info.append(picture)
        full_info = pd.DataFrame(full_info)
        print(full_info)
        full_info = full_info.T
        full_info.columns = columns
        write_to_file(full_info, file_path)



# 重采评论日期
# def get_comment_data(num):
#     # url_df = pd.read_csv(product_type[num] + " product_url.csv", names=['page', 'product_url', 'product_picture'])
#     url_df = pd.read_excel(product_type[num] + " product_url.xlsx")
#     product_url = pd.DataFrame(url_df)
#     # columns = ['产品类别', '店铺名称', '店铺销售量', '产品标题', '产品图片0', '产品美元价格', '产品评论数', '店铺评论数0', '采集日期', '产品url', '产品图片']
#     columns = ['产品类别', '店铺评论数', '最新评论日期', '最早评论日期', '采集日期', '产品url', '产品图片']
#     file_path = current_type + '商品数据'
#     for i in range(219, 439, 1):
#         url = product_url['product_url'][i-1]
#         picture = product_url['product_picture'][i-1]
#         print('开始采集第', i, '/', str(len(product_url)), '条：')
#         print(url)
#         # try:
#         product_comment = get_comments.main(url)
#         # except:
#         #     product_comment = [['错', '错', '错']]
#         full_info = product_comment[0]
#         full_info.insert(0, current_type)
#         full_info.append(now)
#         full_info.append(url)
#         full_info.append(picture)
#         full_info = pd.DataFrame(full_info)
#         print(full_info)
#         full_info = full_info.T
#         full_info.columns = columns
#         write_to_file(full_info, file_path)


if __name__=='__main__':
    get_product_url(product_num)
    get_data(product_num)
    # get_comment_data(product_num)