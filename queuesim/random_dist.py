"""Functions for generating lambdas that produce pseudorandom numbers according to certain distributions."""

from typing import Callable, Union
import math
import random
import scipy.stats as stats


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


def exp(mean: float, as_lambda: bool = False) -> Union[str, Callable[[], float]]:
    """Generates a lambda expression or a string that can be evaluated to a lambda expression, with a pseudorandom number generator for the exponential distribution

    Args:
        mean (float): Mean = standard deviation
        as_lambda (bool, optional): Should a lambda expression (True) or a string (False) be returned? Defaults to False.

    Returns:
        Union[str, Callable[[], float]]: Lambda expression or string with lambda expression for random number generator
    """
    assert mean > 0
    if as_lambda:
        return lambda: random.expovariate(1 / mean)
    else:
        return "lambda: random.expovariate(1/" + str(mean) + ")"


def log_normal(mean: float, std: float, as_lambda: bool = False) -> Union[str, Callable[[], float]]:
    """Generates a lambda expression or a string that can be evaluated to a lambda expression, with a pseudorandom number generator for the log-normal distribution

    Args:
        mean (float): Mean
        std (float): Standard deviation
        as_lambda (bool, optional): Should a lambda expression (True) or a string (False) be returned? Defaults to False.

    Returns:
        Union[str, Callable[[], float]]: Lambda expression or string with lambda expression for random number generator
    """
    assert std >= 0
    mu: float = math.log(mean**2 / math.sqrt(std**2 + mean**2))
    sigma: float = math.sqrt(math.log((std**2 / mean**2) + 1))
    if as_lambda:
        return lambda: random.lognormvariate(mu, sigma)
    else:
        return "lambda: random.lognormvariate(" + str(mu) + ", " + str(sigma) + ")"


def gamma(mean: float, std: float, as_lambda: bool = False) -> Union[str, Callable[[], float]]:
    """Generates a lambda expression or a string that can be evaluated to a lambda expression, with a pseudorandom number generator for the gamma distribution

    Args:
        mean (float): Mean
        std (float): Standard deviation
        as_lambda (bool, optional): Should a lambda expression (True) or a string (False) be returned? Defaults to False.

    Returns:
        Union[str, Callable[[], float]]: Lambda expression or string with lambda expression for random number generator
    """
    assert mean > 0
    assert std > 0
    beta: float = mean / (std ** 2)
    alpha: float = mean * beta
    beta: float = 1 / beta
    if as_lambda:
        return lambda: random.gammavariate(alpha, beta)
    else:
        return "lambda: random.gammavariate(" + str(alpha) + ", " + str(beta) + ")"


def erlang(mean: float, std: float, as_lambda: bool = False) -> Union[str, Callable[[], float]]:
    """Generates a lambda expression or a string that can be evaluated to a lambda expression, with a pseudorandom number generator for the Erlang distribution

    Args:
        mean (float): Mean
        std (float): Standard deviation
        as_lambda (bool, optional): Should a lambda expression (True) or a string (False) be returned? Defaults to False.

    Returns:
        Union[str, Callable[[], float]]: Lambda expression or string with lambda expression for random number generator
    """
    assert mean > 0
    assert std > 0

    scale: float = std**2 / mean
    a: int = max(1, round(mean / scale))
    if as_lambda:
        return lambda: stats.erlang.rvs(a, scale=scale)
    else:
        return "lambda: stats.erlang.rvs(" + str(a) + ", scale = " + str(scale) + ")"


def uniform(low: float, high: float, as_lambda: bool = False) -> Union[str, Callable[[], float]]:
    """Generates a lambda expression or a string that can be evaluated to a lambda expression, with a pseudorandom number generator for the uniform distribution

    Args:
        low (float): Minimum value of the support
        high (float): Maximum value of the support
        as_lambda (bool, optional): Should a lambda expression (True) or a string (False) be returned? Defaults to False.

    Returns:
        Union[str, Callable[[], float]]: Lambda expression or string with lambda expression for random number generator
    """
    if as_lambda:
        return lambda: random.uniform(low, high)
    else:
        return "lambda: random.uniform(" + str(low) + ", " + str(high) + ")"


def triangular(low: float, most_likely: float, high: float, as_lambda: bool = False) -> Union[str, Callable[[], float]]:
    """Generates a lambda expression or a string that can be evaluated to a lambda expression, with a pseudorandom number generator for the triangular distribution

    Args:
        low (float): Minimum value of the support
        most_likely (float): x value of the highest density
        high (float): Maximum value of the support
        as_lambda (bool, optional): Should a lambda expression (True) or a string (False) be returned? Defaults to False.

    Returns:
        Union[str, Callable[[], float]]: Lambda expression or string with lambda expression for random number generator
    """
    if as_lambda:
        return lambda: random.triangular(low, high, most_likely)
    else:
        return "lambda: random.triangular(" + str(low) + ", " + str(high) + ", " + str(most_likely) + ")"


