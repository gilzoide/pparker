# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .exporters import TxtItemExporter

import re
from os import path, makedirs

class LimpaCorpoNoticia(object):
    """
    Limpa o corpo de uma notícia, tirando tags HTML, e talz.

    Para efetivamente limpar o corpo da notícia, implemente um método
    `limpa_corpo` em sua spider.
    """

    saida_template = r"""<title>{titulo}</title>
<subtitle>{subtitulo}</subtitle>
<category>{categoria}</category>
<author>{autor}</author>
<date>{data}</date>
<url>{url}</url>

{corpo}"""
    def process_item(self, item, spider):
        limpador = getattr(spider, 'limpa_corpo', lambda x: x)
        item['final'] = LimpaCorpoNoticia.saida_template.format(
            titulo=item['titulo'],
            subtitulo=item['subtitulo'],
            categoria=item['categoria'],
            autor=item['autor'],
            data=item['data'],
            url=item['url'],
            corpo=limpador(item['corpo']),
        )
        return item


class SalvaNoLugar(object):
    """Pipeline que exporta cada item da lista em seu arquivo"""
    def process_item(self, item, spider):
        pasta_saida = path.expanduser(spider.settings.get('DIRETORIO_SAIDA'))
        subpasta = path.join(pasta_saida, spider.name, item['categoria_principal'].title())
        makedirs(subpasta, exist_ok=True)
        nome_arquivo = path.join(subpasta, re.sub(r'\W', '_', item['titulo'])) + '.txt'
        with open(nome_arquivo, 'w') as arquivo:
            exp = TxtItemExporter(arquivo)
            exp.start_exporting()
            exp.export_item(item['final'])
            exp.finish_exporting()

        return item

