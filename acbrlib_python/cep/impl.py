# -*- coding: utf-8 -*-
#
# acbrlib_python/cep/impl.py
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

import configparser
import io

from contextlib import contextmanager
from ctypes import POINTER
from ctypes import c_char_p
from ctypes import c_int
from typing import List
from typing import Mapping
from typing import Type

from ..constantes import AUTO
from ..excecoes import ACBrLibException
from ..mixins import ACBrLibCommonMixin
from ..mixins import ACBrLibConfigMixin
from ..proto import ACBrLibReferencia
from ..proto import ReferenceLibrary
from ..proto import Signature
from ..proto import common_method_prototypes
from ..proto import config_method_prototypes
from ..proto import read_string_buffer

from .excecoes import ACBrLibCEPException
from .excecoes import ACBrLibCEPErroResposta
from .modelos import Endereco


class ACBrLibCEP(ACBrLibReferencia, ACBrLibCommonMixin, ACBrLibConfigMixin):

    def __init__(
            self,
            prefixo: str,
            biblioteca: ReferenceLibrary,
            prototipos: Mapping[str, Signature],
            base_exception: Type[ACBrLibException]):
        super().__init__(prefixo, biblioteca, prototipos, base_exception)

    @staticmethod
    def usar(caminho_biblioteca, convencao_chamada=AUTO):
        prototypes = {
                **common_method_prototypes('CEP'),
                **config_method_prototypes('CEP'),
                'CEP_BuscarPorCEP': Signature([c_char_p, c_char_p, POINTER(c_int)]),  # eCEP, sResposta, esTamanho,
                'CEP_BuscarPorLogradouro': Signature([
                        c_char_p,  # eCidade
                        c_char_p,  # eTipo_Logradouro
                        c_char_p,  # eLogradouro
                        c_char_p,  # eUF
                        c_char_p,  # eBairro
                        c_char_p,  # sResposta
                        POINTER(c_int),  # esTamanho
                    ])
            }
        instancia = ACBrLibCEP(
                'CEP',
                ReferenceLibrary(
                        caminho_biblioteca,
                        calling_convention=convencao_chamada
                    ),
                prototypes,
                ACBrLibCEPException
            )
        return instancia

    @classmethod
    @contextmanager
    def usando(
            cls,
            caminho_biblioteca,
            convencao_chamada=AUTO,
            arq_config='',
            chave_crypt=''):
        cep = cls.usar(caminho_biblioteca, convencao_chamada=convencao_chamada)
        cep.inicializar(arq_config, chave_crypt)
        try:
            yield cep
        finally:
            cep.finalizar()

    def buscar_por_cep(self, numero: str) -> List[Endereco]:
        """
        Faz uma busca pelo número do CEP.
        :param numero: Número do CEP. Deve possuir exatamente oito digitos e
            pode ou não estar formatado (qualquer caracter que não seja um
            digito, será ignorado).
        :return: Retorna uma lista de :class:`~acbrlib_python.cep.Endereco`.
        :raise ValueError: Se o argumento não possuir oito digitos, após
            todos os caracteres não-digito terem sido removidos.
        """
        cep = ''.join([c for c in numero if c.isdigit()])
        if len(cep) != 8:
            raise ValueError(
                    f'CEP informado nao possui nove digitos: {numero!r}'
                )
        metodo = f'{self._prefixo}_BuscarPorCEP'
        resposta = read_string_buffer(self, metodo, self._b(cep))
        return processar_resposta(resposta)

    def buscar_por_logradouro(
            self,
            tipo_logradouro='',
            logradouro='',
            bairro='',
            municipio='',
            uf='') -> List[Endereco]:
        """
        Faz uma busca por determinados atributos de um endereço. Embora,
        todos os parâmetros sejam opcionais, para que você obtenha um
        resultado mais próximo do que procura, especifique o maior número de
        atributos que conheçer do endereço.

        A precisão do resultado irá depender da qualidade dos valores dos
        atributos informados e do serviço de busca de CEP que estiver usando.

        :param str tipo_logradouro: Opcional. O tipo do logradouro (rua,
            avenida, etc).
        :param str logradouro: Opcional. O nome do logradouro.
        :param str bairro: Opcional. O nome do bairro.
        :param str municipio: Opcional. O nome do município.
        :param str uf: Opcional. A sigla do Estado do município.

        :return: Retorna uma lista de :class:`~acbrlib_python.cep.Endereco`.
        """
        metodo = f'{self._prefixo}_BuscarPorLogradouro'
        resposta = read_string_buffer(
                self,
                metodo,
                self._b(municipio),
                self._b(tipo_logradouro),
                self._b(logradouro),
                self._b(uf),
                self._b(bairro),
            )
        return processar_resposta(resposta)


def processar_resposta(resposta: str) -> List[Endereco]:
    buf = io.StringIO(resposta)
    parser = configparser.ConfigParser()
    parser.read_file(buf)
    section, option = 'CEP', 'Quantidade'
    if not parser.has_option(section, option):
        raise ACBrLibCEPErroResposta(
                'Resposta mal formada; a resposta nao possui a '
                'informacao da quantidade de enderecos encontrados; '
                f'resposta={resposta!r}'
            )
    enderecos = []
    for i in range(parser.getint(section, option)):
        enderecos.append(_endereco(i, parser))
    return enderecos


def _endereco(i: int, parser: configparser.ConfigParser) -> Endereco:
    section = f'Endereco{i + 1}'
    options = [
            'Tipo_Logradouro',
            'Logradouro',
            'Complemento',
            'Bairro',
            'Municipio',
            'UF',
            'CEP',
            'IBGE_Municipio',
            'IBGE_UF',
        ]
    kwargs = {}
    for option in options:
        if not parser.has_option(section, option):
            raise ACBrLibCEPErroResposta(
                'Resposta mal formada; a resposta nao possui a '
                f'informacao {option!r} na secao {section!r}'
            )
        kwargs[option.lower()] = parser.get(section, option)
    return Endereco(**kwargs)
