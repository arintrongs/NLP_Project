# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import datetime

# idx = 279063
idx = 274837
m = 200000

class PBSSpider(scrapy.Spider):

    name = 'pbs_spider'
    allowed_domains = ['news.thaipbs.or.th']
    start_urls = ['https://news.thaipbs.or.th/content/274837']
    handle_httpstatus_list = [404, 500]

    def parse(self, response):

        global idx,m
        if idx>m :
            idx = idx-1
            next_page = 'https://news.thaipbs.or.th/content/'+str(idx).zfill(6)
        else : return
           
        if response.status in (404, 500):
            print('heyyy')
            yield Request(next_page, callback=self.parse, dont_filter=True)
            return


        MonthL = ['มกราคม','กุมภาพันธ์','มีนาคม','เมษายน','พฤษภาคม','มิถุนายน','กรกฎาคม','สิงหาคม','กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม']
        DayL = ['MON','TUE','WED','THU','FRI','SAT','SUN']

        headline = response.xpath('//h1[@class="content-title"]/text()').extract_first()

        tokens = response.xpath('//div[@class="content-meta"]/span/text()').extract()     
        date_tokens = tokens[1].split()
        dd = date_tokens[0].zfill(2)
        mm = str(MonthL.index(date_tokens[1])+1).zfill(2)
        yy = date_tokens[2]

        date = dd+'/'+mm+'/'+yy
        DOW =DayL[datetime.datetime(int(yy)-543, int(mm), int(dd)).weekday()]
        time = tokens[0]
        view = tokens[2] 
        view = ''.join([e for e in view if e!= ','])
        category = response.xpath('//ol[@class="breadcrumb"]/li/a/text()').extract()[1]
        tag = response.xpath('//div[@class="tag-list"]/a/text()').extract()
        tag = ','.join(tag)
        content = response.xpath('//article[@class="content-article-content entry-content"]/p/text()').extract()
        content = ' '.join(' '.join(content).split('\xa0'))

        yield {'headline' : headline, 
        'date' : date,
        'DOW' : DOW,
        'time' : time,
        'view' : view,
        'category' : category,
        'tag': tag,
        'content': content 
        }

        yield Request(next_page, callback=self.parse, dont_filter=True)
    
    

        


