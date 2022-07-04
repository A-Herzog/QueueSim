"""Erlang C formula (for a M/M/c system)"""

from math import exp
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


class erlang_c:
    """Erlang C formula (for a M/M/c system)"""

    def __init__(self, l: float, mu: float, c: int) -> None:
        """Erlang C formula (for a M/M/c system)

        Args:
            l (float): Arrival rate (lambda)
            mu (float): Service rate (mu)
            c (int): Number of operators
        """
        self.__l: float = max(0, l)
        self.__mu: float = max(0, mu)
        self.__a: float = self.__l / self.__mu if self.__mu > 0 else 0
        self.__c: int = max(1, c)

        result: float = sum([power_factorial(self.__a, K) for K in range(self.__c)])
        result = result + power_factorial(self.__a, self.__c) * self.__c / (self.__c - self.__a)
        self.__p0: float = 1 / result if result > 0 else 0

        self.__pn: dict[int, float] = {0: self.__p0}

        self.__P1: float = power_factorial(self.__a, self.__c) * self.__c / (self.__c - self.__a) * self.__p0

    @property
    def l(self) -> float:
        """Arrival rate (lambda)

        Returns:
            float: Arrival rate (lambda)
        """
        return self.__l

    @property
    def mu(self) -> float:
        """Service rate (mu)

        Returns:
            float: Service rate (mu)
        """
        return self.__mu

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
    def rho(self) -> float:
        """Utilization (rho)

        Returns:
            float: Utilization (rho)
        """
        return self.__a / self.__c

    def pn(self, n: int) -> float:
        """Probability for n clients in the system P(N = n)

        Args:
            n (int): Number of clients in the system

        Returns:
            float: Probability for n clients in the system P(N = n)
        """
        if n in self.__pn: return self.__pn[n]

        if n <= self.__c:
            result = power_factorial(self.__a, n) * self.__p0
        else:
            result = power_factorial(self.__a, self.__c) * (self.__a / self.__c)**(n - self.__c) * self.__p0

        self.__pn[n] = result
        return result

    @property
    def P1(self) -> float:
        """P1 in Erlang C formular

        Returns:
            float: P1 in Erlang C formular
        """
        return self.__P1

    def Pt(self, t: float) -> float:
        """Probability that clients have to wait t or less seconds ( = Erlang C formula)

        Args:
            t (float): Maximum waiting time

        Returns:
            float: P(W <= t)
        """
        if self.__a >= self.__c: return 0
        return 1 - self.__P1 * exp(-(self.__c - self.__a) * self.__mu * t)

    @property
    def ENQ(self) -> float:
        """Mean number of clients in the queue E[N_Q]

        Returns:
            float: Mean number of clients in the queue E[N_Q]
        """
        if self.__a >= self.__c: return 0
        return self.__P1 * self.__a / (self.__c - self.__a)

    @property
    def EN(self) -> float:
        """Mean number of clients in the system (waiting and in service process) E[N]

        Returns:
            float: Mean number of clients in the system (waiting and in service process) E[N]
        """
        if self.__a >= self.__c: return 0
        return self.__P1 * self.__a / (self.__c - self.__a) + self.__a

    @property
    def EW(self) -> float:
        """Mean waiting time E[W]

        Returns:
            float: Mean waiting time E[W]
        """
        if self.__a >= self.__c: return 0
        return self.__P1 / (self.__c * self.__mu - self.__l)

    @property
    def EV(self) -> float:
        """Mean residence time ( = waiting time + service time) E[V]

        Returns:
            float: Mean residence time ( = waiting time + service time) E[V]
        """
        if self.__a >= self.__c: return 0
        return self.__P1 / (self.__c * self.__mu - self.__l) + 1 / self.__mu


def erlang_c_table(parameters: list) -> pd.DataFrame:
    """Calculates the Erlang C results for multiple parameter sets

    Args:
        parameters (list[tuple[float, float, int]]): List of tuples containing the values for lambda, mu and c each

    Returns:
        pd.DataFrame: Erlang C results table
    """
    l, mu, a, c, rho, ENQ, EN, EW, EV = [], [], [], [], [], [], [], [], []

    for parameter in parameters:
        erl = erlang_c(parameter[0], parameter[1], parameter[2])
        l.append(erl.l)
        mu.append(erl.mu)
        a.append(erl.a)
        c.append(erl.c)
        rho.append(erl.rho)
        ENQ.append(erl.ENQ)
        EN.append(erl.EN)
        EW.append(erl.EW)
        EV.append(erl.EV)

    return pd.DataFrame({'lambda': l, 'mu': mu, 'a': a, 'c': c, 'rho': rho, 'E[N_Q]': ENQ, 'E[N]': EN, 'E[W]': EW, 'E[V]': EV})
