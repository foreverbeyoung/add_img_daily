# coding:utf-8
import random
import re

import parsel
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner,CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from scrapy.mail import MailSender
import os

import requests
#configure_logging(install_root_handler=False)
from fake_useragent import UserAgent
mail = MailSender.from_settings(settings=get_project_settings())

# def mail_send(sub, body=''):
#     mail.send(to=MAIL_LIST, subject=sub, body=body)
USER_AGENTS = [
 "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
 "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
 "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
 "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
 "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
 "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
 "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
 "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
 "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
 "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
def get_header(asin='B078Y9QT8P'):
    return {
  'cookie': 'session-id-time=2082787201l; session-id=132-3255370-1340819; ubid-main=135-2389356-6925346; i18n-prefs=USD; SL_G_WPT_TO=zh; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; session-token=3dp8Gbcu6rhFcNwUjw8S2dOStyNc87CuwLDLMnZsp6fgwu1a4VU3kG79B0XDWFEtHVZt25VMM101tpMJk5DQYiKLykX7mFQP4tEvSy+mWh/jrC2+EGvjc9HUAREiv/lByXmFMmKo/EiFzeo2f4q5GYCfBdHtrgNJr2azX+elA67KdBFj5XHSeW0gZkm9+P7m; csm-hit=tb:VFBF9C8MQ7YRGVSJ0NNE+s-N8PBMR9R67VPHFREJ5KB|1643009309782&t:1643009309782&adb:adblk_yes',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }

def get_asin_top(key_word ='anker',total_page=2):
    """

    :param key_word: 输入的搜索关键词
    :return: 相关的top类型asin
    """
    total_asin = []
    search_url = 'https://www.amazon.com/s?k=nebula&i=electronics&rh=n:172282,p_89:NEBULA&dc&page={}&crid=WADWI28JVX8D&qid=1643013553&rnid=2528832011&sprefix=nebula,electronics,927&ref=sr_pg_{}'
    for page in range(total_page+1)[1:]:
        print(search_url.format(str(page),str(page)))
        response = requests.get(search_url.format(str(page),str(page)),headers=get_header()).text
        # with open('1.html', 'w', encoding='utf-8') as f:
        #
        #     f.write(response)
        # print(response)
        res_extr = parsel.Selector(text=response)
        total_contain = res_extr.xpath('//*[@data-component-type="s-search-result"]')
        for contain in total_contain:
            asin = contain.xpath('./@data-asin').extract_first()

            print(asin)
            total_asin.append(asin)
    return total_asin
def save_xlt(input,doc_name):
    """

    :param input: 所有asin集合(列表 元组 set)
    :param doc_name: 预计存成的文件名
    :return: 生成一个可读可写的装asin的文件
    """
    # if not os.path.exists(doc_name):
    #     os.mknod(doc_name)
    with open(doc_name,'w',encoding='utf-8') as f:
        for asin in input:
            f.writelines(asin+'\n')




configure_logging()

# def _finished_message(c):
#     return "NODE: %s, ROUND: %s, FINISHED IN %s" % (NODE, c, now())

def start_spider():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    for spider_name in process.spider_loader.list():
        print(spider_name)
        # if spider_name in ('dereview','frreview','itreview','ukreview','usreview','jpreview'):

        process.crawl(spider_name)
    process.start()

if __name__ == '__main__':
    total_asin = get_asin_top()
    print(total_asin)
    save_xlt(total_asin,'roal.txt')
    # start_spider()