"""Function for building a graph from the queueing network"""

import networkx as nx
from .stations import Source


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


def _build_station_name(station, station_names: dict, last_nr_for_type: dict):
    if station in station_names: return
    cls = type(station)
    base_name: str = str(cls.__name__)

    addon: str = ""
    if isinstance(station, Source): addon = " \"" + station.client_type_name + "\""

    if cls in last_nr_for_type:
        nr = last_nr_for_type[cls] + 1
    else:
        nr = 1
    last_nr_for_type[cls] = nr
    station_names[station] = base_name + " " + str(nr) + addon


def _add_station_to_graph(station, station_names: dict, todo: list, edges: list, graph):
    name = station_names[station]
    graph.add_node(name)
    for next_station in station.next_stations:
        edges.append((station, next_station))
        if not next_station in station_names and not next_station in todo: todo.append(next_station)


def build_graph(initial_nodes: list):
    """Builds a networkx based model of a queueing network

    Args:
        initial_nodes (list): List of the starting nodes (usually source stations) of the queueing network

    Returns:
        networkx.DiGraph: network graph
    """
    todo = list(initial_nodes)
    station_names = {}
    last_nr_for_type = {}
    edges = []
    dg = nx.DiGraph()

    while todo:
        station = todo.pop()
        _build_station_name(station, station_names, last_nr_for_type)
        _add_station_to_graph(station, station_names, todo, edges, dg)

    for edge in edges:
        dg.add_edge(station_names[edge[0]], station_names[edge[1]])

    return dg
