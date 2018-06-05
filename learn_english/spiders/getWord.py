# -*- coding: utf-8 -*-
import scrapy
from learn_english.word import Word, Comment


class GetwordSpider(scrapy.Spider):
    name = 'getWord'
    allowed_domains = ['qiaoyingyu123.com']
    start_urls = ['http://qiaoyingyu123.com/?p=25']

    def parse(self, response):
        word = Word()
        word['word'] = response.xpath('//div[@class="entry-content"]/h3/text()').extract_first()
        word['learn'] = response.xpath('//div[@class="dictionary-comment"]/p[last()]/text()').extract_first()
        next_line = response.xpath('//span[@class="nav-next"]/a/@href').extract_first()
        word['nextLine'] = next_line
        word['comments'] = []
        myList = response.xpath('//div[@class="dictionary-comment"]//p')
        for p in myList:
            if len(p.xpath('.//b').extract()) > 0:
                comment = Comment()
                comment['type'] = p.xpath('b/text()').extract_first()
                comment['desc'] = p.xpath('text()').extract_first()
                word['comments'].append(comment)
        # 如果使用管道， parse 必须返回要处理的数据
        yield word
        if len(next_line):
            yield scrapy.Request(response.urljoin(next_line), self.parse)
