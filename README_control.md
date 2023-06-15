# Queueing systems with control

If a client arrival stream is distributed among several process stations and if certain rules are applied in this distribution, this is referred to as a queuing system with control.


## Base model

```python
import queuesim
from queuesim.stations import Source, Process, Dispose
from queuesim.random_dist import exp as exp_dist
from queuesim.models import mmc_results

count = 100_000
get_i = exp_dist(100)
get_s = exp_dist(160)
c1 = 1
c2 = 1

simulator = queuesim.Simulator()

source = Source(simulator, count, get_i)
decide = ...  # Select decide mode
process2 = Process(simulator, get_s, c1)
process2 = Process(simulator, get_s, c1)
dispose = Dispose(simulator)

source.set_next(decide)
...  # Setup decide mode
process1.set_next(dispose)
process2.set_next(dispose)

simulator.run()
```

The arriving clients (`source` station) are directed to some kind of decide station. From there the clients are send to `process1` or `process2`. At the process stations the arriving clients have to wait and then will be served. After this they leave the system (`dispose` station).


## Decide by chance

```python
from queuesim.stations import Decide

decide = Decide(simulator)

decide.add_next(process1, 1)
decide.add_next(process2, 1)
```

In this case 50% of the arriving clients are sent to `process1` and 50% to `process2`. No further control takes place. The second parameter in `add_next` is a rate. So you need not to enter a probability (the rates need not to sum up to exact 1). QueueSim will normalize the rates to probabilities when simulation starts.

The disadvantage of "decide by chance" is that on partial queue can run empty while clients who have chosen the other queue are still waiting. The available work performance of the two operators is not utilized well.

## Decide by shortest queue

```python
from random import randint
from queuesim.stations import DecideCondition

decide = DecideCondition(simulator)

def shortest_queue(client) -> int:
    nq1 = process1.nq
    nq2 = process2.nq
    if nq1 < nq2: return 0
    if nq1 > nq2: return 1
    return randint(0, 1)

decide.set_condition(shortest_queue)
decide.add_next(process1)
decide.add_next(process2)
```

Each time a client arrives at the decide station, the `shortest_queue` function is executed. If the queue at `process1` is shorter than the queue at `process2`, the client is sent to `process1`, i.e. to exit 0 (0-based) of the decide station. If the queue at `process1` is longer, the client is sent to `process2`. If both queue lengths are equal, the next station is chosen by chance (`randint(0, 1)`).

This method reduces the risk that one queue runs empty while there are clients in the other queue. But some risk still exists.

## More options

* **Single queue, faster operator**<br>This is just the M/M/c case but we have `get_s = exp_dist(80)` instead of `get_s = exp_dist(160)`. In this case there is only one queue so no control strategy is needed and a client can never choose the worse queue.
* **Single queue, two operators**<br>This is also a M/M/c model with `c=2`. There is also no control needed and there is also only a single queue.
* **Single queue, batch processing**<br>In this case we have `b=2`. This has the same result on the available work performance s the faster operator or as to have two default operators. But the there strategies still have some differences (see example notebook below).


## Example files

In [`exmaple_sim_shortest_queue.ipynb`](exmaple_sim_shortest_queue.ipynb) and in [`exmaple_sim_shortest_queue.py`](exmaple_sim_shortest_queue.py) the strategies descript above are implemented and the differences are explained.