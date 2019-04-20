# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest


class NewsSpider(scrapy.Spider):
    name = 'news'
    # allowed_domains = ['thestandard.co']
    start_urls = ['https://thestandard.co/category/news/page/' +
                  str(page_num) for page_num in range(830, 987)]

    def parse(self, response):
        for url in response.xpath('//h3[@class=\'news-title\']/a/@href').getall():
            yield SeleniumRequest(url=url, callback=self.news)

    def news(self, response):
        headline = response.xpath(
            '//div[@class=\'entry-title\']/h1/text()').get().strip('"').strip()
        date = response.xpath(
            '//div[@class=\'meta-date\']/span/text()').get().strip('"').strip()
        views = response.xpath(
            '//span[@class=\'entry-view\']/@data-views').get().strip('"').strip()
        share = response.xpath(
            '//span[@class=\'fb-share-count count\']/text()').get().strip('"').strip()
        category = response.xpath(
            '//div[@class=\'entry-meta\']/span[@class=\'category\']/a/text()').getall()
        tags = response.xpath('//div[@class=\'tags\']/a/text()').getall()
        contents = response.xpath(
            '//div[@class=\'entry-content\']/p/span/text()').getall()[:-1]
        contents = ''.join(contents)
        yield {'headline': headline, 'date': date, 'time': None, 'view': views, 'like': None, 'share': share, 'comment': None, 'category': category, 'tag': tags, 'content': contents}
