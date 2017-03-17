# -*- coding: utf-8 -*-

import scrapy

import json
import re
from w3lib import html

def monta_url(pagina):
    """Monta a URL da página desejada usando uma base comum"""
    return 'http://revistagalileu.globo.com/dinamico/plantao/galileu/galileu/qtd/10/{}/'.format(pagina)


class GalileuSpider(scrapy.Spider):
    name = "galileu"
    allowed_domains = ["revistagalileu.globo.com"]
    start_urls = [monta_url(1)]

    def parse(self, response):
        data = json.loads(response.body)
        if data['itensObtidos']:
            for dado in data['conteudos']:
                yield {
                    'autor': dado['autor'],
                    'data': dado['data_ptbr'],
                    'editorias': dado['editorias'],
                    'editoria_principal': dado['editoria_principal'],
                    'url': dado['permalink'],
                    'titulo': dado['titulo'],
                    'subtitulo': dado['subtitulo'],
                    'corpo': dado['corpo'],
                }
            proxima_pagina = int(data['paginaAtual']) + 1
            next_url = monta_url(proxima_pagina)
            yield scrapy.Request(next_url)

    # Algumas Regex pra limpar textos
    foto_re = r"\(Foto:[^)]+\)"
    possivel_subtitulo_re = r"(.+)[^.:;!?\n]\n"

    @staticmethod
    def limpa_corpo(corpo):
        """
        Pós-processamento do corpo, retirando tags HTML e outros ruídos da
        notícia, como "(Foto: <explicação>)", "Leia ['mais' | 'também']:<lista>"
        """
        def possivel_subtitulo(match):
            linha = match.group(0)
            print(linha)
            eh_foto = re.match(GalileuSpider.foto_re, linha)
            if eh_foto:
                return linha[0:eh_foto.pos]
            else:
                return linha
        texto = corpo
        texto = html.replace_entities(texto)
        texto = html.replace_escape_chars(texto, which_ones=('\r',))
        texto = html.remove_tags(texto)
        #  texto = re.sub(GalileuSpider.possivel_subtitulo_re, possivel_subtitulo, texto)

        return texto

