# -*- coding: utf-8 -*-
#
# acbrlib_python/cep/proto.py
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

import sys

from ctypes import CDLL
from ctypes import POINTER
from ctypes import byref
from ctypes import c_char_p
from ctypes import c_int
from ctypes import create_string_buffer

from typing import Any
from typing import List
from typing import Mapping
from typing import Optional
from typing import Type
from typing import Union

from .constantes import AUTO
from .constantes import BUFFER_LENGTH
from .excecoes import ACBrLibException


class Signature(object):
    """Descreve uma assinatura de função e o tipo de retorno."""

    __slots__ = ('_argtypes', '_restype')

    def __init__(
            self,
            argtypes: List[Any],
            restype: Optional[Any] = None):
        self._argtypes = argtypes[:]
        self._restype = restype or c_int

    @property
    def argtypes(self):
        return self._argtypes[:]

    @property
    def restype(self):
        return self._restype


class ReferenceLibrary(object):

    def __init__(self, library_path, calling_convention=AUTO, lazy_load=True):
        self._path = library_path
        self._calling_convention = calling_convention
        self._lazy_load = lazy_load
        self._ref = None if self._lazy_load else self._load_library()

    @property
    def ref(self):
        if self._ref is None:
            self._load_library()
        return self._ref

    def _load_library(self):
        self._ref = loader(self._path, self._calling_convention)


class ACBrLibMixin:
    pass


class ACBrLibReferencia(object):

    def __init__(
            self,
            prefixo: str,
            biblioteca: ReferenceLibrary,
            prototipos: Mapping[str, Signature],
            base_exception: Type[ACBrLibException],
            encoding: str = 'utf-8'):
        self._prefixo = prefixo
        self._biblioteca = biblioteca
        self._prototipos = prototipos
        self._base_exception = base_exception
        self._encoding = encoding

    def _invocar(self, metodo: str):
        if metodo not in self._prototipos:
            raise ValueError(f'Metodo/funcao desconhecido: {metodo}')
        proto = self._prototipos.get(metodo)
        fptr = getattr(self._biblioteca.ref, metodo)
        fptr.argtypes = proto.argtypes
        fptr.restype = proto.restype
        return fptr

    def _b(self, value: str) -> bytes:
        return value.encode(self._encoding)

    def _s(self, value: bytes) -> str:
        return value.decode(self._encoding)


def read_string_buffer(
        impl: Union[ACBrLibReferencia, ACBrLibMixin],
        method_name: str,
        *args,
        **kwargs):
    """
    Faz uma leitura de um buffer string considerando que o tamanho inicial do
    buffer possa ser insuficiente. Se for o caso, esta função invocará a
    leitura dos dados do último retorno, considerando o tamanho ideal do
    buffer que é indicado durante a primeira tentativa.

    O código usuário desta biblioteca não deveria ter que acessar diretamente
    esta função.

    :param impl: Instância da :class:`ACBrLibReferencia`.
    :param method_name: Nome do método a ser invocado.
    :param args: Os parâmetros posicionais a serem passados para o método.
    :param kwargs: Os parâmetros nomeados a serem passados parao método.
        Se houver um parâmetro chamado ``buffer_len`` (*int*), ele será
        utilizado como referência para o tamanho do buffer a ser lido.
        Se não for informado será usado o valor da constante
        :attr:`acbrlib_python.constantes.BUFFER_LENGTH`.

    :return: Retorna o buffer string já convertido para o encoding da
        implementação definido em :class:`ACBrLibReferencia`.
    """
    buffer_len = kwargs.pop('buffer_len', BUFFER_LENGTH)
    str_buffer = create_string_buffer(buffer_len)
    int_size = c_int(buffer_len)
    mod_args = list(args) + [str_buffer, byref(int_size)]
    retval = getattr(impl, '_invocar')(method_name)(*mod_args, **kwargs)
    if retval == 0:
        if int_size.value > buffer_len:
            return impl.ultimo_retorno(buffer_len=int_size.value)
        else:
            return getattr(impl, '_s')(str_buffer.value)
    else:
        exc = getattr(impl, '_base_exception')
        raise exc(metodo=method_name, retorno=retval)


