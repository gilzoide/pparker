# -*- coding: utf-8 -*-

import re
import html

def html2txt_com_subtitulos(corpo):
    # Regex de tags HTML: dá match em tag (abrindo ou fechando) e no
    # conteúdo antes da próxima
    tag_re = r"<([^>]+)>([^<>]*)"
    # Pilha de tags, pra tracking da profundidade
    pilha_tags = []
    # Lista que se tornará o resultado final =]
    resultado = []
    # Marca quando estamos pegando um subtítulo, e onde esse deve ficar
    eh_subtitulo = False
    indice_subtitulo = 0
    def checa_subtitulo():
        return (pilha_tags[-1:] == ['p'] and resultado[-1].endswith('\t')) or \
                (pilha_tags[-2:] == ['p', 'em'] and resultado[-2].endswith('\t'))

    todas_tags = re.findall(tag_re, corpo)
    for tag, txt in todas_tags:
        tag = tag.partition(' ')[0]
        if tag in ['/p', 'br', 'br /']:
            resultado.append('\n')
        if tag in ['strong', 'b'] and checa_subtitulo():
            indice_subtitulo = len(resultado)
            eh_subtitulo = True
        elif eh_subtitulo and tag in ['/strong', '/b']:
            if txt == '':
                resultado.insert(indice_subtitulo, '<subtitle>')
                resultado.append('</subtitle>')
            eh_subtitulo = False
        if tag == 'p' or len(pilha_tags) > 0 and pilha_tags[0] == 'p':
            resultado.append(html.unescape(txt))
        # Empilha/desempilha tags
        if not tag.endswith('/'):
            if not tag.startswith('/'):
                pilha_tags.append(tag)
            else:
                while pilha_tags.pop() != tag[1:]:
                    pass

    return ''.join(resultado)

