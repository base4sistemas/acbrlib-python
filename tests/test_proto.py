# -*- coding: utf-8 -*-
#
# tests/test_proto.py
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

from acbrlib_python import proto
from acbrlib_python.constantes import AUTO
from acbrlib_python.proto import ReferenceLibrary
from acbrlib_python.proto import Signature
from acbrlib_python.proto import common_method_prototypes
from acbrlib_python.proto import config_method_prototypes


class _FakeCDLL:

    def __init__(self, path, calling_convention):
        self._path = path
        self._calling_convention = calling_convention


def test_referencelibrary_class_auto_cdecl(monkeypatch):
    def mockreturn(path, calling_convention):
        return _FakeCDLL(path, calling_convention)
    monkeypatch.setattr(proto, 'loader', mockreturn)
    lib = ReferenceLibrary('/var/lib.so')
    assert isinstance(lib.ref, _FakeCDLL)
    assert lib._path == '/var/lib.so'
    assert lib._calling_convention == AUTO
    assert lib._lazy_load is True


def test_signature_class():
    original_args = ['a', 'b', 'c']
    s = Signature(original_args, restype='t')
    assert 'a' in s.argtypes
    assert 'b' in s.argtypes
    assert 'c' in s.argtypes
    assert 't' == s.restype

    # a lista em argtypes deve ser uma cópia da lista de
    # argumentos informada e, portanto, imutável externamente
    original_args.append('x')
    assert 'x' not in s.argtypes

    ext_args = s.argtypes
    ext_args.append('x')
    assert 'x' not in s.argtypes


def test_common_method_prototypes_all():
    res = common_method_prototypes('CEP')
    assert 'CEP_Inicializar' in res
    assert 'CEP_Finalizar' in res
    assert 'CEP_UltimoRetorno' in res
    assert 'CEP_Nome' in res
    assert 'CEP_Versao' in res


def test_common_method_prototypes_excluded():
    res = common_method_prototypes('CEP', excludes=['CEP_Finalizar'])
    assert 'CEP_Finalizar' not in res


def test_config_method_prototypes_all():
    res = config_method_prototypes('NFE')
    assert 'NFE_ConfigLer' in res
    assert 'NFE_ConfigGravar' in res
    assert 'NFE_ConfigLerValor' in res
    assert 'NFE_ConfigGravarValor' in res
    assert 'NFE_ConfigImportar' in res
    assert 'NFE_ConfigExportar' in res


def test_config_method_prototypes_excluded():
    res = config_method_prototypes(
            'DIS',
            excludes=['DIS_ConfigImportar', 'DIS_ConfigExportar']
        )
    assert 'DIS_ConfigImportar' not in res
    assert 'DIS_ConfigExportar' not in res
