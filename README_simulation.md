# Simulating simple models using QueueSim

A simple M/M/c simulation model consists of three stations: a source, a process station and a dispose station. Additionally a simulator object for managing the events is needed.


## Simulator

The `Simulator` object is the core of each simulation model and should be created first:

```python
import queuesim

simulator = queuesim.Simulator()
```


## Stations

Then the stations can be created:

```python
from queuesim.stations import Source, Process, Dispose

source = Source(simulator, count, get_i)
process = Process(simulator, get_s, c)
dispose = Dispose(simulator)
```

The constructor of each station needs the simulator object as first parameter. After this station dependent parameters can be enters. There are also many optional parameters (see DocString help for the station constructors).

* The source station needs the number of arrivals to be generated (`count`) and an inter-arrival times distribution (`get_i`).
* The process station needs a service times distribution (`get_s`) and the number of available operators (`c`).
* The dispose station has no configuration.


## Random number distributions

`get_i` and `get_s` are lambda expressions (or strings that can be evaluated to lambda expressions) returning the next value of the corresponding distribution (the time span between the current and the next arrival or the needed time to serve the current client). This means any expression or random number distribution can be used here. For example

```python
def get_s():
    return 5
```

will result in a fixed service time of 5 time units for each client. For the most common distribution types there are already convenience functions which can be used directly (see [Random number distributions](README_distributions.md)). For example

```python
from queuesim.random_dist import exp as exp_dist

process = Process(simulator, exp_dist(100), c)
```

will create a process station with exponentially distributed service times and and average service time of 100 time units.


## Connecting the stations

The simulator object will send the clients from one station to the next. Using the `set_next` method of the source and the process station will define to which stations the clients will be sent after leaving the current station. (The dispose station has no `set_next` method since the clients leave the system at this station. There is no next station after the dispose station.)

```python
source.set_next(process)
process.set_next(dispose)
```


## Running the simulation

After creating a simulator and the stations and connecting the stations the simulation can be started:

```python
simulator.run()
```


## Processing the results

The process and the dispose stations are recording statistic data automatically. The process stations record the number of clients at the station and in the queue and waiting and service times. The dispose stations record the client data (for example the whole collected waiting times while moving through the system of a client) of the clients which leave the system at the corresponding dispose stations.

There is a class for recording discrete recordable values (like waiting times) `RecordDiscrete` and a class for continuous available values (like the number of clients at a station) `RecordContinuous`.

* The `RecordDiscrete` class offers these properties: `count`, `mean`, `sd`, `cv`, `min`, `max`, `histogram` and `histogram_stepwide`.
* The `RecordContinuous` object offers these properties: `time`, `mean`, `min` and `max`.

At process and dispose stations the following statistic information are available:

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

The data can be accessed very easily:

```python
print("E[N_Q]=", process.statistic_queue_length.mean)
print("E[W]=", dispose.statistic_client_waiting.mean)
```

There is also a convenience function for displaying all statistic data for M/M/c models:

```python
from queuesim.models import mmc_results

model={'Source': source, 'Process': process, 'Dispose': dispose}
print(mmc_results(model))
```


## Putting all together

```python
import queuesim
from queuesim.stations import Source, Process, Dispose
from queuesim.random_dist import exp as exp_dist
from queuesim.models import mmc_results

count = 100_000
get_i = exp_dist(100)
get_s = exp_dist(80)
c = 1

simulator = queuesim.Simulator()

source = Source(simulator, count, get_i)
process = Process(simulator, get_s, c)
dispose = Dispose(simulator)

source.set_next(process)
process.set_next(dispose)

simulator.run()

model={'Source': source, 'Process': process, 'Dispose': dispose}
print(mmc_results(model))
```

There is also a helper function for generating M/M/c models:

```python
from queuesim.models import mmc_model, get_simulator_from_model, mmc_results

count = 100_000
mean_i = 100
mean_s = 80
c = 1

model = mmc_model(mean_i, mean_s, c, count)
simulator = get_simulator_from_model(model)

simulator.run()

print(mmc_results(model))
```