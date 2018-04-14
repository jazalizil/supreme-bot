# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem
from scrapy.exporters import JsonItemExporter


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item


class JsonPipeline(object):
    file = None
    exporter = None

    def open_spider(self, spider):
        self.file = open(spider.name + ".json", 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        if self.exporter:
            self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        if self.exporter:
            self.exporter.export_item(item)
        return item
