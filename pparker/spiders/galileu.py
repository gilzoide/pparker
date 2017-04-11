# -*- coding: utf-8 -*-

import scrapy

from .html2txt_com_subtitulos import html2txt_com_subtitulos

import json
import re
import html

def monta_url(pagina):
    """Monta a URL da página desejada usando uma base comum"""
    return 'http://revistagalileu.globo.com/dinamico/plantao/galileu/galileu/qtd/10/{}/'.format(pagina)


class GalileuSpider(scrapy.Spider):
    name = "galileu"
    allowed_domains = ["revistagalileu.globo.com"]
    def start_requests(self):
        yield scrapy.Request(monta_url(self.settings.get('PAGINA_INICIAL')))

    def parse(self, response):
        data = json.loads(response.body)
        if data['itensObtidos']:
            for dado in data['conteudos']:
                if dado.get('corpo'):
                    yield {
                        'autor': ', '.join(dado['autor']),
                        'data': dado['data_ptbr'],
                        'categoria': ','.join(dado['editorias']),
                        'categoria_principal': dado['editoria_principal'],
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
    leia_mais_re = r"Leia\s+(mais|também)\s*:.*"
    comeca_mais_ou_asterisco_re = r"^\s*[+*].+$"
    fontes_re = r"Fontes?:.+\n|\([^)]+\)\n"
    varias_linhas_re = r"\n\s+\n"

    @staticmethod
    def limpa_corpo(corpo):
        """
        Pós-processamento do corpo, retirando tags HTML e outros ruídos da
        notícia, como "(Foto: <explicação>)", "Leia ['mais' | 'também']:<lista>"
        """
        texto = corpo
        texto = texto.replace('\r', '')
        texto = html2txt_com_subtitulos(texto)
        texto = re.sub(GalileuSpider.leia_mais_re, '', texto, flags=re.MULTILINE)
        texto = re.sub(GalileuSpider.comeca_mais_ou_asterisco_re, '', texto, flags=re.MULTILINE)
        texto = re.sub(GalileuSpider.foto_re, '', texto)
        texto = re.sub(GalileuSpider.fontes_re, '', texto)
        # último passo: comprimir o monte de espaços em branco
        texto = re.sub(r'^\t+', '', texto, flags=re.MULTILINE)
        texto = re.sub(GalileuSpider.varias_linhas_re, '\n\n', texto)
        return texto

