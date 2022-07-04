"""Erlang B, Erlang C and Allen Cunneen calculation package."""

from .erlang_b import erlang_b, erlang_b_table
from .erlang_c import erlang_c, erlang_c_table
from .erlang_c_ext import erlang_c_ext, erlang_c_ext_table
from .ac_approx import ac_approx, ac_approx_table


__title__ = "queuesim"
__version__ = "1.0"
__author__ = "Alexander Herzog"
__email__ = "alexander.herzog@tu-clausthal.de"
__copyright__ = """
Copyright 2022 Alexander Herzog

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
__license__ = "Apache 2.0"
