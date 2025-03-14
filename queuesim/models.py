"""Auxiliary functions for creation of M/M/c and call center models"""

from typing import Any, Optional
from .random_dist import exp as dist_exp
from .descore import Simulator
from .stations import Source, Process, Decide, Delay, Dispose


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


def get_simulator_from_model(model) -> Simulator:
    """Returns the simulator object from a station of a model.

    Args:
        model (dict): Mapping of all stations

    Returns:
        Simulator: Simulator object
    """
    anyStation = model[list(model.keys())[0]]
    return anyStation.simulator


def mmc_model(mean_i: float, mean_s: float, c: int, count: int, record_values: bool = False) -> dict:
    """Generates a simple M/M/c model.

    Args:
        mean_i (float): Average inter-arrival time (E[I])
        mean_s (float): Average service time (E[S])
        c (int): Number of operators (c)
        count (int): Client arrivals to be simulated
        record_values (bool, optional): Record each state change? Defaults to False.

    Returns:
        object: Entire model consisting of stations and input parameters
    """
    # Define parameters
    get_i = dist_exp(mean_i)
    get_s = dist_exp(mean_s)

    # Create and configure stations
    simulator = Simulator()
    source = Source(simulator, count, get_i)
    process = Process(simulator, get_s, c, record_values=record_values)
    dispose = Dispose(simulator)

    # Link stations
    source.set_next(process)
    process.set_next(dispose)

    # Return model
    return {'Source': source, 'Process': process, 'Dispose': dispose, 'meanI': mean_i, 'meanS': mean_s, 'c': c}


def mmc_model_priorities(mean_i: float, mean_s: float, c: int, count: int, priority: Any) -> dict:
    """Generates a simple M/M/c model with a priority lambda for the service discipline.

    Args:
        mean_i (float): Average inter-arrival time (E[I])
        mean_s (float): Average service time (E[S])
        c (int): Number of operators (c)
        count (int): Client arrivals to be simulated
        priority (Any): Lambda for getting the client priority

    Returns:
        object: Entire model consisting of stations and input parameters
    """
    # Define parameters
    get_i = dist_exp(mean_i)
    get_s = dist_exp(mean_s)

    # Create and configure stations
    simulator = Simulator()
    source = Source(simulator, count, get_i)
    process = Process(simulator, get_s, c, getPriority=priority)
    dispose = Dispose(simulator)

    # Link stations
    source.set_next(process)
    process.set_next(dispose)

    # Return model
    return {'Source': source, 'Process': process, 'Dispose': dispose, 'meanI': mean_i, 'meanS': mean_s, 'c': c}


def impatience_and_retry_model_build(mean_i: float, mean_s: float, mean_wt: float, retry_probability: float, mean_retry_delay: float, c: int, count: int) -> dict:
    """Generates a M/M/c + M model with impatience.

    Args:
        mean_i (float): Average inter-arrival time (E[I])
        mean_s (float): Average service time (E[S])
        mean_wt (float): Average waiting time tolerance (E[WT])
        retry_probability: Retry probability
        mean_retry_delay (float): Average delay before a retry
        c (int): Number of operators (c)
        count (int): Client arrivals to be simulated
        record_values (bool, optional): Record each state change? Defaults to False.

    Returns:
        object: Entire model consisting of stations and input parameters
    """
    # Define parameters
    get_i = dist_exp(mean_i)
    get_s = dist_exp(mean_s)
    get_nu = dist_exp(mean_wt)
    get_delay = dist_exp(mean_retry_delay)
    c = 1

    # Create and configure stations
    simulator = Simulator()
    source = Source(simulator, count, get_i)
    process = Process(simulator, get_s, c, get_nu)
    dispose = Dispose(simulator)

    # Link stations
    source.set_next(process)
    process.set_next(dispose)
    if retry_probability > 0:
        retry_decide = Decide(simulator)
        retry_delay = Delay(simulator, get_delay)
        process.set_next_cancel(retry_decide)
        retry_decide.add_next(retry_delay, retry_probability)
        retry_decide.add_next(dispose, 1 - retry_probability)
        retry_delay.set_next(process)
        # Return model
        return {'Source': source, 'Process': process, 'Dispose': dispose, 'RetryDecide': retry_decide, 'RetryDelay': retry_delay, 'meanI': mean_i, 'meanS': mean_s, 'meanWT': mean_wt, 'c': c}
    else:
        process.set_next_cancel(dispose)
        # Return model
        return {'Source': source, 'Process': process, 'Dispose': dispose, 'meanI': mean_i, 'meanS': mean_s, 'meanWT': mean_wt, 'c': c}


