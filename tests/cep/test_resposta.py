# -*- coding: utf-8 -*-
#
# tests/cep/test_resposta.py
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

import pytest

from acbrlib_python.cep.impl import processar_resposta
from acbrlib_python.cep.excecoes import ACBrLibCEPErroResposta


def test_resposta_sem_resultados():
    """Uma resposta sem resultados deve resultar uma lista vazia."""
    conteudo = [
            '[CEP]',
            'Quantidade=0',
        ]
    enderecos = processar_resposta('\n'.join(conteudo))
    assert len(enderecos) == 0


def test_resposta_com_um_resultado():
    """Resposta normal, contendo um resultado."""
    conteudo = [
            '[Endereco1]',
            'Bairro = Centro',
            'CEP = 18270-170',
            'Complemento =',
            'IBGE_Municipio = 3554003',
            'IBGE_UF = 35',
            'Logradouro = Rua Coronel Aureliano de Camargo',
            'Municipio = Tatuí',
            'Tipo_Logradouro =',
            'UF = SP',
            '',
            '[CEP]',
            'Quantidade = 1',
        ]
    enderecos = processar_resposta('\n'.join(conteudo))
    assert len(enderecos) == 1

    e = enderecos[0]
    assert e.tipo_logradouro == ''
    assert e.logradouro == 'Rua Coronel Aureliano de Camargo'
    assert e.complemento == ''
    assert e.bairro == 'Centro'
    assert e.municipio == 'Tatuí'
    assert e.uf == 'SP'
    assert e.cep == '18270-170'
    assert e.ibge_municipio == '3554003'
    assert e.ibge_uf == '35'


def test_resposta_mal_formada_sem_quantidade():
    """
    Testa uma resposta que não possui a seção que indica a quantidade de
    endereços encontrados.
    """
    conteudo = [
            '[Endereco1]',
            'Tipo_Logradouro = Rua',
        ]
    with pytest.raises(ACBrLibCEPErroResposta):
        processar_resposta('\n'.join(conteudo))


def test_resposta_mal_formada_sem_enderecos():
    """
    Testa uma resposta que indica a existência de 1 endereço, mas que não
    possui nenhuma seção ``EnderecoN``.
    """
    conteudo = [
            '[CEP]',
            'Quantidade=1',
        ]
    with pytest.raises(ACBrLibCEPErroResposta):
        processar_resposta('\n'.join(conteudo))
