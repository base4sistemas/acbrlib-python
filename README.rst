
==============
ACBrLib Python
==============

|PyPI pyversions| |PyPI version fury.io| |PyPI license|

Camada de abstração para acesso à `ACBrLib`_ em Python.

----

`ACBrLib`_ é um conjunto de bibliotecas voltadas para o mercado de
automação comercial que oferece acesso à um conjunto rico de abstrações
que facilitam o desenvolvimento de aplicações como pontos-de-venda (PDV) e
aplicações relacionadas. Esta biblioteca fornece uma camada que torna
trivial a utilização da `ACBrLib`_ em seus próprios aplicativos escritos em
`linguagem Python <https://www.python.org>`_.

.. note::

    Esta biblioteca está em seus primeiros estágios de desenvolvimento,
    portanto, não espere encontrar toda a riqueza que os componentes
    `ACBr`_ possuem, por enquanto. Mas estamos totalmente abertos a
    `sujestões`_ e estamos aceitando `pull-requests`_.


Instalação
----------

Instale, preferencialmente em um ambiente virtual, usando ``pip``:

.. code-block:: shell

    pip install acbrlib-python


ACBrLibCEP
----------

Dá acesso a consultas de CEP utilizando dezenas de serviços de consulta
disponíveis. Alguns desses serviços podem ser gratuítos ou gratuítos para
desenvolvimento. Veja `este link <https://acbr.sourceforge.io/ACBrLib/ConfiguracoesdaBiblioteca8.html>`_
para ter uma ideia dos serviços que podem ser utilizados.

Para fazer uma consulta baseada no CEP:

.. code-block:: python

    from acbrlib_python import ACBrLibCEP

    with ACBrLibCEP.usando('/caminho/para/libacbrcep64.so') as cep:
        enderecos = cep.buscar_por_cep('18270170')
        for endereco in enderecos:
            print(endereco)

O trecho acima resultará em uma lista de objetos ``Endereco`` como resultado
da busca, prontos para serem usados. A consulta acima trará um único resultado
(usando o serviço `ViaCEP <https://viacep.com.br/>`_):

.. code-block:: python

    Endereco(
            tipo_logradouro='',
            logradouro='Rua Coronel Aureliano de Camargo',
            complemento='',
            bairro='Centro',
            municipio='Tatuí',
            uf='SP',
            cep='18270-170',
            ibge_municipio='3554003',
            ibge_uf='35'
        )

Para mais exemplos de uso, veja a pasta ``exemplos`` neste repositório.


Sobre Nomenclatura e Estilo de Código
=====================================

Uma questão muito relevante é a maneira como esta abstração se refere aos
nomes dos métodos disponíveis na biblioteca `ACBrLib`_ que utiliza uma
convenção de nomenclatura para variáveis e nomes de argumentos ou
parâmetros de funções conhecida como `Notação Húngara <https://pt.wikipedia.org/wiki/Nota%C3%A7%C3%A3o_h%C3%BAngara>`_.
Porém, em Python é utilizada a convenção `snake case <https://en.wikipedia.org/wiki/Snake_case>`_
tal como descrito na `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_.

Assim, para manter o estilo de Python, os nomes de variáveis e argumentos de
função deverão descartar o prefixo que indica o tipo de dado e converter o
restante para snake case, assim como nomes de métodos e funções também,
por exemplo:

* `eArqConfig` para `arq_config`;
* `ConfigLerValor` para `config_ler_valor`;
* `eArquivoXmlEvento` para `arquivo_xml_evento`;
* etc…

Métodos de bibliotecas que são prefixados com o nome da lib, será descartado o
prefixo e o restante do nome do método convertido para snake case, por exemplo:

* (ACBrLibNFe) `NFE_CarregarINI` para `carregar_ini`;
* (ACBrLibNFe) `NFE_ValidarRegrasdeNegocios` para `validar_regras_de_negocios`
  (note a correção do conector `de` que está em minúsculo no original);
* (ACBrLibCEP) `CEP_BuscarPorLogradouro` para `buscar_por_logradouro`;
* etc…

Esperamos que essa explicação faça sentido, senão, envia suas `sujestões`_.


Desenvolvimento
===============

Você é bem-vindo para ajudar no desenvolvimento desta biblioteca enviando
suas contribuições através de `pull-requests`_. Faça um *fork* deste
repositório e execute os testes antes de começar a implementar alguma
coisa. A gestão de dependências é feita via `Poetry`_ e recomendamos a
utilização de `pyenv`_

.. code-block:: shell

    $ git clone https://github.com/base4sistemas/acbrlib-python.git
    $ cd acbrlib-python
    $ poetry install
    $ poetry run pytest


.. _`sujestões`: https://github.com/base4sistemas/acbrlib-python/issues
.. _`pull-requests`: https://github.com/base4sistemas/acbrlib-python/pulls
.. _`ACBr`: https://projetoacbr.com.br/
.. _`ACBrLib`: https://projetoacbr.com.br/downloads/#acbrlib
.. _`pyenv`: https://github.com/pyenv/pyenv
.. _`Poetry`: https://python-poetry.org/

.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/acbrlib-python.svg
   :target: https://pypi.python.org/pypi/acbrlib-python/

.. |PyPI version fury.io| image:: https://badge.fury.io/py/acbrlib-python.svg
   :target: https://pypi.python.org/pypi/acbrlib-python/

.. |PyPI license| image:: https://img.shields.io/pypi/l/acbrlib-python.svg
   :target: https://pypi.python.org/pypi/acbrlib-python/
