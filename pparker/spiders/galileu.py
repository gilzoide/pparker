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
                    'autor': ', '.join(dado['autor']),
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
    foto_re = r"\(\w+:[^)]+\)"
    leia_mais_re = r"Leia\s+(mais|também)\s*:\s*(.|\n)+?\n(\n|$)"
    varias_linhas_re = r"\n\s*\n"

    @staticmethod
    def limpa_corpo(corpo):
        """
        Pós-processamento do corpo, retirando tags HTML e outros ruídos da
        notícia, como "(Foto: <explicação>)", "Leia ['mais' | 'também']:<lista>"
        """
        texto = corpo
        texto = html.replace_entities(texto)
        texto = html.replace_escape_chars(texto, which_ones=('\r',))
        # TODO: adicionar subtítulos
        texto = html.remove_tags(texto)
        texto = re.sub(GalileuSpider.leia_mais_re, '', texto)
        texto = re.sub(GalileuSpider.foto_re, '', texto)
        texto = re.sub(GalileuSpider.varias_linhas_re, '\n\n', texto)

        return texto

