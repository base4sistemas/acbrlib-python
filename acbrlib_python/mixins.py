# -*- coding: utf-8 -*-
#
# acbrlib_python/mixins.py
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

from ctypes import byref
from ctypes import c_int
from ctypes import create_string_buffer

from .constantes import BUFFER_LENGTH
from .proto import ACBrLibMixin
from .proto import read_string_buffer


class ACBrLibCommonMixin(ACBrLibMixin):
    """
    Fornece os "métodos da biblioteca" comuns a todos os sabores de
    bibliotecas ACBrLib:

    * ``XXX_Inicializar``
    * ``XXX_Finalizar``
    * ``XXX_UltimoRetorno``
    * ``XXX_Nome``
    * ``XXX_Versao``

    Este mixin requer que a classe herde de
    :class:`~acbrlib_python.base.ACBrLibReferencia`.
    """

    def inicializar(self, arq_config: str, chave_crypt: str) -> None:
        metodo = f'{self._prefixo}_Inicializar'
        retorno = self._invocar(metodo)(self._b(arq_config), self._b(chave_crypt))
        if retorno == 0:
            return
        else:
            codigos_erro = {
                    -1: 'Falha na inicialização da biblioteca',
                    -5: 'Não foi possível localizar o arquivo INI informado',
                    -6: 'Não foi possível encontrar o diretório do arquivo INI',
                }
            raise self._base_exception(
                    metodo=metodo,
                    retorno=retorno,
                    mensagem=codigos_erro.get(retorno)
                )

    def finalizar(self) -> None:
        metodo = f'{self._prefixo}_Finalizar'
        retorno = self._invocar(metodo)()
        if retorno == 0:
            return
        else:
            codigos_erro = {
                    -2: 'Falha na finalização da biblioteca'
                }
            raise self._base_exception(
                    metodo=metodo,
                    retorno=retorno,
                    mensagem=codigos_erro.get(retorno)
                )

    def ultimo_retorno(self, buffer_len=BUFFER_LENGTH) -> str:
        metodo = f'{self._prefixo}_UltimoRetorno'
        resposta = create_string_buffer(buffer_len)
        tamanho = c_int(buffer_len)
        retorno = self._invocar(metodo)(resposta, byref(tamanho))
        if retorno == 0:
            return self._s(resposta.value)
        else:
            codigos_erro = {
                    -10: 'Falha na execução do método'
                }
            raise self._base_exception(
                    metodo=metodo,
                    retorno=retorno,
                    mensagem=codigos_erro.get(retorno)
                )

    def nome(self) -> str:
        metodo = f'{self._prefixo}_Nome'
        return read_string_buffer(self, metodo, buffer_len=1)

    def versao(self) -> str:
        metodo = f'{self._prefixo}_Versao'
        return read_string_buffer(self, metodo)


class ACBrLibConfigMixin(ACBrLibMixin):
    """
    Fornece os "métodos de configuração" comuns a todos os sabores de
    bibliotecas ACBrLib:

    * ``XXX_ConfigLer``
    * ``XXX_ConfigGravar``
    * ``XXX_ConfigLerValor``
    * ``XXX_ConfigGravarValor``
    * ``XXX_ConfigImportar``
    * ``XXX_ConfigExportar``

    Este mixin requer que a classe herde de
    :class:`~acbrlib_python.base.ACBrLibReferencia`.
    """

    def config_ler(self, arq_config: str) -> None:
        metodo = f'{self._prefixo}_ConfigLer'
        retorno = self._invocar(metodo)(self._b(arq_config))
        if retorno != 0:
            codigos_erro = {
                    -5: 'Não foi possível localizar o arquivo INI informado',
                    -6: 'Não foi possível encontrar o diretório do arquivo INI',
                    -10: 'Houve uma falha na execução do método'
                }
            raise self._base_exception(
                    metodo=metodo,
                    retorno=retorno,
                    mensagem=codigos_erro.get(retorno)
                )

    def config_gravar(self, arq_config: str) -> None:
        metodo = f'{self._prefixo}_ConfigGravar'
        retorno = self._invocar(metodo)(self._b(arq_config))
        if retorno != 0:
            codigos_erro = {
                    -5: 'Não foi possível localizar o arquivo INI informado',
                    -6: 'Não foi possível encontrar o diretório do arquivo INI',
                    -10: 'Houve uma falha na execução do método'
                }
            raise self._base_exception(
                    metodo=metodo,
                    retorno=retorno,
                    mensagem=codigos_erro.get(retorno)
                )

    def config_ler_valor(self, sessao: str, chave: str) -> str:
        metodo = f'{self._prefixo}_ConfigLerValor'
        resposta = create_string_buffer(BUFFER_LENGTH)
        tamanho = c_int(BUFFER_LENGTH)
        retorno = self._invocar(metodo)(
                self._b(sessao),
                self._b(chave),
                resposta,
                byref(tamanho)
            )
        if retorno == 0:
            return self._s(resposta.value)
        else:
            codigos_erro = {
                    -1: 'A biblioteca não foi inicializada',
                    -3: 'Erro ao ler a configuração informada',
                }
            raise self._base_exception(
                    metodo=metodo,
                    retorno=retorno,
                    mensagem=codigos_erro.get(retorno)
                )

    def config_gravar_valor(self, sessao: str, chave: str, valor: str) -> None:
        metodo = f'{self._prefixo}_ConfigGravarValor'
        retorno = self._invocar(metodo)(self._b(sessao), self._b(chave), self._b(valor))
        if retorno != 0:
            codigos_erro = {
                    -1: 'A biblioteca não foi inicializada',
                    -3: 'Erro ao ler a configuração informada',
                }
            raise self._base_exception(
                    metodo=metodo,
                    retorno=retorno,
                    mensagem=codigos_erro.get(retorno)
                )

    def config_importar(self, arq_config: str) -> None:
        metodo = f'{self._prefixo}_ConfigImportar'
        retorno = self._invocar(metodo)(self._b(arq_config))
        if retorno != 0:
            codigos_erro = {
                    -5: 'Não foi possível localizar o arquivo INI informado',
                    -6: 'Não foi possível encontrar o diretório do arquivo INI',
                    -10: 'Houve uma falha na execução do método'
                }
            raise self._base_exception(
                    metodo=metodo,
                    retorno=retorno,
                    mensagem=codigos_erro.get(retorno)
                )

    def config_exportar(self) -> str:
        metodo = f'{self._prefixo}_ConfigExportar'
        resposta = create_string_buffer(BUFFER_LENGTH)
        tamanho = c_int(BUFFER_LENGTH)
        retorno = self._invocar(metodo)(resposta, byref(tamanho))
        if retorno == 0:
            return self._s(resposta.value)
        else:
            codigos_erro = {
                    -10: 'Houve uma falha na execução do método'
                }
            raise self._base_exception(
                    metodo=metodo,
                    retorno=retorno,
                    mensagem=codigos_erro.get(retorno)
                )
