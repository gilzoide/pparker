PParker
=======
Aranhas que buscam notícias usando scrapy_. Notícias são tiradas dos sites
das revistas `Galileu`_, `Super Interessante`_ e `Mundo Educação`_.

.. _scrapy: https://scrapy.org/
.. _python 3: https://www.python.org/
.. _Galileu: http://revistagalileu.globo.com/
.. _Super Interessante: http://super.abril.com.br/
.. _Mundo Educação: http://mundoeducacao.bol.uol.com.br/


Dependências
============
- `python 3`_
- scrapy_


Como rodar
==========
Há uma aranha para cada revista. Para rodar todas, utilize os seguintes
comandos::

    $ scrapy crawl galileu
    $ scrapy crawl super
    $ scrapy crawl mundoeducacao

Note que, por enquanto, PParker busca somente 20 notícias, para facilitar os
testes. Para baixar todas as notícias disponíveis (o que demora), utilize os
seguintes comandos::

    $ scrapy crawl -s DEPTH_LIMIT=0 galileu
    $ scrapy crawl -s DEPTH_LIMIT=0 super
    $ scrapy crawl -s DEPTH_LIMIT=0 mundoeducacao

Para alterar a pasta de destino das notícias, utilize a opção ``DIRETORIO_SAIDA``::

    $ scrapy crawl -s DIRETORIO_SAIDA=caminho_das_noticias galileu

Saídas
======
As notícias coletadas são armazenadas na pasta "noticias", em subpastas
específicas da revista e seções da mesma. Cada arquivo é uma notícia
individual.

Curiosidade
===========
**Por que PParker?**

É uma aranha que busca notícias, quem isso te lembra? =P
