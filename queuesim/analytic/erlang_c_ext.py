"""Extended Erlang C formula (for a M/M/c/K + M system with impatience)"""

from scipy.special import gammainc
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


class erlang_c_ext:
    """Extended Erlang C formula (for a M/M/c/K + M system with impatience)"""

    def __init__(self, l: float, mu: float, nu: float, c: int, K: int) -> None:
        """Extended Erlang C formula (for a M/M/c/K + M system with impatience)

        Args:
            l (float): Arrival rate (lambda)
            mu (float): Service rate (mu)
            nu (float): Cancelation rate (nu)
            c (int): Number of operators
            K (int): Maximum system size
        """
        self.__l: float = max(0, l)
        self.__mu: float = max(0, mu)
        self.__a: float = self.__l / self.__mu if self.__mu > 0 else 0
        self.__nu: float = max(0, nu)
        self.__c: int = max(1, c)
        self.__K: int = max(self.__c, K)

        self.__Cn: dict[int, float] = {}

        p0 = 1 / sum([self.Cn(i) for i in range(self.__K + 1)])
        self.__pn: dict[int, float] = {0: p0}

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
    def nu(self) -> float:
        """Cancelation rate (nu)

        Returns:
            float: Cancelation rate (mu)
        """
        return self.__nu

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
    def K(self) -> int:
        """Maximum system size

        Returns:
            int: Maximum system size
        """
        return self.__K

    def Cn(self, n: int) -> float:
        """Factor C(n) for calculation extended Erlang C formula

        Args:
            n (int): Number of clients in the system

        Returns:
            float: C(n)
        """
        if n in self.__Cn: return self.__Cn[n]
        if n <= self.__c:
            value = power_factorial(self.__l / self.__mu, n)
        else:
            value = power_factorial(self.__l / self.__mu, self.__c)
            for i in range(1, n - self.__c + 1): value = value * self.__l / (self.__c * self.__mu + i * self.__nu)

        self.__Cn[n] = value
        return value

    def pn(self, n: int) -> float:
        """Probability for n clients in the system P(N = n)

        Args:
            n (int): Number of clients in the system

        Returns:
            float: Probability for n clients in the system P(N = n)
        """
        if n > self.__K: return 0

        if n in self.__pn: return self.__pn[n]

        value = self.Cn(n) * self.__pn[0]
        self.__pn[n] = value
        return value

    @property
    def p_blocked(self) -> float:
        """Probability of arriving clients being blocked P(N = K)

        Returns:
            float: P(N = K)
        """
        return self.pn(self.__K)

    @property
    def PA(self) -> float:
        """Cancelation probability P(A)

        Returns:
            float: Cancelation probability P(A)
        """
        p0 = self.pn(0)
        input_reject = self.pn(self.__K)
        return sum([self.__nu / (self.__l * (1 - input_reject)) * (n - self.__c) * p0 * self.Cn(n) for n in range(self.__c + 1, self.__K + 1)])

    def Pt(self, t: float) -> float:
        """Probability that clients have to wait t or less seconds ( = extended Erlang C formula)

        Args:
            t (float): Maximum waiting time

        Returns:
            float: P(W <= t)
        """
        p0 = self.pn(0)

        if p0 == 0:
            p = 1
        else:
            p = 1 - p0 * self.Cn(self.__K)

        for n in range(self.__c, self.__K):
            a = n - self.__c + 1
            x = (self.__c * self.__mu + self.__nu) * t
            g = 1 - gammainc(a, x)
            p = p - p0 * self.Cn(n) * g

        return p

    @property
    def rho_real(self) -> float:
        """Real utilization ( = E[N]/c)

        Returns:
            float: Real utilization ( = E[N]/c)
        """
        return (self.EN - self.ENQ) / self.__c

    @property
    def ENQ(self) -> float:
        """Mean number of clients in the queue E[N_Q]

        Returns:
            float: Mean number of clients in the queue E[N_Q]
        """
        p0 = self.pn(0)
        return sum([p0 * (n - self.__c) * self.Cn(n) for n in range(self.__c + 1, self.__K + 1)])

    @property
    def EN(self) -> float:
        """Mean number of clients in the system (waiting and in service process) E[N]

        Returns:
            float: Mean number of clients in the system (waiting and in service process) E[N]
        """
        p0 = self.pn(0)
        return sum([p0 * n * self.Cn(n) for n in range(1, self.__K + 1)])

    @property
    def EW(self) -> float:
        """Mean waiting time E[W]

        Returns:
            float: Mean waiting time E[W]
        """
        return self.ENQ / self.__l

    @property
    def EV(self) -> float:
        """Mean residence time ( = waiting time + service time) E[V]

        Returns:
            float: Mean residence time ( = waiting time + service time) E[V]
        """
        return self.EN / self.__l


def erlang_c_ext_table(parameters: list) -> pd.DataFrame:
    """Calculates the extended Erlang C results for multiple parameter sets

    Args:
        parameters (list[tuple[float, float, float, int, int]]): List of tuples containing the values for lambda, mu, nu, c and K each

    Returns:
        pd.DataFrame: Extended Erlang C results table
    """
    l, mu, nu, a, c, K, rho_offered, rho_real, p_blocked, PA, ENQ, EN, EW, EV = [], [], [], [], [], [], [], [], [], [], [], [], [], []

    for parameter in parameters:
        erl = erlang_c_ext(parameter[0], parameter[1], parameter[2], parameter[3], parameter[4])
        l.append(erl.l)
        mu.append(erl.mu)
        nu.append(erl.nu)
        a.append(erl.a)
        c.append(erl.c)
        K.append(erl.K)
        rho_offered.append(erl.rho_offered)
        rho_real.append(erl.rho_real)
        p_blocked.append(erl.p_blocked)
        PA.append(erl.PA)
        ENQ.append(erl.ENQ)
        EN.append(erl.EN)
        EW.append(erl.EW)
        EV.append(erl.EV)

    return pd.DataFrame({'lambda': l, 'mu': mu, 'nu': nu, 'a': a, 'c': c, 'K': K, 'rho_offered': rho_offered, 'rho_real': rho_real, 'P(blocked)': p_blocked, 'P(A)': PA, 'E[N_Q]': ENQ, 'E[N]': EN, 'E[W]': EW, 'E[V]': EV})
