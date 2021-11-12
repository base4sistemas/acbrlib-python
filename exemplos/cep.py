# -*- coding: utf-8 -*-
#
# exemplos/cep.py
#
# Copyright 2021 Base4 Sistemas
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Invoque este exemplo, modificando os valores padrão das variáveis
diretamente neste código ou modificando os valores das variáveis de
ambiente na chamada, por exemplo:

    $ ACBRLIB_INI_PATH=/home/user/ACBR.INI python exemplos/cep.py

Não considere este exemplo completo ou definitivo. Dê uma boa olhada
antes de executá-lo. Sempre tomamos o cuidado de
não fazer nada que possa causar problemas.
"""

import os

from acbrlib_python import ACBrLibCEP


ACBRLIB_PATH = os.getenv('ACBRLIB_PATH', '/usr/lib/libacbrcep64.so')
ACBRLIB_INI_PATH = os.getenv('ACBRLIB_INI_PATH', '')
ACBRLIB_CHAVE_CRYPT = os.getenv('ACBRLIB_CHAVE_CRYPT', '')


def iniciacao_simples():
    cep = ACBrLibCEP.usar(ACBRLIB_PATH)
    cep.inicializar(ACBRLIB_INI_PATH, ACBRLIB_CHAVE_CRYPT)
    print(f'CEP_Nome: {cep.nome()}')
    print(f'CEP_Versao: {cep.versao()}')
    print(f'CEP_UltimoRetorno: {cep.ultimo_retorno()}')
    cep.finalizar()


def iniciacao_simples_e_segura():
    # o context manager garante a finalização
    with ACBrLibCEP.usando(
            ACBRLIB_PATH,
            arq_config=ACBRLIB_INI_PATH,
            chave_crypt=ACBRLIB_CHAVE_CRYPT) as cep:
        print(f'{cep.nome()}, versao {cep.versao()}')
        print(f'Último retorno: {cep.ultimo_retorno()}')


def consultar_por_cep():
    with ACBrLibCEP.usando(
            ACBRLIB_PATH,
            arq_config=ACBRLIB_INI_PATH,
            chave_crypt=ACBRLIB_CHAVE_CRYPT) as cep:
        enderecos = cep.buscar_por_cep('18270170')
        for endereco in enderecos:
            print(endereco)


def consultar_por_logradouro():
    with ACBrLibCEP.usando(
            ACBRLIB_PATH,
            arq_config=ACBRLIB_INI_PATH,
            chave_crypt=ACBRLIB_CHAVE_CRYPT) as cep:
        enderecos = cep.buscar_por_logradouro(
                logradouro='Rua Brasil',
                municipio='Catanduva',
                uf='SP'
            )
        for ender in enderecos:
            print(ender)


def manipulacao_de_configuracao():
    with ACBrLibCEP.usando(ACBRLIB_PATH) as cep:
        cep.config_ler(ACBRLIB_INI_PATH)
        # valor = cep.config_ler_valor('CEP', 'WebService')
        # print(f'CEP/WebService: {valor!r}')
        valor = cep.config_ler_valor('Principal', 'LogPath')
        print(f'Principal/LogPath: {valor!r}')


if __name__ == '__main__':
    # iniciacao_simples()
    # iniciacao_simples_e_segura()
    # consultar_por_cep()
    consultar_por_logradouro()
    # manipulacao_de_configuracao()
