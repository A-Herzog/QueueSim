# QueueSim

QueueSim is a Python package for discrete event stochastic simulation of queueing networks. For Kendall models the performance indicators can also be computed using Erlang and Allen Cunneen approximation formulas.


## Installation

A PyPI package is not yet available. Just download and extract the zip package offered here.

The zip package also includes some example files (as plain Python files and as Jupyter notebooks) describing the base functions.

* If you are using a Python environment which can show Jupyter notebooks, open and run any from the `example_*.ipynb` files in this directory.
* If you are using plain Python, open and run any from the `example_*.py` files in this directory.


## Requirements

* **Python 3.7 or higher** is needed to execute QueueSim.
* **`numpy`** is used by `queuesim.statistics` and in several example files.
* **`pandas`** and **`scipy`** are used in `queuesim.analytic`.
* The visualizations in the example Jupyter notebooks use **`matplotlib`** and **`seaborn`**.
* The graphical network builder (see `queuesim.graph.build_graph`) uses **`networkx`**.

As long a you are not using the function for calculating analytical results, not using the Jupyter notebooks and not using the graph builder you will not need `pandas`, `mathplotlib`, `seaborn` and `networkx`.


## Main features of QueueSim

* Building queueing networks on source code base (not only Kendall models)
* Option to use any lambda expressions for inter-arrival and service times (lambda expression generators for the most common distributions are included)
* Batch arrival and service is possible
* Option to model impatience of the clients
* Branching clients by conditions or by chance
* Different service disciplines are available (FIFO, LIFO or user-defined priority formulas)
* Automatic statistic recording
* Erlang and Allen Cunneen classes for comparison of simulation and analytical results
* Helper classes for parallel multi-process simulation
* Can be compiled using Cython (`pyx` classes with type annotations for speed-up are included)



# Usage examples

* [Simulating simple models](README_simulation.md)
* [Random number distributions](README_distributions.md)
* [Impatience](README_impatience.md)
* [Networks](README_networks.md)
* [Batch arrival and batch service](README_batch.md)
* [Multiple client types with different service times or different priorities](README_clienttypes.md)
* [FIFO/LIFO/Random](README_discipline.md)
* [Post-processing times](README_postprocessing.md)
* [Queueing systems with control](README_control.md)
* [Statistics results](README_statistics.md)
* [Parallelization](README_parallelization.md)
* [Calculating analytical results](README_analytical.md)



# Example files

There is a number of `py` files and Jupyter notebooks that illustrate various functions of QueueSim:


## Analytical calculations

* **Erlang B formula for M/M/c/c models**
  * Plain Python: [`example_analytic_erlang_b.py`](example_analytic_erlang_b.py)
  * Jupyter notebook: [`example_analytic_erlang_b.ipynb`](example_analytic_erlang_b.ipynb)
* **Erlang C formula for M/M/c models**
  * Plain Python: [`example_analytic_erlang_c.py`](example_analytic_erlang_c.py)
  * Jupyter notebook: [`example_analytic_erlang_c.ipynb`](example_analytic_erlang_c.ipynb)
* **Extended Erlang C formula (with impatient clients) for M/M/c/K+M models**
  * Plain Python: [`example_analytic_erlang_c_ext.py`](example_analytic_erlang_c_ext.py)
  * Jupyter notebook: [`example_analytic_erlang_c_ext.ipynb`](example_analytic_erlang_c_ext.ipynb)
* **Allen Cunneen approximation formula for GI/G/c models**
  * Plain Python: [`example_analytic_ac_approx.py`](example_analytic_ac_approx.py)
  * Jupyter notebook: [`example_analytic_ac_approx.ipynb`](example_analytic_ac_approx.ipynb)


## Simulation

### Very simple simulation models not using QueueSim

* **Minimal simulator for a M/M/1 model not using QueueSim, just a few lines of code**
  * Plain Python: [`example_sim_minimal_MM1.py`](example_sim_minimal_MM1.py)
  * Jupyter notebook: [`example_sim_minimal_MM1.ipynb`](example_sim_minimal_MM1.ipynb)
* **Minimal simulator for G/G/c models not using QueueSim, just a few lines of code**
  * Plain Python: [`example_sim_minimal_GGc.py`](example_sim_minimal_GGc.py)
  * Jupyter notebook: [`example_sim_minimal_GGc.ipynb`](example_sim_minimal_GGc.ipynb)

