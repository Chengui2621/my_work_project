import random
import time
import selenium
import requests
from lxml import etree
import json
from hyper.contrib import HTTP20Adapter
import httpx

proxies = {'HTTP://': 'http://127.0.0.1:10809', 'HTTPS://': 'https://127.0.0.1:10809'}
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
    'user-agent': random.choice(UserAgent_List),
    ":authority":"www.etsy.com",
    ":method":"POST",
    ":path":"/api/v3/ajax/bespoke/member/neu/specs/reviews",
    ":scheme":"https",
    # "accept":"*/*",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"zh-CN,zh;q=0.9",
    "content-length":"708",
    "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
    "cookie":"user_prefs=z32lFDFzOgGWQmQb79N2H036MFtjZACCpNpvujA6Wik02EVJJ680J0dHKTVPNzRYSUcJRIBFjCAULiKWAQA.; fve=1652422189.0; ua=531227642bc86f3b5fd7103a0c0b4fd6; ku1-vid=8f2500c6-560c-bbe3-f41f-67e0112980be; _gcl_au=1.1.1420846768.1652422234; __pdst=4607a618dd2546deb5fb9588941c0c93; _pin_unauth=dWlkPU1UZGlORGM1Tm1VdE1UYzBOUzAwWlRVekxUaGlOekV0WVdZMFlqUmxOR0V3TmpJNQ; _ga_KR3J610VYM=GS1.1.1653025816.32.1.1653038049.60; search_history_v2=r4A6_VpDvdkUkBZCmV7pjBwDLDRjZACCpEXz1sPoaqXi1MSi5IzUYiWr6GqlwtLUokolKyVHH88wV4WQ0qK8pNTSktQcJR2lkszc1PjiksTcAiUrQzNTEwsjEzMjYx2ljMTi-KLU4tKcEqARJUWlqbWxtQwA; lp_primary_nudge_order=quantity_only%2Cin_cart_only%2Ccombo_cart_and_quantity%2Crare_find_and_cart_combo%2Calmost_gone_and_cart_combo%2Conly_one_available; lp_secondary_nudge_order=%7B%22region_order%22%3A%5B1%2C0%2C2%5D%2C%22secondary_order%22%3A%5B1%2C3%2C4%2C2%2C0%5D%7D; uaid=AVHrjxgy3DYtJ95GliuxsNzaDW1jZACCpNpvumB6g2N3tVJpYmaKkpWST0Cgj0eURV6Kc0BFRHJESnphcamZr29FYb57oFItAwA.; ku1-sid=JieH03jW7w64aH47pH-hP; _gid=GA1.2.922672176.1655961162; granify.new_user.qivBM=true; _uetsid=ebd0aa00f2b311ecaa7c1b37e0a33989; _uetvid=6de4cb70d28311ec8fdb350ef89dfd89; granify.uuid=e9916e63-0f67-4819-87ef-9b3dc1bc0199; _ga=GA1.1.1182092054.1652422246; _ga_KR3J610VYM=GS1.1.1655967353.33.0.1655967353.60; granify.session.qivBM=-1; exp_hangover=nIpILCKmRP4nxg6ILok2QPRTS61jZACCpNpvumB6i5RHtVJBalFajH55alJ8YlFJZlpmcmZiTnxOYklqXnJlfKFhvJGBkZGSVVpiTnFqLQMA; last_browse_page=https%3A%2F%2Fwww.etsy.com%2Fshop%2FHomeRemediesStore",
    "origin":"https://www.etsy.com",
    "referer":"https://www.etsy.com/listing/1020012076/",
    # "sec-ch-ua":"" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"",
    # "sec-ch-ua-mobile":"?0",
    "sec-ch-ua-platform":"Windows",
    "sec-fetch-dest":"empty",
    "sec-fetch-mode":"cors",
    "sec-fetch-site":"same-origin",
    "x-csrf-token":"3:1655970376:M5TllACXvZew3XdpNGmoOLLESgD5:81672de120816c945619908e784eca11370660f1657e4252db1d0d00321be526",
    # "x-detected-locale":"USD|en-US|US",
    # "x-page-guid":"f0f9b42b706.8a7eea9bf086155065bc.00",
    "x-requested-with":"XMLHttpRequest"
}


params = {
    "log_performance_metrics": "false",
    "specs[reviews][]": "Etsy\Web\ListingPage\Reviews\ApiSpec",
    "specs[reviews][1][listing_id]": "1020012076",
    "specs[reviews][1][shop_id]": "6932389",
    "specs[reviews][1][render_complete]": "true",
    # "specs[reviews][1][active_tab]": "",
    "specs[reviews][1][should_lazy_load_images]": "false",
    "specs[reviews][1][should_use_pagination]": "true",
    "specs[reviews][1][page]": "1",
    "specs[reviews][1][should_show_variations]": "false",
    "specs[reviews][1][selected_keyword_filter]": "all",
    "specs[reviews][1][is_reviews_untabbed_cached]": "true",
    "specs[reviews][1][was_landing_from_external_referrer]": "false",
    "specs[reviews][1][sort_option]": "Relevancy"
}
client_params = json.dumps(params)

