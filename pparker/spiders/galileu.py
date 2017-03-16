# -*- coding: utf-8 -*-

import scrapy

import json
import html

def monta_url(pagina):
    """Monta a URL da página desejada usando uma base comum"""
    return 'http://revistagalileu.globo.com/dinamico/plantao/galileu/galileu/qtd/10/{}/'.format(pagina)

def processa_dado(dado):
    """Arruma os dados recebidos para saírem do jeito que queremos"""
    return {
        'autor': dado['autor'],
        'data': dado['data_ptbr'],
        'editorias': dado['editorias'],
        'editoria_principal': dado['editoria_principal'],
        'url': dado['permalink'],
        'titulo': dado['titulo'],
        'subtitulo': dado['subtitulo'],
        # TODO: limpar \r\n, e tirar tags inúteis
        'corpo': html.unescape(dado['corpo']),
    }


class GalileuSpider(scrapy.Spider):
    name = "galileu"
    allowed_domains = ["revistagalileu.globo.com"]
    start_urls = [monta_url(1)]

    def parse(self, response):
        data = json.loads(response.body)
        if data['itensObtidos']:
            for dado in data['conteudos']:
                yield processa_dado(dado)
            proxima_pagina = int(data['paginaAtual']) + 1
            next_url = monta_url(proxima_pagina)
            yield scrapy.Request(next_url)

