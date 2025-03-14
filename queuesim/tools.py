"""Auxiliary functions for the simulation of queueing models."""

from typing import Optional
import multiprocessing as mp
from time import perf_counter
from .descore import Simulator
from .stations import Station
from .models import get_simulator_from_model


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


def _run_sim_process(model: dict, queue: mp.Queue) -> None:
    simulator = get_simulator_from_model(model)
    simulator.run()

    for station in model.values():
        if isinstance(station, Station): station.clear_lambdas()
    queue.put(model)


class SimProcess:
    """This class encapsulates a complete simulation process."""

    def __init__(self, model: dict):
        """This class encapsulates a complete simulation process.

        Args:
            model (dict): Stations of the model
        """
        self.__queue: mp.Queue = mp.Queue()
        self.__process: mp.Process = mp.Process(target=_run_sim_process, args=(model, self.__queue, ))
        self.__simulator: Optional[Simulator] = None
        self.__results: Optional[dict] = None

    def start(self) -> None:
        """Starts the process.
        """
        self.__process.start()

    def join(self) -> None:
        """Waits for the simulation to complete."""
        self.__process.join()

        self.__results = self.__queue.get()
        self.__simulator = get_simulator_from_model(self.__results)

    @property
    def results(self) -> dict:
        """Returns the results of the simulation in the form of a Dict object.

        Returns:
            dict: Results of the simulation
        """
        if self.__results is None: self.join()
        return self.__results if self.__results is not None else {}

    @property
    def simulator(self) -> Simulator:
        """Simulator object

        Returns:
            Simulator: Simulator object
        """
        if self.__results is None: self.join()
        return self.__simulator if self.__simulator is not None else Simulator()


def run_parallel(processes: list) -> tuple:
    """Starts the processes, waits for their termination and collects the results.

    Args:
        processes (list[SimProcess]): List of simulation processes to be started

    Returns:
        tuple[list[dict], list[Simulator]]: Tuple of lists of models and of simulators
    """
    start = perf_counter()

    for process in processes: process.start()
    print(len(processes), "parallel processes started.")

    for process in processes: process.join()
    print("All processes terminated, runtime:", round(perf_counter() - start, 1), "seconds.")

    models = [process.results for process in processes]
    simulators = [process.simulator for process in processes]
    print("Results have been collected.")

    return (models, simulators)


def get_multi_run_info(sources: list, simulators: list, lang: Optional[str] = None) -> str:
    """Outputs information about the total runtime over several models.

    Args:
        sources (list[Source]): List of client sources of the models
        simulators (list[Simulator]): List of simulator objects of models
        lang (str, optional): Output language ("de" for German, English in all other cases). Defaults to None.

    Returns:
        str: Total runtime information
    """
    runTimeAll: float = max(simulator.run_time for simulator in simulators)
    runTimeSum: float = sum(simulator.run_time for simulator in simulators)
    arrivalCount: int = sum(source.count for source in sources)
    results: list = []

    if not isinstance(lang, str) or lang.lower() != "de":
        results.append("Models: " + str(len(simulators)))
        results.append("Client arrivals (total): " + str(round(arrivalCount / 1000 / 1000, 1)) + " millions")
        results.append("Computing time (total): " + str(round(runTimeAll, 1)) + " seconds")
        results.append("Computing time per client (real): " + str(round(runTimeSum / arrivalCount * 1000 * 1000, 1)) + " µs")
    else:
        results.append("Modelle: " + str(len(simulators)))
        results.append("Kundenankünfte (gesamt): " + str(round(arrivalCount / 1000 / 1000, 1)) + " Mio.")
        results.append("Rechenzeit (gesamt): " + str(round(runTimeAll, 1)) + " Sekunden")
        results.append("Rechenzeit pro Kunde (real): " + str(round(runTimeSum / arrivalCount * 1000 * 1000, 1)) + " µs")
    return "\n".join(results)
