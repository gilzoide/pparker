# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import XmlItemExporter

from os import path, makedirs

class NoticiaPipeline(object):
    """Pipeline que exporta cada item da lista em seu arquivo"""
    def process_item(self, item, spider):
        subpasta = path.join('noticias', spider.name, item['editoria_principal'])
        makedirs(subpasta, exist_ok=True)
        nome_arquivo = path.join(subpasta, item['titulo']) + '.xml'
        with open(nome_arquivo, 'w') as arquivo:
            exp = XmlItemExporter(arquivo, root_element='noticia')
            exp.start_exporting()
            exp.export_item(item)
            exp.finish_exporting()

        return item
