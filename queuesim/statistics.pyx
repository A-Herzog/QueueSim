"""Classes for recording measured values for statistics"""

from typing import Any, Optional
from math import sqrt
import collections
import numpy as np  # Comment out this line for use with PyPy
import cython


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


discrete_record_np_cache_size: cython.int = 8_192
discrete_record_histogram_steps: cython.int = 128


@cython.cclass
class RecordDiscrete:
    """Captures discrete measured values (such as individual waiting times)."""
    __slots__ = ("__count", "__sum", "__sum2", "__min", "__max", "__cache", "__cacheSize", "__cacheUsed", "__histogram", "__histogram_stepwide")

    __count: cython.int
    __sum: cython.float
    __sum2: cython.float
    __min: cython.float
    __max: cython.float
    __cache: Any
    __cacheSize: cython.int
    __cacheUsed: cython.int
    __histogram: list[cython.float]
    __histogram_stepwide: cython.int

    def __init__(self) -> None:
        """Captures discrete measured values (such as individual waiting times)."""
        global discrete_record_histogram_steps
        global discrete_record_np_cache_size
        self.__count: cython.int = 0
        self.__sum: cython.float = 0
        self.__sum2: cython.float = 0
        self.__min: cython.float = 0
        self.__max: cython.float = 0
        try:
            self.__cache = np.zeros(discrete_record_np_cache_size)
            self.__cacheSize = len(self.__cache)
        except NameError:
            self.__cache = []
            self.__cacheSize = 0
        self.__cacheUsed = 0
        self.__histogram: list[cython.float] = []
        if discrete_record_histogram_steps > 0:
            self.__histogram = [0 for i in range(discrete_record_histogram_steps)]
            self.__histogram_stepwide = 1
        else:
            self.__histogram_stepwide = -1

    @cython.ccall
    def __process_cache(self):
        # Only process cache, if there are values in the cache
        if self.__cacheUsed == 0: return

        # Is full array used?
        if self.__cacheUsed == self.__cacheSize:
            cache = self.__cache
        else:
            cache = self.__cache[:self.__cacheUsed]

        # Process min/max first
        if self.__count == 0:
            self.__min = float(np.min(cache))
            self.__max = float(np.max(cache))
        else:
            self.__min = min(self.__min, float(np.min(cache)))
            self.__max = max(self.__min, float(np.max(cache)))

        self.__count += len(cache)
        self.__sum += float(np.sum(cache))
        self.__sum2 += np.sum(np.power(cache, 2))

        # Reset cache usage
        self.__cacheUsed = 0

    @cython.ccall
    def record(self, value: cython.float):
        """Captures a single measured value.

        Args:
            value (float): New measured value
        """
        global discrete_record_histogram_steps

        if self.__cacheSize == 0:
            # Direct recording
            self.__count += 1
            self.__sum += value
            self.__sum2 += value**2
            if self.__count == 1:
                self.__min = value
                self.__max = value
            else:
                if value < self.__min: self.__min = value
                if value > self.__max: self.__max = value
        else:
            if self.__cacheUsed == self.__cacheSize: self.__process_cache()
            self.__cache[self.__cacheUsed] = value
            self.__cacheUsed += 1

        if discrete_record_histogram_steps > 0:
            index: cython.int = round(value) // self.__histogram_stepwide
            b: cython.int = len(self.__histogram)
            a: cython.int = int(b / 2)
            while index >= b:
                for i in range(a): self.__histogram[i] = self.__histogram[2 * i] + self.__histogram[2 * i + 1]
                for i in range(a, b): self.__histogram[i] = 0
                self.__histogram_stepwide *= 2
                index = int(index / 2)
            self.__histogram[index] += 1

    def done_recording(self) -> None:
        """Terminates caching system before serializing the object.
        (Calling this method is not needed for normal processing.)
        """
        self.__process_cache()
        self.__cache = []

    @property
    def count(self) -> int:
        """Number of recorded values.

        Returns:
            int: Number of recorded values
        """
        self.__process_cache()
        return self.__count

    @property
    def mean(self) -> float:
        """Mean value over the recorded values.

        Returns:
            float: Mean value over the recorded values (or 0 if no value has been recorded yet)
        """
        self.__process_cache()
        return self.__sum / self.__count if self.__count > 0 else 0

    @property
    def sd(self) -> float:
        """Standard deviation of the recorded values.

        Returns:
            float: Standard deviation of the recorded values (or 0, if less than 2 values have been recorded)
        """
        self.__process_cache()
        if self.__count < 2: return 0
        var: cython.float = self.__sum2 / (self.__count - 1) - (self.__sum**2) / self.__count / (self.__count - 1)
        return sqrt(max(0, var))

    @property
    def cv(self) -> float:
        """Coefficient of variation of the recorded values.

        Returns:
            float: Coefficient of variation of the recorded values (or 0 if the mean is 0)
        """
        self.__process_cache()
        if self.mean == 0: return 0
        return self.sd / self.mean

    @property
    def min(self) -> float:
        """Minimum of the recorded values.

        Returns:
            float: Minimum of the recorded values (or 0 if no values have been recorded yet)
        """
        self.__process_cache()
        return self.__min

    @property
    def max(self) -> float:
        """Maximum of the recorded values.

        Returns:
            float: Maximum of the recorded values (or 0 if no values have been recorded yet)
        """
        self.__process_cache()
        return self.__max

    @property
    def histogram(self) -> list:
        """Frequency distribution of the recorded values

        Returns:
            list[float]: Frequency distribution of the recorded values
        """
        return self.__histogram

    @property
    def histogram_stepwide(self) -> int:
        """Wide of each entry in the frequency distribution

        Returns:
            int: Wide of each entry in the frequency distribution
        """
        return self.__histogram_stepwide

    def __str__(self) -> str:
        return "count = {}, mean = {:.1f}, sd = {:.1f}, cv = {:.1f}, min = {:.1f}, max = {:.1f}".format(self.count, self.mean, self.sd, self.cv, self.min, self.max)

    @property
    def info(self) -> str:
        """Short information about the main indicators

        Returns:
            str: Short information about the main indicators
        """
        return "mean = {:.1f}, sd = {:.1f}, cv = {:.1f}".format(self.mean, self.sd, self.cv)


