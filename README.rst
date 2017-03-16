PParker
=======
Aranhas que buscam notícias usando scrapy_. Notícias são tiradas dos sites
das revistas Galileu_ e `Super Interessante`_. Por enquanto, somente a aranha
`galileu` está implementada.

.. _scrapy: https://scrapy.org/
.. _python 3: https://www.python.org/
.. _Galileu: http://revistagalileu.globo.com/
.. _Super Interessante: http://super.abril.com.br/


Dependências
============
- `python 3`_
- scrapy_


Como rodar
==========
Há uma aranha para cada revista. Para rodar ambas, utilize os seguintes
comandos::

    $ scrapy crawl galileu
    $ scrapy crawl super

Note que, por enquanto, PParker busca somente 20 notícias, para facilitar os
testes. Para baixar todas as notícias disponíveis (o que demora, utilize os seguintes
comandos::

    $ scrapy crawl --set DEPTH_LIMIT=0 galileu
    $ scrapy crawl --set DEPTH_LIMIT=0 super

Saídas
======
As notícias coletadas são armazenadas na pasta "noticias", em subpastas
específicas da revista e seções da mesma. Cada arquivo é uma notícia
individual.