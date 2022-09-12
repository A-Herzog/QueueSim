# Impatience

In classical M/M/c models the clients are willing to wait for any needed time. In many real queueing systems (like call centers) the clients will have an individual limited waiting time tolerance. If the waiting time gets to long, the client will leave the station without being served.

To add a limited waiting time tolerance to a process station you need to do two things:

* Add a `getNu=` parameter to the process station constructor to define a waiting time tolerance.
* Define a next station for clients who have canceled waiting at the process station (`process.set_next_cancel(...)`).

```python
import queuesim
from queuesim.stations import Source, Process, Dispose
from queuesim.random_dist import exp as exp_dist
from queuesim.models import mmc_results

count = 100_000
get_i = exp_dist(100)
get_s = exp_dist(80)
get_Nu= exp_dist(600)  # Waiting time tolerance
c = 1

simulator = queuesim.Simulator()

source = Source(simulator, count, get_i)
process = Process(simulator, get_s, c, getNu=getNu)
dispose = Dispose(simulator)

source.set_next(process)
process.set_next(dispose)
process.set_next_cancel(dispose)  # Canceled clients leave the system just as successful clients

simulator.run()
```


## Retry

Impatience is often combined with retry. In this case the canceled clients are not directly directed to the dispose station but a decide station routes some of them back to the process station (repeater) and some of them to the dispose station (final cancelation).

```python
simulator = queuesim.Simulator()

source = Source(simulator, count, get_i)
process = Process(simulator, get_s, c, getNu=getNu)
decide = Decide()
dispose = Dispose(simulator)

source.set_next(process)
process.set_next(dispose)
process.set_next_cancel(decide)
decide.add_next(process, 0.4)  # 40% will retry
decide.add_next(dispose, 1 - 0.6)
```

In many cases clients will wait some time before starting a retry. This can be modeled by adding a `Delay` station between the decide and the process station. `decide.add_next(process, 0.4)` will be changed to `decide.add_next(delay, 0.4)`. `delay` will delay the clients and then send them back to the process station.


## Helper function

As for plain M/M/c models there is also a helper function in `queuesim.models` for creating queueing models with impatience and retry:

```python
model = impatience_and_retry_model_build(mean_i, mean_s, mean_wt, retry_probability, mean_retry_delay, c, count)
simulator = get_simulator_from_model(model)

simulator.run()
```


## Example Jupyter notebook

See [`example_sim_call_center.ipynb`](example_sim_call_center.ipynb) for a complete example of a model with impatience and retry.