def common_method_prototypes(
        prefix: str,
        excludes: Optional[List[str]] = None) -> Mapping[str, Signature]:
    """
    Retorna o conjunto dos métodos que aparecem na documentação da
    ACBrLib como "Métodos da Biblioteca". O código usuário desta
    biblioteca não deveria ter que acessar diretamente esta função.

    :param prefix: Prefixo de três letras que identifica a biblioteca,
        como "CEP" ou "NFE" por exemplo.

    :param excludes: Nomes de métodos que devem ser removidos do
        resultado. Deve ser uma lista especificando o nome completo,
        incluindo o prefixo, por exemplo "CEP_UltimoRetorno" para
        que esse protótipo de função seja excluído do resultado.

    :return: Um dicionário contendo os nomes de função e suas
        assinaturas de parâmetros (protótipos de funções).
    """
    prototypes = {
            f'{prefix}_Inicializar': Signature([c_char_p, c_char_p]),  # eArqConfig, eChaveCrypt
            f'{prefix}_Finalizar': Signature([]),
            f'{prefix}_UltimoRetorno': Signature([c_char_p, POINTER(c_int)]),  # sMensagem, esTamanho
            f'{prefix}_Nome': Signature([c_char_p, POINTER(c_int)]),  # sNome, esTamanho
            f'{prefix}_Versao': Signature([c_char_p, POINTER(c_int)]),  # sVersao, esTamanho
        }
    if excludes:
        for name in excludes:
            prototypes.pop(name)
    return prototypes


def config_method_prototypes(
        prefix: str,
        excludes: Optional[List[str]] = None) -> Mapping[str, Signature]:
    """
    Retorna o conjunto dos métodos que aparecem na documentação da
    ACBrLib como "Métodos da Configuração". O código usuário desta
    biblioteca não deveria ter que acessar diretamente esta função.

    :param prefix: Prefixo de três letras que identifica a biblioteca,
        como "CEP" ou "NFE" por exemplo.

    :param excludes: Nomes de métodos que devem ser removidos do
        resultado. Deve ser uma lista especificando o nome completo,
        incluindo o prefixo, por exemplo "DIS_ConfigImportar" para
        que esse protótipo de função seja excluído do resultado.

    :return: Um dicionário contendo os nomes de função e suas
        assinaturas de parâmetros (protótipos de funções).
    """
    prototypes = {
            f'{prefix}_ConfigLer': Signature([c_char_p]),  # eArqConfig
            f'{prefix}_ConfigGravar': Signature([c_char_p]),  # eArqConfig
            f'{prefix}_ConfigLerValor': Signature([
                    c_char_p,  # eSessao
                    c_char_p,  # eChave
                    c_char_p,  # sValor
                    POINTER(c_int)  # esTamanho
                ]),
            f'{prefix}_ConfigGravarValor': Signature([c_char_p, c_char_p, c_char_p]),  # eSessao, eChave, sValor
            f'{prefix}_ConfigImportar': Signature([c_char_p]),  # eArqConfig
            f'{prefix}_ConfigExportar': Signature([c_char_p, POINTER(c_int)]),  # sMensagem, esTamanho
        }
    if excludes:
        for name in excludes:
            prototypes.pop(name)
    return prototypes


def loader(path: str, calling_convention: str) -> CDLL:
    """
    Carrega uma biblioteca (DLL/shared object) no caminho indicado.

    :param path: Caminho completo para biblioteca.

    :param calling_convention: Convenção de chamada.
        Veja as constantes definidas em
        :attr:`acbrlib_python.constantes.CONVENCOES_CHAMADA`.

    :return: Uma referência para ``ctypes.CDLL`` carregada,
        conforme a convenção de chamada (*CDECL* ou *StdCall*).

    """
    name = f'_loader_{calling_convention}'
    loader_func = getattr(sys.modules[__name__], name, None)
    if not loader_func:
        raise ValueError(
                f'Unexpected calling convention; got {calling_convention!r}'
            )
    return loader_func(path, calling_convention)


def _loader_auto(path: str, calling_convention: str) -> CDLL:
    if path.endswith(('.DLL', '.dll')):
        return _loader_stdcall(path, calling_convention)
    else:
        return _loader_cdecl(path, calling_convention)


def _loader_stdcall(path: str, calling_convention: str) -> CDLL:
    from ctypes import WinDLL
    return WinDLL(path)


def _loader_cdecl(path: str, calling_convention: str) -> CDLL:
    return CDLL(path)
