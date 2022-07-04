"""This file will setup Cython Python file compilation.

If Cython is not used, this file is of no meaning.

See: https://cython.org/
"""

from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(["./queuesim/statistics.pyx","./queuesim/descore.pyx","./queuesim/stations.pyx",])
)