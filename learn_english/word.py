#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy


class Word(scrapy.Item):
    word = scrapy.Field()
    learn = scrapy.Field()
    comments = scrapy.Field()
    nextLine = scrapy.Field()


class Comment(scrapy.Item):
    type = scrapy.Field()
    desc = scrapy.Field()