def trapezoid(a: float, b: float, c: float, d: float, as_lambda: bool = False) -> Union[str, Callable[[], float]]:
    """Generates a lambda expression or a string that can be evaluated to a lambda expression, with a pseudorandom number generator for the trapezoid distribution

    Args:
        a (float): Minimum value of the support
        b (float): x value of the left side of the highest density
        c (float): x value of the right side of the highest density
        d (float): Maximum value of the support
        as_lambda (bool, optional): Should a lambda expression (True) or a string (False) be returned? Defaults to False.

    Returns:
        Union[str, Callable[[], float]]: Lambda expression or string with lambda expression for random number generator
    """
    c_shape = (b - a) / (d - a)
    d_shape = (c - a) / (d - a)
    loc = a
    scale = d - a
    if as_lambda:
        return lambda: stats.trapezoid.rvs(c_shape, d_shape, loc=loc, scale=scale)
    else:
        return "lambda: stats.trapezoid.rvs(" + str(c_shape) + ", " + str(d_shape) + ", loc=" + str(loc) + ", scale=" + str(scale) + ")"


def beta(alpha: float, beta: float, low: float, high: float, as_lambda: bool = False) -> Union[str, Callable[[], float]]:
    """Generates a lambda expression or a string that can be evaluated to a lambda expression, with a pseudorandom number generator for the beta distribution

    Args:
        alpha (float): Alpha parameter of the beta distribution
        beta (float): Beta parameter of the beta distribution
        low (float): Minimum value of the support
        high (float): Maximum value of the support
        as_lambda (bool, optional): Should a lambda expression (True) or a string (False) be returned? Defaults to False.

    Returns:
        Union[str, Callable[[], float]]: Lambda expression or string with lambda expression for random number generator
    """
    loc = low
    scale = high - loc
    if as_lambda:
        return lambda: stats.beta.rvs(alpha, beta, loc=loc, scale=scale)
    else:
        return "lambda: stats.beta.rvs(" + str(alpha) + ", " + str(beta) + ", loc=" + str(loc) + ", scale=" + str(scale) + ")"


def half_normal(low: float, mean: float, as_lambda: bool = False) -> Union[str, Callable[[], float]]:
    """Generates a lambda expression or a string that can be evaluated to a lambda expression, with a pseudorandom number generator for the half-normal distribution

    Args:
        low (float): Minimum value of the support
        mean (float): Mean of the half-normal distribution
        as_lambda (bool, optional): Should a lambda expression (True) or a string (False) be returned? Defaults to False.

    Returns:
        Union[str, Callable[[], float]]: Lambda expression or string with lambda expression for random number generator
    """
    assert mean > low
    loc = low
    scale = (mean - low) * math.sqrt(math.pi / 2)
    if as_lambda:
        return lambda: stats.halfnorm.rvs(loc=loc, scale=scale)
    else:
        return "lambda: stats.halfnorm.rvs(loc=" + str(loc) + ", scale=" + str(scale) + ")"


def deterministic(mean: float, as_lambda: bool = False) -> Union[str, Callable[[], float]]:
    """Generates a lambda expression or a string that can be evaluated to a lambda expression, which returns a fixed number (which is a special case of a pseudorandom number generator)

    Args:
        mean (float): Mean (=fixed number)
        as_lambda (bool, optional): Should a lambda expression (True) or a string (False) be returned? Defaults to False.

    Returns:
        Union[str, Callable[[], float]]: Lambda expression or string with lambda expression for random number generator
    """
    if as_lambda:
        return lambda: mean
    else:
        return "lambda: " + str(mean)


def empirical_helper(rate_sum, values: dict) -> float:
    rnd: float = random.random() * rate_sum
    s: float = 0
    for key in values:
        s += values[key]
        if s >= rnd:
            return float(key)
    return 0


def empirical(values: dict, as_lambda: bool = False) -> Union[str, Callable[[], float]]:
    """Generates a lambda expression or a string that can be evaluated to a lambda expression, with a pseudorandom number generator for an empirical distribution

    Args:
        values (dict[float, float]): A dict containing pairs: value -> rate
        as_lambda (bool, optional): Should a lambda expression (True) or a string (False) be returned? Defaults to False.

    Returns:
        Union[str, Callable[[], float]]: Lambda expression or string with lambda expression for random number generator
    """
    rate_sum: float = sum(values.values())
    if as_lambda:
        return lambda: empirical_helper(rate_sum, values)
    else:
        return "lambda: empirical_helper(" + str(rate_sum) + ", " + str(values) + ")"
