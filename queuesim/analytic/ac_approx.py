"""Allen Cunneen approximation formula (for a GI/G/c system)"""

from math import sqrt
import pandas as pd
from queuesim.analytic import erlang_c


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


class ac_approx:
    """Allen Cunneen approximation formula (for a GI/G/c system)"""

    def __init__(self, l: float, mu: float, c: int, scv_i: float, scv_s: float) -> None:
        """Allen Cunneen approximation formula (for a GI/G/c system)

        Args:
            l (float): Arrival rate (lambda)
            mu (float): Service rate (mu)
            c (int): Number of operators
            scv_i (float): Squared coefficient of variation of the inter-arrival times
            scv_s (float): Squared coefficient of variation of the service times
        """
        self.__l: float = max(0, l)
        self.__mu: float = max(0, mu)
        self.__a: float = self.__l / self.__mu if self.__mu > 0 else 0
        self.__c: int = max(1, c)
        self.__scv_i: float = max(0, scv_i)
        self.__scv_s: float = max(0, scv_s)
        self.__erlang_enq = erlang_c(self.__l, self.__mu, self.__c).ENQ

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

    @property
    def scv_i(self) -> float:
        """Squared coefficient of variation of the inter-arrival times

        Returns:
            float: Squared coefficient of variation of the inter-arrival times
        """
        return self.__scv_i

    @property
    def scv_s(self) -> float:
        """Squared coefficient of variation of the service times

        Returns:
            float: Squared coefficient of variation of the service times
        """
        return self.__scv_s

    @property
    def ENQ(self) -> float:
        """Mean number of clients in the queue E[N_Q]

        Returns:
            float: Mean number of clients in the queue E[N_Q]
        """
        if self.__a >= self.__c: return 0
        return self.__erlang_enq * (self.__scv_i + self.__scv_s) / 2

    @property
    def EN(self) -> float:
        """Mean number of clients in the system (waiting and in service process) E[N]

        Returns:
            float: Mean number of clients in the system (waiting and in service process) E[N]
        """
        if self.__a >= self.__c: return 0
        return self.__erlang_enq * (self.__scv_i + self.__scv_s) / 2 + self.__a

    @property
    def EW(self) -> float:
        """Mean waiting time E[W]

        Returns:
            float: Mean waiting time E[W]
        """
        if self.__a >= self.__c: return 0
        return self.__erlang_enq * 1 / self.__l * (self.__scv_i + self.__scv_s) / 2

    @property
    def EV(self) -> float:
        """Mean residence time ( = waiting time + service time) E[V]

        Returns:
            float: Mean residence time ( = waiting time + service time) E[V]
        """
        if self.__a >= self.__c: return 0
        return self.__erlang_enq / self.__l * (self.__scv_i + self.__scv_s) / 2 + 1 / self.__mu


def ac_approx_table(parameters: list) -> pd.DataFrame:
    """Calculates the Allen Cunneen approximation results for multiple parameter sets

    Args:
        parameters (list[tuple[float, float, int, float, float]]): List of tuples containing the values for lambda, mu, c, SCV[I] and SCV[S] each

    Returns:
        pd.DataFrame: Allen Cunneen approximation results table
    """
    l, mu, a, c, rho, cv_i, cv_s, scv_i, scv_s, ENQ, EN, EW, EV = [], [], [], [], [], [], [], [], [], [], [], [], []

    for parameter in parameters:
        ac = ac_approx(parameter[0], parameter[1], parameter[2], parameter[3], parameter[4])
        l.append(ac.l)
        mu.append(ac.mu)
        a.append(ac.a)
        c.append(ac.c)
        rho.append(ac.rho)
        cv_i.append(sqrt(ac.scv_i))
        cv_s.append(sqrt(ac.scv_s))
        scv_i.append(ac.scv_i)
        scv_s.append(ac.scv_s)
        ENQ.append(ac.ENQ)
        EN.append(ac.EN)
        EW.append(ac.EW)
        EV.append(ac.EV)

    return pd.DataFrame({'lambda': l, 'mu': mu, 'a': a, 'c': c, 'rho': rho, 'CV[I]': cv_i, 'CV[S]': cv_s, 'SCV[I]': scv_i, 'SCV[S]': scv_s, 'E[N_Q]': ENQ, 'E[N]': EN, 'E[W]': EW, 'E[V]': EV})
