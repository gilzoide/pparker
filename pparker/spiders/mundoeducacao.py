# -*- coding: utf-8 -*-

import scrapy

from .html2txt_com_subtitulos import html2txt_com_subtitulos

import re

def get_proxima_pagina(url):
    """Transforma a url na da próxima página, trocando o número do final"""
    prefixo, _, pagina_atual = url.rpartition('/')
    nova_pagina = int(pagina_atual) + 1
    return '{}/{}'.format(prefixo, nova_pagina)

class MundoeducacaoSpider(scrapy.Spider):
    name = "mundoeducacao"
    allowed_domains = ["mundoeducacao.bol.uol.com.br"]
    start_urls = [
        'http://mundoeducacao.bol.uol.com.br/saude-bem-estar/1',
        'http://mundoeducacao.bol.uol.com.br/curiosidades/1',
        'http://mundoeducacao.bol.uol.com.br/politica/1',
        'http://mundoeducacao.bol.uol.com.br/drogas/1',
        'http://mundoeducacao.bol.uol.com.br/biologia/1',
        'http://mundoeducacao.bol.uol.com.br/sociologia/1',
    ]

    def parse(self, response):
        noticias = response.css('div.box-item h3 a::attr(href)').extract()
        for url in noticias:
            yield scrapy.Request(url, callback=self.extrai_noticia)
        # próxima página, se ainda tiver notícia
        if noticias:
            yield scrapy.Request(get_proxima_pagina(response.url))

    def extrai_noticia(self, response):
        url = response.url
        content = response.css('div.content')
        header = content.css('div#crumbs')
        titulo = header.css('h2::text').extract_first()
        subtitulo = header.css('h3::text').extract_first() or ''
        # Metadados: Autor e categoria
        metadados = header.css('p.post-meta > span > a::text').extract()
        autor = metadados[0]
        categoria = metadados[1].strip()
        # Conteúdo
        corpo = '\n'.join(content.css('div#conteudo-texto p, div#conteudo-texto ul').extract())

        if corpo:
            yield {
                'autor': autor,
                'data': '',
                'categoria': categoria,
                'categoria_principal': categoria,
                'url': url,
                'titulo': titulo,
                'subtitulo': subtitulo,
                'corpo': corpo,
            }

    # Algumas Regex pra limpar textos
    ul_li_span2p_re = r"<ul[^>]*>\s*<li[^>]*>\s*<span[^>]*>(.+?)</span>\s*</li>\s*</ul>"

    @staticmethod
    def limpa_corpo(corpo):
        texto = corpo
        texto = texto.replace('\r', '')
        texto = re.sub(MundoeducacaoSpider.ul_li_span2p_re, r'<p>\1</p>', texto)
        texto = re.sub(r'<p>|<p [^>]+>', '<p>\t', texto)
        texto = html2txt_com_subtitulos(texto)
        texto = re.sub(r'^\t+', '', texto, flags=re.MULTILINE)
        texto = re.sub(r"\n\s+\n", '\n\n', texto)
        return texto
