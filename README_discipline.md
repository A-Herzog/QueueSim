# Queueing discipline

In the default case clients are served at a process station in arrival order (first in, first out; FIFO). This behavior can be influenced by two parameters of the `Process` constructor.


## LIFO

If you just want to switch from FIFO to LIFO (last in first out), you can add `LIFO=True` to the `Process` constructor.


## Priority based service

If you want to use some more complex, priority formula based queueing discipline, you can do this by adding a `getPriority=` parameter to the `Process` constructor. `getPriority` has to be a lambda with two parameters: the client object and the waiting time of the client at the current process station so far. The lambda has to return the current priority of the client.

Some examples for priority expressions that will result in FIFO, LIFO and random priority:

```python
def priority_FIFO(client, waiting_time):
    return waiting_time

def priority_LIFO(client, waiting_time):
    return -waiting_time

def priority_random(client, waiting_time):
    return random_float() * 100
```


## Different priorities for different client types

Priorities are often used to offer different client types different service qualities at the same process station. In this case the `client` parameter of the priority function is used to return different values for different client types. If you have a client type A for which each waiting second should have a 5 times higher value then for the other client types, you can model this by using this priority function:

```python
def priority(client, waiting_time):
    if client.type_name=="ClientsA":
        return 5*waiting_time
    else:
        return waiting_time
```

(The type of a client can be defined at a source station via the optional constructor parameter `client_type_name=`.)


## Example Jupyter notebooks

For FIFO, LIFO and random priorities see [`example_sim_mmc_priorities1.ipynb`](example_sim_mmc_priorities1.ipynb) and for client type dependent priorities see [`example_sim_mmc_priorities2.ipynb`](example_sim_mmc_priorities2.ipynb).