# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# 爬取到的数据写入到SQLite数据库
import sqlite3


class LearnEnglishPipeline(object):
    # 打开数据库
    def open_spider(self, spider):
        print('open_spider: ' + spider.name)
        db_name = spider.settings.get('SQLITE_DB_NAME', 'word.db')
        self.db_conn = sqlite3.connect(db_name)
        self.db_cur = self.db_conn.cursor()

    # 关闭数据库
    def close_spider(self, spider):
        print('close_spider: ' + spider.name)
        self.db_conn.commit()
        self.db_conn.close()

    # 对数据进行处理
    def process_item(self, item, spider):
        print('process_item: ' + spider.name)
        self.insert_db(item)
        return item

    # 插入数据
    def insert_db(self, item):
        values = (
            item['word'],
            item['learn'],
            None,
        )

        sql = 'INSERT INTO word VALUES(?,?,?)'
        self.db_cur.execute(sql, values)
        word_id = int(self.db_cur.lastrowid)
        self.insert_comment_db(item['comments'], word_id)

    def insert_comment_db(self, item, wid):
        for comment in item:
            # print('insert_comment_db: ' + str(comment))
            values = (
                None,
                comment['type'],
                comment['desc'],
                wid
            )
            sql = 'INSERT INTO comment VALUES(?,?,?,?)'
            self.db_cur.execute(sql, values)
