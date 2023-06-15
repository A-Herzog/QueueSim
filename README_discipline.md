# Queueing discipline

In the default case clients are served at a process station in arrival order (first in, first out; **FIFO**). This behavior can be influenced by two parameters of the `Process` constructor.



## LIFO service mode

If you just want to switch from FIFO to LIFO (last in first out), you can add `LIFO = True` to the `Process` constructor:

```python
import queuesim
from queuesim.stations import Process, ...
from queuesim.random_dist import exp as exp_dist

process = Process(simulator, exp_dist(80), c = 1, LIFO = True)
```



## Priority based service

If you want to use some more complex, priority formula based queueing discipline, you can do this by adding a `getPriority=` parameter to the `Process` constructor. `getPriority` has to be a lambda expression with two parameters: the client object and the waiting time of the client at the current process station so far. The lambda expression has to return the current priority of the client.

Some examples for priority expressions that will result in FIFO, LIFO and random priority:

```python
import queuesim
from queuesim.stations import Process, ...
from queuesim.random_dist import exp as exp_dist

def priority_FIFO(client, waiting_time):
    return waiting_time

def priority_LIFO(client, waiting_time):
    return -waiting_time

def priority_random(client, waiting_time):
    return random_float() * 100

process_FIFO = Process(simulator, exp_dist(80), c = 1, getPriority = priority_FIFO)
process_LIFO = Process(simulator, exp_dist(80), c = 1, getPriority = priority_LIFO)
process_random_order = Process(simulator, exp_dist(80), c = 1, getPriority = priority_random)
```



## Different priorities for different client types

Priorities are often used to offer different client types different service qualities at the same process station. In this case the `client` parameter of the priority function is used to return different values for different client types. If you have a client type A for which each waiting second should have a 5 times higher value than for the other client types, you can model this by using this priority function:

```python
import queuesim
from queuesim.stations import Source, Process, ...
from queuesim.random_dist import exp as exp_dist

def priority(client, waiting_time):
    if client.type_name == "ClientsA":
        return 5 * waiting_time
    else:
        return waiting_time

sourceA = Source(simulator, exp_dist(200), client_type_name="ClientsA")
sourceB = Source(simulator, exp_dist(200), client_type_name="ClientsB")
process = Process(simulator, exp_dist(80), c = 1, getPriority = priority)

sourceA.set_next(process)
sourceB.set_next(process)
```

(The type of a client can be defined at a source station via the optional constructor parameter `client_type_name=`.)


## Example files

For FIFO, LIFO and random priorities see [`example_sim_mmc_priorities1.ipynb`](example_sim_mmc_priorities1.ipynb) or [`example_sim_mmc_priorities1.py`](example_sim_mmc_priorities1.py) and for client type dependent priorities see [`example_sim_mmc_priorities2.ipynb`](example_sim_mmc_priorities2.ipynb) or [`example_sim_mmc_priorities2.py`](example_sim_mmc_priorities2.py).