@cython.cclass
class RecordContinuous:
    """Records continuous trends (e.g. the number of clients in the system over time)."""
    __slots__ = ("__lastTime", "__lastValue", "__timeSum", "__valueSum", "__min", "__max", "__recordedTimestamps", "__recordedValues")

    __lastTime: cython.float
    __lastValue: cython.float
    __timeSum: cython.float
    __valueSum: cython.float
    __min: cython.float
    __max: cython.float
    __recordedTimestamps: Optional[list[cython.float]]
    __recordedValues: Optional[list[cython.float]]

    def __init__(self, record_values: bool = False) -> None:
        """Records continuous trends (e.g. the number of clients in the system over time).

        Args:
            record_values (bool, optional): Record each state change? Defaults to False.
        """
        self.__lastTime: cython.float = -1
        self.__lastValue: cython.float = -1
        self.__timeSum: cython.float = 0
        self.__valueSum: cython.float = 0
        self.__min: cython.float = 0
        self.__max: cython.float = 0
        self.__recordedTimestamps: Optional[list[cython.float]] = None
        self.__recordedValues: Optional[list[cython.float]] = None
        if record_values:
            self.__recordedTimestamps = []
            self.__recordedValues = []

    @cython.ccall
    def record(self, time: cython.float, value: cython.float):
        """Captures a change of state.

        Args:
            time (float): Time at which the change of state occurred
            value (float): New state
        """
        if self.__lastTime >= 0:
            delta: cython.float = time - self.__lastTime
            last: cython.float = self.__lastValue
            if delta > 0:
                self.__timeSum += delta
                self.__valueSum += delta * last
            if last < self.__min: self.__min = last
            if last > self.__max: self.__max = last
        else:
            self.__min = value
            self.__max = value

        self.__lastTime = time
        self.__lastValue = value

        if self.__recordedTimestamps is not None and self.__recordedValues is not None:
            self.__recordedTimestamps.append(time)
            self.__recordedValues.append(value)

    @property
    def time(self) -> float:
        """Time of the last recorded change of state.

        Returns:
            float: Time of the last recorded change of state
        """
        return max(0, self.__timeSum)

    @property
    def mean(self) -> float:
        """Mean value over the recorded states.

        Returns:
            float: Mean value over the recorded states (or 0 if no state has been recorded yet)
        """
        return self.__valueSum / self.__timeSum if self.__timeSum > 0 else 0

    @property
    def min(self) -> float:
        """Minimum recorded state

        Returns:
            float: Minimum recorded state
        """
        return self.__min

    @property
    def max(self) -> float:
        """Maximum recorded state

        Returns:
            float: Maximum recorded state
        """
        return self.__max

    @property
    def values(self) -> tuple:
        """List of the recorded values (if recording was activated)

        Returns:
            tuple[list[float], list[float]]: List of the recorded values (if recording was activated)
        """
        if self.__recordedTimestamps is not None and self.__recordedValues is not None:
            return self.__recordedTimestamps, self.__recordedValues
        else:
            return [], []

    def __str__(self) -> str:
        return "timespan = {:.1f}, mean = {:.1f}, min = {:.1f}, max = {:.1f}".format(self.time, self.mean, self.min, self.max)

    @property
    def info(self) -> str:
        """Short information about the main indicators

        Returns:
            str: Short information about the main indicators
        """
        return "mean = {:.1f}".format(self.mean)


@cython.cclass
class RecordOptions:
    """Captures proportions (e.g. the number of successful clients)."""
    __slots__ = ("__options")

    __options: collections.Counter

    def __init__(self) -> None:
        """Captures proportions (e.g. the number of successful clients)."""
        self.__options: collections.Counter = collections.Counter()

    @cython.ccall
    def record(self, option: Any):
        """Increases the counter for one of the possible options by 1.

        Args:
            option (Any): Chosen option
        """
        if option in self.__options:
            self.__options[option] += 1
        else:
            self.__options[option] = 1

    @property
    def count(self) -> int:
        """Total number of option selections recorded.

        Returns:
            int: Total number of option selections recorded
        """
        return sum(self.__options.values())

    @property
    def data(self) -> collections.Counter:
        """Mapping of options to frequencies for the respective options.

        Returns:
            dict: Mapping of options to frequencies for the respective options
        """
        return self.__options

    def __str__(self) -> str:
        sum: cython.int = self.count
        result: str = "count = {}".format(self.count)
        for option in self.__options:
            result += ", {} = {:.1%}".format(option, self.__options[option] / sum)
        return result
