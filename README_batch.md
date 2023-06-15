# Batch arrival and batch service

In the default case, clients arrive one at a time and are also served one at a time. But batch arrival and batch service can also be modeled in QueueSim.


## Batch arrival

The constructor of the `Source` class has the optional parameter `getB=`. If a lambda expression is passed here, this expression is evaluated on each arrival event. The integer number returned is used to determine the number of clients to be generated in this arrival event. After being created at the same time the clients move through the system as individual objects.

```python
import queuesim
from queuesim.stations import Source, ...
from queuesim.random_dist import exp as exp_dist

simulator = queuesim.Simulator()

# Fixed arrival batch size of 5
fixed_batch_size = lambda: 5
source = Source(simulator, count = 100_000, getI = exp_dist(100), getB = fixed_batch_size)

# Random batch size in range from 3 to 5 (including both limits)
from random import randint
variable_batch_size = lambda: randint(3, 5)
source = Source(simulator, count = 100_000, getI = exp_dist(100), getB = variable_batch_size)
```


## Batch processing

The constructor of the `Process` has the optional parameter `b=`. If a positive integer number is passed here, clients are served in batch mode. This means, if there are less than `b` clients waiting at the station, the service process is not started. On the other side, a single operator will be able to serve `b` clients at the same time.

```python
import queuesim
from queuesim.stations import Process, ...
from queuesim.random_dist import exp as exp_dist

simulator = queuesim.Simulator()

# Serve clients in batches of size 3
process = Process(simulator, getS = exp_dist(80), c = 1, b = 3)
```