def build_network_model(sources: list, processes: list, disposes: list, connections1: list, connections2: list) -> None:
    """Connections sources, process stations and dispose station by transition rates defined in two matrices

    Args:
        sources (list[Source]): List of sources
        processes (list[Process]): List of process stations
        disposes (list[Dispose]): List of dispose stations
        connections1 (list[list[float]]): Matrix of size len(sources) x len(processes) defining the transition rates from the sources to the process stations
        connections2 (list[list[float]]): Matrix of size len(processes) x (len(processes)+len(disposes)) defining the transition rates from the process stations to the process stations or the dispose stations

    Raises:
        RuntimeError: Raises an error if the matrix dimensions does to match to the list lengths
    """
    if len(connections1) != len(sources): raise RuntimeError("connections1 row count does not match number of sources")
    if len(connections2) != len(processes): raise RuntimeError("connections2 row count does not match number of processes")

    # Get simulator
    simulator: Simulator = sources[0].simulator

    # Connect sources to process stations
    for s_index, source in enumerate(sources):
        decide: Decide = Decide(simulator)
        source.set_next(decide)
        row = connections1[s_index]
        if len(row) > len(processes): raise RuntimeError("connections1 column count does mot match number of processes")
        for p_index, rate in enumerate(row):
            if rate <= 0: continue
            decide.add_next(processes[p_index], rate)

    # Connect process stations to each other and to the dispose stations
    for p_index, process in enumerate(processes):
        row = connections2[p_index]
        if len(row) > len(processes) + len(disposes): raise RuntimeError("connections2 column count does mot match sum of number of processes and number of dispose stations")

        if sum([1 for i in row if i > 0]) == 1:
            # Only one connection
            for next_index, rate in enumerate(row):
                if rate > 0:
                    process.set_next(processes[next_index])
        else:
            # Multiple connections, use decide station
            decide: Decide = Decide(simulator)
            process.set_next(decide)
            for next_index, rate in enumerate(row):
                if rate <= 0: continue
                if next_index < len(processes):
                    decide.add_next(processes[next_index], rate)
                else:
                    decide.add_next(disposes[next_index - len(processes)], rate)


def mmc_results(model: dict) -> str:
    """Returns the most relevant statistic information about a M/M/c model

    Args:
        model (dict): M/M/c model with completed simulation

    Returns:
        str: Statistic information about a M/M/c model
    """
    source = model["Source"]
    process = model["Process"]
    dispose = model["Dispose"]

    results = []

    results.append("System")
    results.append("  Simulated arrivals: " + str(source.count))
    results.append("  Inter-arrival times at the system (I): " + source.statistic.info)
    results.append("  Inter-departure times from the system (ID): " + dispose.statistic.info)
    results.append("")

    results.append("Process station")
    results.append("  Waiting times (W): " + process.statistic_station_waiting.info)
    results.append("  Service times (S): " + process.statistic_station_service.info)
    results.append("  Queue length (NQ): " + process.statistic_queue_length.info)
    results.append("  Clients at the station (N): " + process.statistic_wip.info)
    results.append("  Work load (rho*c): " + process.statistic_workload.info)
    results.append("")

    results.append("Clients")
    results.append("  Waiting times (W): " + dispose.statistic_client_waiting.info)
    results.append("  Service times (S): " + dispose.statistic_client_service.info)
    results.append("  Residence times (V): " + dispose.statistic_client_residence.info)

    return "\n".join(results)


