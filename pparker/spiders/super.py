# -*- coding: utf-8 -*-
import scrapy

import json
from pprint import pprint

def monta_url(pagina):
    """Monta a URL da página desejada usando uma base comum"""
    return 'http://super.abril.com.br/?infinity=scrolling&page={}'.format(pagina)

class SuperSpider(scrapy.Spider):
    name = "super"
    DOMAIN = "super.abril.com.br"
    allowed_domains = ["super.abril.com.br"]
    def start_requests(self):
        self.pagina = int(self.settings.get('PAGINA_INICIAL'))
        yield scrapy.Request(monta_url(self.pagina))

    def parse(self, response):
        data = json.loads(response.body)
        for url in data['postflair'].keys():
            if '/videos/' not in url:
                yield scrapy.Request(url, callback=self.extrai_noticia)
        if not data['lastbatch']:
            self.pagina += 1
            next_url = monta_url(self.pagina)
            yield scrapy.Request(next_url)

    def extrai_noticia(self, response):
        header = response.css('article header')
        titulo = header.css('h1.article-title::text').extract_first()
        subtitulo = header.css('h2.article-subtitle::text').extract_first()
        data = header.css('div.article-date span::text').extract_first().strip().partition(',')[0]
        # Autor tem vários formatos: pega o que não tem o texto "Por" (segundo)
        header_autor = header.css('div.article-author')
        autor = header_autor.xpath('descendant::text()').extract()[1]
        url = response.url
        # Categorias no rodapé: "TUDO SOBRE"
        categorias = response.css('article section.article-tags a::text').extract()
        categoria_principal = '/'.join(url.split('/')[3:-2])

        corpo = response.css('article section.article-content').extract_first()

        yield {
            'autor': autor,
            'data': data,
            'categoria': ', '.join(categorias),
            'categoria_principal': categoria_principal,
            'url': url,
            'titulo': titulo,
            'subtitulo': subtitulo,
            'corpo': corpo,
        }

