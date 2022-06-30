import random
import time
import selenium
import requests
from lxml import etree
import re

from requests import RequestException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions
# from retrying import retry
#
#
# @retry(wait_fixed=10, stop_max_attempt_number=1)
# def click(path):
#     driver.find_element(By.XPATH, path).click()

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
    'User-agent':random.choice(UserAgent_List)
}

option = webdriver.ChromeOptions()
option.add_argument("headless")
option.page_load_strategy = 'eager'
proxies = {'http': 'http://127.0.0.1:10809', 'https': 'http://127.0.0.1:10809'}
option.add_argument("--proxy-server=http://127.0.0.1:10809")
option.add_argument('--user-agent={}'.format(headers))
option.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path=r'E:\pycharmproject\chromedriver.exe', options=option)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})


def iselement(browser, path):
    try:
        browser.find_element(by=By.XPATH, value=path)
        return True
    except exceptions.NoSuchElementException:
        return False


def get_page(url):
    driver.get(url)
    print('chromedriver启动成功！')
    if iselement(driver, '//*[@id="sort-reviews-menu"]/button'):
        time.sleep(0.5)
        driver.find_element(by=By.XPATH, value='//*[@id="sort-reviews-menu"]/button').click()
        time.sleep(0.5)
        driver.find_element(by=By.XPATH, value='//*[@id="sort-reviews-menu"]/div/button[2]').click()
        time.sleep(1)  # 等待后，上一次点击的页面才能获取
        driver.switch_to.window(driver.window_handles[-1])
        return driver.page_source
    else:
        return 0


def click_to_last_page(path):
    last_page_button = driver.find_element(by=By.XPATH, value=path)
    last_page_button.click()
    time.sleep(0.5)  # 等待后，上一次点击的页面才能获取
    driver.switch_to.window(driver.window_handles[-1])
    return driver.page_source


def parse_original_page(html):
    global latest_review_time, earliest_review_time
    comment_info = []
    page_tree = etree.HTML(html)
    reviews_num = page_tree.xpath('//*[@id="reviews"]/div[1]/div/div[1]/h2/text()')[0].strip().replace(' ', '').replace('\n', '').replace('reviews', '').replace('shop', '').replace('review', '')
    item_reviews_num = page_tree.xpath('//*[@id="same-listing-reviews-tab"]/span/text()')
    if item_reviews_num:
        item_reviews_num = item_reviews_num[0].strip().replace(' ', '').replace('\n', '')
    else:
        item_reviews_num = ''

    # 判断有无评论
    if item_reviews_num != '':
        # 判断评论时间有无对应评论人
        if len(page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div[1]//p/text()')) > 1:
            print(page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div[1]//div[contains(@class,"wt-display-flex-xs wt-align-items-center")]/p/text()'))
            latest_review_time = page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div[1]//div[contains(@class,"wt-display-flex-xs wt-align-items-center")]/p[contains(@class,"wt-text-caption wt-text-gray")]/text()')[1].strip().replace('\n', '')
        else:
            latest_review_time = page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div[1]//div[contains(@class,"wt-display-flex-xs wt-align-items-center")]/p[contains(@class,"wt-text-caption wt-text-gray")]/text()')[0].strip().replace('\n', '')

        #判断是否有翻页
        if iselement(driver, '//*[@id="reviews"]/div[2]/nav/ul/li[2]/a'):
            li_list = page_tree.xpath('//*[@id="reviews"]/div[2]/nav/ul/li')
            if page_tree.xpath('//*[@id="reviews"]/div[2]/nav/ul/li[{}]/a/@href'.format(str(len(li_list)-1))) != '':
                last_page_path = '//*[@id="reviews"]/div[2]/nav/ul/li[{}]/a'.format(str(len(li_list) - 1))
                print('页标签：',len(li_list)-1,page_tree.xpath('//*[@id="reviews"]/div[2]/nav/ul/li[{}]/a/@href'.format(str(len(li_list)-1)))[0])
                try:
                    new_html = click_to_last_page(last_page_path)
                except selenium.common.exceptions.StaleElementReferenceException:
                    # time.sleep(2)
                    new_html = click_to_last_page(last_page_path)
                new_page_tree = etree.HTML(new_html)
                div_list = new_page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div')
                if len(new_page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div[{}]//p/text()'.format(str(len(div_list))))) >1:
                    earliest_review_time = new_page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div[{}]//div[contains(@class,"wt-display-flex-xs wt-align-items-center")]/p[contains(@class,"wt-text-caption wt-text-gray")]/text()'.format(str(len(div_list))))[1].strip().replace('\n', '')
                else:
                    earliest_review_time = new_page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div[{}]//div[contains(@class,"wt-display-flex-xs wt-align-items-center")]/p[contains(@class,"wt-text-caption wt-text-gray")]/text()'.format(str(len(div_list))))[0].strip().replace('\n', '')
        else:
            div_list = page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div')
            if len(page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div[{}]//p/text()'.format(str(len(div_list))))) > 1:
                earliest_review_time = page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div[{}]//div[contains(@class,"wt-display-flex-xs wt-align-items-center")]/p[contains(@class,"wt-text-caption wt-text-gray")]/text()'.format(str(len(div_list))))[1].strip().replace('\n', '')
            else:
                earliest_review_time = page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div[{}]//div[contains(@class,"wt-display-flex-xs wt-align-items-center")]/p[contains(@class,"wt-text-caption wt-text-gray")]/text()'.format(str(len(div_list))))[0].strip().replace('\n', '')
    else:
        latest_review_time=earliest_review_time= ''
        print('该商品暂无评论！')
    comment_item = [reviews_num, latest_review_time, earliest_review_time]
    comment_info.append(comment_item)
    print(comment_info)
    driver.delete_all_cookies()
    return comment_info


def write_to_file(content):
    with open('detail_info.txt', 'w', encoding='utf-8') as f:
        f.write(content)
        f.close()


# url = 'https://www.etsy.com/listing/552879987/canvas-shoes-trainers-kids-to-adults?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=&ref=sr_gallery-1-12'

def main(url):
    # url = 'https://www.etsy.com/listing/536493303/huaraches-mexican-shoes-for-her?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=&ref=sr_gallery-2-22&frs=1'
    html = get_page(url)
    if html != 0:
        return parse_original_page(html)
    else:
        print('该店铺及商品暂无评论！')
        return [['', '', '']]


# main(url)

