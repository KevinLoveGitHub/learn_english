# -*- coding: utf-8 -*-
import scrapy
from learn_english.word import Word, Comment


class GetwordSpider(scrapy.Spider):
    name = 'getWord'
    allowed_domains = ['qiaoyingyu123.com']
    start_urls = ['http://qiaoyingyu123.com/?p=25']

    def parse(self, response):
        word = Word()
        word['word'] = response.xpath('//h1[@class="entry-title"]/text()').extract_first()
        next_line = response.xpath('//span[@class="nav-next"]/a/@href').extract_first()
        word['nextLine'] = next_line
        word['comments'] = []
        all_desc_text = response.xpath('//div[@class="dictionary-comment"]//text()')
        all_text = response.xpath('//div[@class="entry-content"]//text()').extract()

        for text in all_text:
            if '巧记：' in text or '注：' in text:
                if len(text) > 3:
                    word['learn'] = text.strip().split('：', maxsplit=1)[1]

        for desc_selector in all_desc_text:
            desc_text = desc_selector.extract()
            if len(desc_text.strip()) > 0 and desc_text.endswith('.'):
                # print('desc_text', desc_selector.extract())
                comment = Comment()
                comment['type'] = desc_text
                desc_index = all_desc_text.index(desc_selector) + 1
                comment['desc'] = all_desc_text[desc_index].extract()
                word['comments'].append(comment)
        # 如果使用管道， parse 必须返回要处理的数据
        print(word)
        yield word
        if len(next_line):
            yield scrapy.Request(response.urljoin(next_line), self.parse)
