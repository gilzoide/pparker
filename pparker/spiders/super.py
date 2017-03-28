# -*- coding: utf-8 -*-

import scrapy

from .html2txt_com_subtitulos import html2txt_com_subtitulos

import json
import re

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
            if not ('/videos/' in url or '/testes/' in url):
                yield scrapy.Request(url, callback=self.extrai_noticia)
        if not data['lastbatch']:
            self.pagina += 1
            next_url = monta_url(self.pagina)
            yield scrapy.Request(next_url)


    tava_na_exame_re = r"Este.+Exame\.com.*$"

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

        corpo = '\n'.join(response.css('article section.article-content > p').extract())
        yield {
            'autor': autor,
            'data': data,
            'categoria': ', '.join(categorias),
            'categoria_principal': categoria_principal,
            'url': url,
            'titulo': titulo,
            'subtitulo': subtitulo,
            'corpo': corpo,
            # se for notícia originalmente da Exame, manda pra pasta especial
            'pasta_destino': 'Noticias_Exame' if re.search(SuperSpider.tava_na_exame_re, corpo) else None
        }



    # Algumas Regex pra limpar textos
    rodape_re = r"^(Fontes|Post anterior):.+$|^\W+$"
    varias_linhas_re = r"\n\s+\n"
    linha_em_subtitulo_re = r"\n+</subtitle>"

    @staticmethod
    def limpa_corpo(corpo):
        texto = corpo
        texto = re.sub(r'<p>|<p [^>]+>', '<p>\t', texto)
        texto = html2txt_com_subtitulos(texto)
        texto = re.sub(r'^\t+', '', texto, flags=re.MULTILINE)
        texto = re.sub(SuperSpider.tava_na_exame_re, '', texto)
        texto = re.sub(SuperSpider.rodape_re, '', texto, flags=re.MULTILINE)
        texto = re.sub(SuperSpider.linha_em_subtitulo_re, '</subtitle>', texto)
        texto = re.sub(SuperSpider.varias_linhas_re, '\n\n', texto)
        return texto