### Simulation models

* **Simulation results of a M/M/c model compared to the analytical Erlang C results**
  * Plain Python: [`example_sim_mmc_simple.py`](example_sim_mmc_simple.py)
  * Jupyter notebook: [`example_sim_mmc_simple.ipynb`](example_sim_mmc_simple.ipynb)
* **Recording the course of number of clients in the system in a M/M/c model**
  * Plain Python: [`example_sim_mmc_course.py`](example_sim_mmc_course.py)
  * Jupyter notebook: [`example_sim_mmc_course.ipynb`](example_sim_mmc_course.ipynb)
* **Parameter study of a M/M/c model**
  * Plain Python: [`example_sim_mmc_series.py`](example_sim_mmc_series.py)
  * Jupyter notebook: [`example_sim_mmc_series.ipynb`](example_sim_mmc_series.ipynb)

### Complex simulation models

* **Simulation of a call center model (a M/M/c/K+M model with forwarding and retry)**
  * Plain Python: [`example_sim_call_center.py`](example_sim_call_center.py)
  * Jupyter notebook: [`example_sim_call_center.ipynb`](example_sim_call_center.ipynb)
* **Parameter study of a call center model**
  * Plain Python: [`example_sim_call_center_series.py`](example_sim_call_center_series.üy)
  * Jupyter notebook: [`example_sim_call_center_series.ipynb`](example_sim_call_center_series.ipynb)
* **Simulation of a queueing network with transition probabilities defined via matrices**
  * Plain Python: [`example_sim_network.py`](example_sim_network.py)
  * Jupyter notebook: [`example_sim_network.ipynb`](example_sim_network.ipynb)
* **Distribution random number generator tests**
  * Plain Python: [`example_sim_random_numbers.py`](example_sim_random_numbers.py)
  * Jupyter notebook: [`example_sim_random_numbers.ipynb`](example_sim_random_numbers.ipynb)
* **System design - comparison of different queueing disciplines**
  * Plain Python: [`exmaple_sim_shortest_queue.py`](exmaple_sim_shortest_queue.py)
  * Jupyter notebook: [`exmaple_sim_shortest_queue.ipynb`](exmaple_sim_shortest_queue.ipynb)

### Queueing disciplines

* **FIFO, LIFO or random selection of the next client**
  * Plain Python: [`example_sim_mmc_priorities1.py`](example_sim_mmc_priorities1.py)
  * Jupyter notebook: [`example_sim_mmc_priorities1.ipynb`](example_sim_mmc_priorities1.ipynb)
* **Two client types with different priorities**
  * Plain Python: [`example_sim_mmc_priorities2.py`](example_sim_mmc_priorities2.py)
  * Jupyter notebook: [`example_sim_mmc_priorities2.ipynb`](example_sim_mmc_priorities2.ipynb)

## Optimization

* **Simple iterative optimization example**
  * Plain Python: [`example_optimize_simple1.py`](example_optimize_simple1.py)
  * Jupyter notebook: [`example_optimize_simple1.ipynb`](example_optimize_simple1.ipynb)
