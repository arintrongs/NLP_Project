# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import datetime

# idx = 92066
idx = 71050
m = 0

class Ch3Spider(scrapy.Spider):

    name = 'ch3_spider'
    allowed_domains = ['news.ch3thailand.com']
    start_urls = ['http://news.ch3thailand.com/local/71050']

    def parse(self, response):

        global idx,m
        if idx>m :
            idx = idx-1
            
            next_page = 'http://news.ch3thailand.com/politics/'+str(idx).zfill(5)
        else : return
           
        if response.url == 'http://news.ch3thailand.com/pagenotfound': 
            yield Request(next_page, callback=self.parse, dont_filter=True)
            return

        MonthL = ['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.']
        DayL = ['MON','TUE','WED','THU','FRI','SAT','SUN']

        headline = response.xpath('//h1[@class="content-head"]/text()').extract_first()

        date_tokens = response.xpath('//p[@class="content-des-text"]/text()').extract()[1].split('\xa0')
        dd = date_tokens[0].split()[1]
        mm = str(MonthL.index(date_tokens[1])+1).zfill(2)
        yy = '25'+date_tokens[2]

        date = dd+'/'+mm+'/'+yy
        DOW =DayL[datetime.datetime(int(yy)-543, int(mm), int(dd)).weekday()]
        time = date_tokens[3].split()[1][:5]
        view = response.xpath('//p[@class="content-des-text"]/text()').extract()[2].split('\xa0')[2] 
        view = ''.join([e for e in view if e!= ','])
        category = response.xpath('//a[@class="content-des-link"]/text()').extract_first()
        tag = response.xpath('//article[@class="content-tag"]/a/text()').extract()
        tag = ','.join(tag)
        content = response.xpath('//div[@class="content-news"]//text()').extract()
        content = ' '.join(' '.join(content).split('\xa0'))

        ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if (headline[0].strip() in ascii_letters) and (content[0].strip() in ascii_letters) and  (content.split()[-1][-1] == '.') :
            yield Request(next_page, callback=self.parse, dont_filter=True)
            return

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
    
    

        


