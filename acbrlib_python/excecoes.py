# -*- coding: utf-8 -*-
#
# acbrlib_python/excecoes.py
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

from unidecode import unidecode


class ACBrLibException(Exception):
    def __init__(self, metodo=None, retorno=None, mensagem=None):
        if not mensagem:
            mensagem = f'Código de retorno inesperado: {retorno!r}'
        mensagem = f'{mensagem} (método {metodo!r} retornou {retorno!r})'
        self._metodo = metodo
        self._retorno = retorno
        super().__init__(unidecode(mensagem))

    @property
    def metodo(self):
        return self._metodo

    @property
    def retorno(self):
        return self._retorno
