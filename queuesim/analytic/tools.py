"""Auxiliary functions for calculation of Erlang B and Erlang C formulas."""


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


from math import prod


def power_factorial(x: float, n: int) -> float:
    """Calculates the product over x/i für i = 1..n

    Args:
        x (float): x
        n (int): n

    Returns:
        float: Product over x/i für i = 1..n
    """
    if n == 0:
        return 1

    return prod([x / i for i in range(1, n + 1)])