* **Simple optimization example using [BOBYQA](https://pypi.org/project/Py-BOBYQA/)**
  * Plain Python: [`example_optimize_simple2.py`](example_optimize_simple2.py)
  * Jupyter notebook: [`example_optimize_simple2.ipynb`](example_optimize_simple2.ipynb)
* **More complex iterative optimization example**
  * Plain Python: [`example_optimize_complex1.py`](example_optimize_complex1.py)
  * Jupyter notebook: [`example_optimize_complex1.ipynb`](example_optimize_complex1.ipynb)
* **More complex optimization example using [BOBYQA](https://pypi.org/project/Py-BOBYQA/)**
  * Plain Python: [`example_optimize_complex2.py`](example_optimize_complex2.py)
  * Jupyter notebook: [`example_optimize_complex2.ipynb`](example_optimize_complex2.ipynb)



# Overview of the main classes

## The Simulator

```python
class queuesim.Simulator
```
The Simulator class contains the code for event management and for running simulations. There is only one relevant method in this class: `run()`

```python
import queuesim

simulator = queuesim.Simulator()
# Define stations here, link stations to each other and to the simulator
simulator.run()
# Process statistic results here
```

## Stations

QueueSim offers 7 station types from which many types of queueing networks can be built: `Source`, `Process`, `Delay`, `Decide`, `DecideCondition`, `DecideClientType` and `Dispose`. While most stations have input and output connections, the `Source` station has only an output and the `Dispose` station only an input. All station types are defined in module `queuesim.stations`.

### Source

Each model starts with one or more `Source` stations. At these stations clients enter the system.

```python
import queuesim
import queuesim.stations

simulator = queuesim.Simulator()

count = 100_000  # Number of arrivals to be simulated
get_i = ... # string (to be evaluated) or lambda expression to generate inter-arrival times
source = queuesim.stations.Source(simulator, count, get_i)

next_station_in_queueing_network = ...

source.set_next(next_station_in_queueing_network)
```

(For helper functions to generate pseudo random number generators for the inter-arrival times see description of module `queuesim.random_dist` below.) Additionally there is an optional parameter `getIB=` in the constructor of the `Source` object by which variable arrival batch sizes can be defined.

### Process

The ``Process`` station is the main component of every queueing model. Here is the queue and the service desk.

```python
import queuesim
import queuesim.stations

simulator = queuesim.Simulator()

get_s = ... # string (to be evaluated) or lambda expression to generate the service times
c = 1  # Number of parallel operators
process = queuesim.stations.Process(simulator, get_s, c)

next_station_in_queueing_network = ...

process.set_next(next_station_in_queueing_network)
```

Further optional parameters for the constructor are:
* `getNu=` (waiting cancelation distribution)
* `getS2=` (post-processing times distribution)
* `K=` (maximum system size)
* `b=` (service batch size)
* `LIFO=` (use LIFO instead of FIFO)
* `getPriority=` (priorities of the waiting clients)
* `record_values=` (record course of the queue length and the number of clients at the station instead of only the usual statistic indicators)
* `getS_client_type=` (waiting cancelation distributions for individual client types)
* `getNu_client_type=` (service times distributions for individual client types)

If clients can leave the station without being served (due to system size limitations or due to impatience) via `process.set_next_cancel(...)` a path for these unsuccessful clients has to be defined.

### Dispose

At a `Dispose` station the clients will leave the system. Their statistic data will be recorded at this station.

```python
import queuesim
import queuesim.stations

simulator = queuesim.Simulator()

get_s = ... # string (to be evaluated) or lambda expression to generate the service times
c = 1  # Number of parallel operators
dispose = queuesim.stations.Dispose(simulator)
```

There is no configuration needed for the dispose station.


## A complete M/M/c model

Using these three station types, we can build a M/M/c model (or even a G/G/c or a G<sup>b<sub>I</sub></sup>/G<sup>b<sub>S</sub></sup>/c model) very easily:

```python
import queuesim
from queuesim.stations import Source, Process, Dispose
from queuesim.random_dist import exp as exp_dist

count = 100_000  # Number of arrivals to be simulated
get_i = exp_dist(100)  # exponential distribution with mean E[I]=100
get_s = exp_dist(80)  # exponential distribution with mean E[S]=80
c = 1  # One operator in this model

# The simulator
simulator = queuesim.Simulator()

# Configuring the stations
source = Source(simulator, count, get_i)
process = Process(simulator, get_s, c)
dispose = Dispose(simulator)

# Connecting the stations
source.set_next(process)
process.set_next(dispose)

# Running the simulation
simulator.run()
```

Since M/M/c models are very common, there is a convenience method for generating such models:

```python
import queuesim.models

model = queuesim.models.mmc_model(100, 80, 1, 100_000)  # Parameters: E[I], E[S], c and number of arrivals
simulator = queuesim.models.get_simulator_from_model(model)
simulator.run()
```

The `model` object is a `dict` containing source, process and dispose: `model['Source']`, `model['Process']` and `model['Dispose']`.

There are also two more functions for creating more complex models:

* `mmc_model_priorities(mean_i, mean_s, c, count, priority)`: Creates a M/M/c model using a priority formula at the process station for the queueing discipline.
* `impatience_and_retry_model_build(mean_i, mean_s, mean_wt, retry_probability, mean_retry_delay, c, count)`: Create an extended M/M/c model containing impatience and retrying clients.

## Pseudo random number generators

In `queuesim.random_dist` there are lambda factory methods for these distributions:

* Exponential distribution: `exp(mean)`
* Log-normal distribution: `log_normal(mean, sd)`
* Gamma distribution: `gamma(mean, sd)`
* Uniform distribution: `uniform(low, high)`
* Triangular distribution: `uniform(low, most_likely, high)`
* Deterministic: `deterministic(fixed_value)`
* Empirical: `empirical(options)` where `options` is a `dict` of values to rates

Since the gamma distribution is a generalization of the Erlang distribution, the quite common Erlang distribution is also covered.

Note that the parameters for `log_normal` and `gamma` are `mean` and `sd`. So no manual converting from mean and standard deviation to $\mu$, $\sigma$, ... is needed.

The generator functions will return strings containing lambda expressions. The strings are evaluated inside the stations. This is needed for serialization for multi-process simulation. If you do not want to use multi-process parallelization, you can also add the parameter `as_lambda=True` to get lambda expressions directly. The stations will understand both: strings and lambdas.


## Statistics

Each station records the statistic indicators relevant for the station (and the `Dispose` station takes care for the data of the clients leaving the system). After the completion of the simulation the statistic data are available via properties:

* `process.statistic_station_waiting` (type: `RecordDiscrete`)
* `process.statistic_station_service` (type: `RecordDiscrete`)
* `process.statistic_station_post_processing` (type: `RecordDiscrete`)
* `process.statistic_station_residence` (type: `RecordDiscrete`)
* `process.statistic_success` (type: `RecordOptions`)
* `process.statistic_queue_length` (type: `RecordContinuous`)
* `process.statistic_wip` (type: `RecordContinuous`)
* `process.statistic_workload` (type: `RecordContinuous`)
* `dispose.statistic_client_waiting` (type: `RecordDiscrete`)
* `dispose.statistic_client_service` (type: `RecordDiscrete`)
* `dispose.statistic_client_residence` (type: `RecordDiscrete`)

The `RecordDiscrete` class offers these properties: `count`, `mean`, `sd`, `cv`, `min`, `max`, `histogram` and `histogram_stepwide`. While most of them are of the type `float`, `histogram` is `list[float]` and `histogram_stepwide` is `int`.

The `RecordOptions` class offers these properties: `count` and `data`. `count` is of type `int` and `data` of type `collections.Counter`.

The `RecordContinuous` object offers these properties: `time`, `mean`, `min` and `max` (all of type `float`). If value recording is activated, they can be accessed via `values` (tuple of two lists: time stamps and values).

In the M/M/c example model above you can get the mean waiting time of the clients and the mean queue length at the station via:

```python
print("E[N_Q]=", process.statistic_queue_length.mean)
print("E[W]=", dispose.statistic_client_waiting.mean)
```


# What's next?

## Impatience, retry, forwarding

You can add a limited waiting time tolerance at a `Process` station very easily by adding a `getNu=` parameter and defining a path for the canceled clients (`process.set_next_cancel(...)`). Forward and Retry probabilities can be configured using `Decide` stations.

There is also a convenience function for generating models with impatience, retry and forwarding in the `queuesim.models` module called `impatience_and_retry_model_build` (see documentation there).


## Different client types

The constructor of `Source` has the optional parameter `client_type_name=` by which the name of the clients generated at this station can be defined. The clients can be branched on their way through the system via `DecideClientType` stations. Additionally at `Process` stations individual service times and waiting time tolerances can be defined per client type. (`Process(..., getS_client_type={"clientTypeX": random_dist.exp(100)})`).


## Queueing systems with control

By using a `DecideCondition` station clients can be branched to different paths based on systems parameters (like the current queue lengths at different stations). The following example consists of two process stations. A client is directed on arrival to the station with the currently shortest queue:

```python
source = Source(simulator, count, inter_arrival_time)
decide = DecideCondition(simulator)
process1 = Process(simulator, service_time1, c1)
process2 = Process(simulator, service_time2, c2)
dispose = Dispose(simulator)

def shortest_queue(client) -> int:
    nq1 = process1.nq
    nq2 = process2.nq
    if nq1 < nq2: return 0
    if nq1 > nq2: return 1
    return randint(0, 1)

source.set_next(decide)
decide.set_condition(shortest_queue)
decide.add_next(process1)
decide.add_next(process2)
process1.set_next(dispose)
process2.set_next(dispose)
```


## Larger networks

By using the `build_network_model` function from `queuesim.models` individual process stations can be linked by transition rate matrices. Only the stations have to be defined (service times, number of operators etc.). The connections between the stations (by using `Decide` stations) are established by the `build_network_model` function. The function needs a list of the sources, a list of the process stations and a list of the dispose stations. Additionally two matrices have to be defined: The first matrix give the rates by which the arriving clients are led from the sources to the process stations and the second matrix defined the rates at which the clients are led to other process stations or to the dispose stations after service process at an individual process station.

Assume we have m<sub>1</sub> sources, m<sub>2</sub> process stations and m<sub>3</sub> dispose stations, then the first transition rates matrix has the shape m<sub>1</sub> &times; m<sub>2</sub> and the second transition rates matrix has the shape m<sub>2</sub> &times; (m<sub>2</sub>+m<sub>3</sub>).

If you want to get a graphical representation of your queueing network, you can use `queuesim.build_graph(list_of_sources)` to get a digraph which can be plotted using `networkx`.


## Comparison to Erlang B, Erlang C and Allen Cunneen approximation formulas

In `queuesim.analytic` there are classes for calculating the performance indicators for M/M/c/c, M/M/c, M/M/c/K+M and GI/G/c models. The classes for the different formulas all work in the same way: The parameters of the models have to be specified in the constructor. Then the statistic values can be accessed via properties. Example:

```python
from queuesim.analytic import erlang_c

model=erlang_c(l, mu, c)  # Parameters: lambda=1/E[I], mu=1/E[S], c
print("Workload a=", model.a)
print("Utilization rho=", model.rho)
print("Average queue length E[N_Q]=", model.ENQ)
print("Average number of clients in the system E[N]=", model.EN)
print("Average waiting time E[W]=", model.EW)
print("Average residence time E[V]=", model.EV)
```

For each individual value class there is also a `..._table` function which takes a list of tuples of the parameters for the formula as parameter and returns a `pandas.DataFrame` of the results for the individual parameter combinations.

There are four plain Python and for Jupyter notebooks showing how to use the analytical formula classes:
* [`example_analytic_erlang_b.py`](example_analytic_erlang_b.py) / [`example_analytic_erlang_b.ipynb`](example_analytic_erlang_b.ipynb)
* [`example_analytic_erlang_c.py`](example_analytic_erlang_c.py) / [`example_analytic_erlang_c.ipynb`](example_analytic_erlang_c.ipynb)
* [`example_analytic_erlang_c_ext.py`](example_analytic_erlang_c_ext.py) / [`example_analytic_erlang_c_ext.ipynb`](example_analytic_erlang_c_ext.ipynb)
* [`example_analytic_ac_approx.py`](example_analytic_ac_approx.py) / [`example_analytic_ac_approx.ipynb`](example_analytic_ac_approx.ipynb)


## Parallelization

Instead of running a single simulation in the main process via

```python
model = ...
simulator = queuesim.models.get_simulator_from_model(model)
simulator.run()
```

the simulation can also be executed in a background process:

```python
import queuesim.SimProcess

model = ...
task = SimProcess(model)
task.start()
model_with_statistic_results = task.results  # Accessing the "results" property will wait for simulation finished
```

This allows to run multiple simulations at the same time. (Since individual processes are used, the global interpreter lock is no problem.)


## More examples / TL;DR

For all features and functions described above there are Jupyter notebooks included in the QueueSim zip package. So just open a notebook and execute it to try out the different functions.



# What QueueSim cannot do

* QueueSim is implemented in Python, so **its not very fast**. There are `pyx` files and a `setup.py` included so the performance critical classes can be compiled using Cython. This will speed-up simulation by a factor of 1.2 to 2. But this will still be quite slow compared to fully compiling languages. (See `cython-build.sh` script for compiling classes using Cython.)
* QueueSim has **no graphical user-interface**. Models have to be generated by writing Python code. (But queueing networks can be visualized. `queuesim.build_graph(list_of_sources)` will build a digraph which can be plotted using `networkx`.)
* Also carrying out parameter studies requires writing Python code.
* Since there is no graphical user-interface things like **animation of the models** etc. are also not possible.

If you want to have these feature, you can try **[Warteschlangensimulator](https://github.com/A-Herzog/Warteschlangensimulator)**, which is an open source desktop application and allows to define queueing models in form of flow charts. Warteschlangensimulator allows to create and run queueing models without programming.



# Contact

**Alexander Herzog**<br>
[TU Clausthal](https://www.tu-clausthal.de)<br>
[Simulation Science Center Clausthal / Göttingen](https://www.simzentrum.de/)<br>
alexander.herzog@tu-clausthal.de
