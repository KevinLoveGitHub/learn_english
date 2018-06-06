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
        last_sample_target = response.xpath('//p[@class="sample-target"][last()]/text()').extract_first().strip()
        all_text = response.xpath('//div[@class="entry-content"]//text()').extract()
        all_desc = response.xpath('//div[@class="dictionary-comment"]//p[not(@class)]//text()').extract()

        for text in all_text:
            # print('text', text)
            if '巧记：' in text or '注：' in text:
                if len(text) > 3:
                    word['learn'] = text.strip().split('：', maxsplit=1)[1]

            if len(text) > 1 and text.endswith('.') and text in all_desc:
                comment = Comment()
                comment['type'] = text
                desc_index = all_text.index(text) + 1
                comment['desc'] = all_text[desc_index]
                print(comment['type'])
                print(comment['desc'])
                word['comments'].append(comment)

        # 判断对象中是否存在元素
        if word.get('learn') is None:
            word['learn'] = last_sample_target

        # 如果使用管道， parse 必须返回要处理的数据
        yield word
        if len(next_line):
            yield scrapy.Request(response.urljoin(next_line), self.parse)
