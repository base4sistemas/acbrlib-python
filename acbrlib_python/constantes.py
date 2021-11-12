# -*- coding: utf-8 -*-
#
# acbrlib_python/constantes.py
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

from .cep.constantes import *  # noqa:

AUTO = 'auto'
STANDARD_C = 'cdecl'
WINDOWS_STDCALL = 'stdcall'

CALLING_CONVENTIONS = (
        (AUTO, 'Automático (pela extensão)'),
        (STANDARD_C, 'C Padrão (Cdecl)'),
        (WINDOWS_STDCALL, 'Windows Padrão (StdCall)'),
    )


CONVENCOES_CHAMADA = CALLING_CONVENTIONS

BUFFER_LENGTH = 1024
