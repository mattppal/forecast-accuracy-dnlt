# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
import os

class ForecastadvisorPipeline:
    def open_spider(self, spider):
        self.state_to_exporter = {}

    def close_spider(self, spider):
        for exporter in self.state_to_exporter.values():
            exporter.finish_exporting()

    def _exporter_for_item(self, item):
        adapter = ItemAdapter(item)
        sort_state = adapter['sort_state']
        
        if not os.path.exists('./payloads'):
            os.makedirs('./payloads')

        if sort_state not in self.state_to_exporter:
            f = open(f'./payloads/{sort_state}.csv', 'wb')
            exporter = CsvItemExporter(f)
            exporter.start_exporting()
            self.state_to_exporter[sort_state] = exporter
        return self.state_to_exporter[sort_state]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item