def call_center_results(source: Source, process: Process, forwarding: Optional[Decide], retry: Optional[Decide], delay: Optional[Delay], dispose: Dispose, simulator: Simulator, lang: Optional[str] = None) -> str:
    """Output of the results of the simulation of a call center model

    Args:
        source (Source): Client source
        process (Process): Process station
        forwarding (Decide): Decision: Forwarding yes/no (can be None)
        retry (Decide): Decision: Retry yes/no (can be None)
        delay (Delay): Delay before retry (can be None)
        dispose (Dispose): Dispose station
        simulator (Simulator): Simulator object
        lang (str, optional): Output language ("de" for German, English in all other cases). Defaults to None.
    """

    results = []

    if not isinstance(lang, str) or lang.lower() != "de":
        results.append("System")
        results.append("  Simulated arrivals: " + str(source.count))
        results.append("  Inter-arrival times at the system (I): " + str(source.statistic))
        results.append("  Inter-departure times from the system (ID): " + str(dispose.statistic))
        results.append("")

        results.append("Process station")
        results.append("  Success rate: " + str(process.statistic_success))
        results.append("  Waiting times (W): " + str(process.statistic_station_waiting))
        results.append("  Service times (S): " + str(process.statistic_station_service))
        if process.statistic_station_post_processing.count > 0: results.append("  Nachbearbeitungszeiten (S2): " + str(process.statistic_station_post_processing))
        results.append("  Queue length (NQ): " + str(process.statistic_queue_length))
        results.append("  Clients at the station (N): " + str(process.statistic_wip))
        results.append("  Work load (c*rho): " + str(process.statistic_workload))
        results.append("")

        results.append("Clients")
        results.append("  Waiting times (W): " + str(dispose.statistic_client_waiting))
        results.append("  Service times (S): " + str(dispose.statistic_client_service))
        results.append("  Residence times (V): " + str(dispose.statistic_client_residence))
        results.append("")

        if forwarding is not None and len(forwarding.statistic_options.data) > 1:
            results.append("Forwarding")
            results.append("  " + str(forwarding.statistic_options))
            results.append("  Exit 1 = Dispose")
            results.append("  Exit 2 = Forwarding back to process station")
            results.append("")

        if retry is not None and retry.statistic_options.count > 0:
            results.append("Retry")
            results.append("  " + str(retry.statistic_options))
            results.append("  Exit 1 = Final cancelation")
            results.append("  Exit 2 = Retry")
            results.append("")

        if delay is not None and delay.statistic.count > 0:
            results.append("Delay before retry")
            results.append("  Clients at the station (N): " + str(delay.statistic_wip))
            results.append("  Residence times (V): " + str(delay.statistic_station_residence))
            results.append("")

        results.append("Simulator")
        results.append("  Total computing time: " + str(round(simulator.run_time, 1)) + " seconds")
        results.append("  Computing time per client: " + str(round(simulator.run_time / source.count * 1000 * 1000, 1)) + " µs")
        results.append("  Computing time per event: " + str(round(simulator.run_time / simulator.event_count * 1000 * 1000, 1)) + " µs")
        results.append("  Simulated events: " + str(simulator.event_count))
        results.append("")
    else:
        results.append("System")
        results.append("  Simulierte Ankünfte: " + str(source.count))
        results.append("  Zwischenankunftszeiten am System (I): " + str(source.statistic))
        results.append("  Zwischenabgangszeiten aus dem System (ID): " + str(dispose.statistic))
        results.append("")

        results.append("Bedienstation")
        results.append("  Erfolgsquote: " + str(process.statistic_success))
        results.append("  Wartezeit (W): " + str(process.statistic_station_waiting))
        results.append("  Bedienzeit (S): " + str(process.statistic_station_service))
        if process.statistic_station_post_processing.count > 0: results.append("  Nachbearbeitungszeiten (S2): " + str(process.statistic_station_post_processing))
        results.append("  Warteschlangenlänge (NQ): " + str(process.statistic_queue_length))
        results.append("  Kunden an Station (N): " + str(process.statistic_wip))
        results.append("  Auslastung (c*rho): " + str(process.statistic_workload))
        results.append("")

        results.append("Kunden")
        results.append("  Wartezeit (W): " + str(dispose.statistic_client_waiting))
        results.append("  Bedienzeit (S): " + str(dispose.statistic_client_service))
        results.append("  Verweilzeit (V): " + str(dispose.statistic_client_residence))
        results.append("")

        if forwarding is not None and len(forwarding.statistic_options.data) > 1:
            results.append("Weiterleitungen")
            results.append("  " + str(forwarding.statistic_options))
            results.append("  Ausgang 1 = Ende")
            results.append("  Ausgang 2 = Weiterleitung zurück zur Bedienstation")
            results.append("")

        if retry is not None and retry.statistic_options.count > 0:
            results.append("Wiederholungen")
            results.append("  " + str(retry.statistic_options))
            results.append("  Ausgang 1 = Finaler Abbruch")
            results.append("  Ausgang 2 = Neuer Versuch")
            results.append("")

        if delay is not None and delay.statistic.count > 0:
            results.append("Verzögerung vor Wiederholungen")
            results.append("  Kunden an Station (N): " + str(delay.statistic_wip))
            results.append("  Verweilzeit (V): " + str(delay.statistic_station_residence))
            results.append("")

        results.append("Simulator")
        results.append("  Rechenzeit gesamt: " + str(round(simulator.run_time, 1)) + " Sekunden")
        results.append("  Rechenzeit pro Kunde: " + str(round(simulator.run_time / source.count * 1000 * 1000, 1)) + " µs")
        results.append("  Rechenzeit pro Ereignis: " + str(round(simulator.run_time / simulator.event_count * 1000 * 1000, 1)) + " µs")
        results.append("  Simulierte Ereignisse: " + str(simulator.event_count))
        results.append("")

    return "\n".join(results)
