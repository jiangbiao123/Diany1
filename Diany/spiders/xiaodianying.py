# -*- coding: utf-8 -*-
import scrapy
from Diany.items import DianyItem
from lxml import etree
from bs4 import BeautifulSoup


class XiaodianyingSpider(scrapy.Spider):
    name = 'xiaodianying'
    allowed_domains = ['tom960.com']
    start_urls = ['https://tom960.com/yazhouqingse/', 'https://tom960.com/guochanzipai/',
                  'https://tom960.com/oumeixingai/', 'https://tom960.com/chengrendongman/']

    def parse(self, response):
        try:
            soup = BeautifulSoup(response.text, 'lxml')
            link_list = soup.find_all(class_='listBox pl pr col-lg-2 col-md-3 col-sm-4 col-xs-6')
            tree = etree.HTML(response.text)
            fanye_url = 'https://tom960.com' + \
                        tree.xpath('//div[@id="player-dylist"]/a/i[@class="fa fa-chevron-right"]/parent::a/@href')[0]

            # print(link_list)
            for link in link_list:
                pic = link.find_all(class_='pic')[0]['href']
                # print(pic)
                pic_url = 'https://tom792.com' + pic
                # print(pic_url)
                yield scrapy.Request(url=pic_url, callback=self.get_link, dont_filter=True)
            if fanye_url:
                # print(fanye_url)
                yield scrapy.Request(url=fanye_url, callback=self.parse)
            pass
        except Exception as e:
            print("没有数据了")

    def get_link(self, response):
        item = DianyItem()
        tree = etree.HTML(response.text)
        content = tree.xpath('//*[@id="downlist_1"]/table/tbody/script[12]/text()')
        downurls = content[0].split('var')[1]
        # last_url = downurls.split('#')[1]
        item['last_url'] = downurls.split('#')[1]
        # print(content)
        yield item
