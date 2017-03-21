# -*- coding: utf-8 -*-

import scrapy

import json
import re
import html

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
    leia_mais_re = r"Leia\s+(mais|também)\s*:(\s*\+[^\n]+)+"
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
        texto = GalileuSpider.html2txt_com_subtitulos(texto)
        texto = re.sub(GalileuSpider.leia_mais_re, '', texto)
        #  texto = re.sub(GalileuSpider.foto_re, '', texto)
        texto = re.sub(GalileuSpider.fontes_re, '', texto)
        # último passo: comprimir o monte de linhas juntas
        texto = re.sub('\n\t+', '\n', texto)
        texto = re.sub(GalileuSpider.varias_linhas_re, '\n\n', texto)
        return texto

    @staticmethod
    def html2txt_com_subtitulos(corpo):
        # Regex de tags HTML: dá match em tag (abrindo ou fechando) e no
        # conteúdo antes da próxima
        tag_re = r"<([^>]+)>([^<>]*)"
        def paragrafo_subtitulo(p):
            return p.endswith('\t')
        # Pilha de tags, pra tracking da profundidade
        pilha_tags = ['html']
        # Lista que se tornará o resultado final =]
        resultado = []
        # Booleano que marca quando estamos pegando um subtítulo
        eh_subtitulo = False

        all_tags = re.findall(tag_re, corpo)
        for tag, txt in all_tags:
            if tag == '/p' or tag == 'br /':
                resultado.append('\n')
            if tag == 'strong' and \
                    ((pilha_tags[-1:] == ['p'] and paragrafo_subtitulo(resultado[-1])) or \
                    (pilha_tags[-2:] == ['p', 'em'] and paragrafo_subtitulo(resultado[-2]))):
                resultado.append('<subtitle>')
                eh_subtitulo = True
            elif eh_subtitulo and tag == '/strong':
                resultado.append('</subtitle>')
                eh_subtitulo = False
            resultado.append(html.unescape(txt))
            # Empilha/desempilha tags
            if not tag.endswith('/'):
                if not tag.startswith('/'):
                    pilha_tags.append(tag.partition(' ')[0])
                else:
                    pilha_tags.pop()

        

        return ''.join(resultado)


