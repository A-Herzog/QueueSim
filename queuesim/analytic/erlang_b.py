"""Erlang B formula (for a M/M/c/c system)"""

from typing import Optional
import pandas as pd
from .tools import power_factorial


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


class erlang_b:
    """Erlang B formula (for a M/M/c/c system)"""

    def __init__(self, a: float, c: int) -> None:
        """Erlang B formula (for a M/M/c/c system)

        Args:
            a (float): Workload ( = lambda/mu)
            c (int): Number of operators
        """
        self.__a: float = max(0, a)
        self.__c: int = max(1, c)
        self.__p_blocked: Optional[float] = None
        self.__EN: Optional[float] = None

    @property
    def a(self) -> float:
        """Workload ( = lambda/mu)

        Returns:
            float: Workload ( = lambda/mu)
        """
        return self.__a

    @property
    def c(self) -> int:
        """Number of operators

        Returns:
            int: Number of operators
        """
        return self.__c

    @property
    def rho_offered(self) -> float:
        """Offered utilization (rho = a/c)

        Returns:
            float: Offered utilization (rho = a/c)
        """
        return self.__a / self.__c

    @property
    def EN(self) -> float:
        if self.__EN is None:
            nominator: float = sum([power_factorial(self.__a, n) for n in range(self.__c + 1)])
            self.__EN = sum([power_factorial(self.__a, n) * n for n in range(self.__c + 1)]) / nominator
        return self.__EN

    @property
    def rho_real(self) -> float:
        """Real utilization ( = E[N]/c)

        Returns:
            float: Real utilization ( = E[N]/c)
        """
        return self.EN / self.__c

    @property
    def p_blocked(self) -> float:
        """Probability of arriving clients being blocked P(N = c)

        Returns:
            float: P(N = c)
        """
        if self.__p_blocked is None:
            nominator: float = sum([power_factorial(self.__a, n) for n in range(self.__c + 1)])
            self.__p_blocked = power_factorial(self.__a, self.__c) / nominator
        return self.__p_blocked


def erlang_b_table(parameters: list) -> pd.DataFrame:
    """Calculates the Erlang B results for multiple parameter sets

    Args:
        parameters (list[tuple[float, int]]): List of tuples containing the values for a and c each

    Returns:
        pd.DataFrame: Erlang B results table
    """
    a, c, rho_offered, rho_real, EN, p_blocked = [], [], [], [], [], []

    for parameter in parameters:
        erl = erlang_b(parameter[0], parameter[1])
        a.append(erl.a)
        c.append(erl.c)
        rho_offered.append(erl.rho_offered)
        rho_real.append(erl.rho_real)
        EN.append(erl.EN)
        p_blocked.append(erl.p_blocked)

    return pd.DataFrame({'a': a, 'c': c, 'rho_offered': rho_offered, 'rho_real': rho_real, 'E[N]': EN, 'P(blocked)': p_blocked})
