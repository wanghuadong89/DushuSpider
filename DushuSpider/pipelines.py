# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
class DushuspiderPipeline(object):

    def open_spider(self,spider):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user = 'root',
            password='123456',
            db='dushudb',
            charset='utf8'
        )
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        # sql语句
        sql = "INSERT INTO books VALUES(NULL,'%s','%s','%s','%s','%s','%s','%s','%s')" % (item['name'],item['author'],item['cover_img'],item['cbs'],item['content'],item['author_info'],item['price'],item['mulu'])
        self.cur.execute(sql)
        self.conn.commit()
        return item

    def close_spider(self,spider):
        self.cur.close()
        self.conn.close()