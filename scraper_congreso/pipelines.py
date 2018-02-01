# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
class JsonWriterPipeline(object):
    total_publications = 0
    def open_spider(self, spider):
        self.file = open('congreso.json', 'w')

    def close_spider(self, spider):
        self.file_close()
    def process_item(self, item, spider):
        self.total_publications += 1
        print "Publications gathered: " + str(self.total_publications)
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
