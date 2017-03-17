# -*- coding: utf-8 -*-

from scrapy.exporters import BaseItemExporter

class TxtItemExporter(BaseItemExporter):
    """Exporta um Txt, do jeitinho que vier (tem que ser string, huh)"""
    def __init__(self, arquivo, *args, **kwargs):
        BaseItemExporter.__init__(self, *args, **kwargs)
        self.arquivo = arquivo

    def export_item(self, item):
        self.arquivo.write(item)