def get_page(url):
    # sessions = requests.session()
    # sessions.mount(url, HTTP20Adapter())
    # response = sessions.post(url, headers=headers, proxies=proxies, json=params)
    with httpx.Client(proxies=proxies) as client:
        response = client.post(url, headers=headers, json=params, timeout=3)
        print(response.status_code)
    # response.close()
    return response
    # if response.status_code == 200:
    #     print('连接成功')
    #     response.encoding = 'utf-8'
    #     return response.json()
    # return '连接失败'


# def parse_original_page(html):
#     global latest_review_time, earliest_review_time
#     comment_info = []
#     page_tree = etree.HTML(html)
#     reviews_num = page_tree.xpath('//*[@id="reviews"]/div[1]/div/div[1]/h2/text()')[0].strip().replace(' ', '').replace('\n', '').replace('reviews', '').replace('shop', '').replace('review', '')
#     item_reviews_num = page_tree.xpath('//*[@id="same-listing-reviews-tab"]/span/text()')
#     if item_reviews_num:
#         item_reviews_num = item_reviews_num[0].strip().replace(' ', '').replace('\n', '')
#     else:
#         item_reviews_num = ''
#
#     # 判断有无评论
#     if item_reviews_num != '':
#         # 判断评论时间有无对应评论人
#         if len(page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div[1]//p/text()')) > 1:
#             print(page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div[1]//div[contains(@class,"wt-display-flex-xs wt-align-items-center")]/p/text()'))
#             latest_review_time = page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div[1]//div[contains(@class,"wt-display-flex-xs wt-align-items-center")]/p[contains(@class,"wt-text-caption wt-text-gray")]/text()')[1].strip().replace('\n', '')
#         else:
#             latest_review_time = page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div[1]//div[contains(@class,"wt-display-flex-xs wt-align-items-center")]/p[contains(@class,"wt-text-caption wt-text-gray")]/text()')[0].strip().replace('\n', '')
#
#         #判断是否有翻页
#         if iselement(driver, '//*[@id="reviews"]/div[2]/nav/ul/li[2]/a'):
#             li_list = page_tree.xpath('//*[@id="reviews"]/div[2]/nav/ul/li')
#             if page_tree.xpath('//*[@id="reviews"]/div[2]/nav/ul/li[{}]/a/@href'.format(str(len(li_list)-1))) != '':
#                 last_page_path = '//*[@id="reviews"]/div[2]/nav/ul/li[{}]/a'.format(str(len(li_list) - 1))
#                 print('页标签：',len(li_list)-1,page_tree.xpath('//*[@id="reviews"]/div[2]/nav/ul/li[{}]/a/@href'.format(str(len(li_list)-1)))[0])
#                 try:
#                     new_html = click_to_last_page(last_page_path)
#                 except selenium.common.exceptions.StaleElementReferenceException:
#                     # time.sleep(2)
#                     new_html = click_to_last_page(last_page_path)
#                 new_page_tree = etree.HTML(new_html)
#                 div_list = new_page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div')
#                 if len(new_page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div[{}]//p/text()'.format(str(len(div_list))))) >1:
#                     earliest_review_time = new_page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div[{}]//div[contains(@class,"wt-display-flex-xs wt-align-items-center")]/p[contains(@class,"wt-text-caption wt-text-gray")]/text()'.format(str(len(div_list))))[1].strip().replace('\n', '')
#                 else:
#                     earliest_review_time = new_page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div[{}]//div[contains(@class,"wt-display-flex-xs wt-align-items-center")]/p[contains(@class,"wt-text-caption wt-text-gray")]/text()'.format(str(len(div_list))))[0].strip().replace('\n', '')
#         else:
#             div_list = page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div')
#             if len(page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div[{}]//p/text()'.format(str(len(div_list))))) > 1:
#                 earliest_review_time = page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div[{}]//div[contains(@class,"wt-display-flex-xs wt-align-items-center")]/p[contains(@class,"wt-text-caption wt-text-gray")]/text()'.format(str(len(div_list))))[1].strip().replace('\n', '')
#             else:
#                 earliest_review_time = page_tree.xpath('//*[@id="same-listing-reviews-panel"]/div/div[{}]//div[contains(@class,"wt-display-flex-xs wt-align-items-center")]/p[contains(@class,"wt-text-caption wt-text-gray")]/text()'.format(str(len(div_list))))[0].strip().replace('\n', '')
#     else:
#         latest_review_time=earliest_review_time= ''
#         print('该商品暂无评论！')
#     comment_item = [reviews_num, latest_review_time, earliest_review_time]
#     comment_info.append(comment_item)
#     print(comment_info)
#     driver.delete_all_cookies()
#     return comment_info


def write_to_file(content):
    with open('detail_info.txt', 'w', encoding='utf-8') as f:
        f.write(content)
        f.close()


url = 'https://www.etsy.com/api/v3/ajax/bespoke/member/neu/specs/reviews'
# url = 'https://www.etsy.com/listing/1020012076'


def main(url):
    html = get_page(url)
    print(html)
    # write_to_file(html)


main(url)
