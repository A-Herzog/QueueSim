# Client types

Clients of different types can have different service times or can be branched in different directions. The client type is a string and can be accessed via the `type_name` attribute of a `Client` object.



## Source

The type of a client is determined on creation of the client object. All clients created at a source object will have the same client type. The type of the clients created at a source can be defined via the optional `client_type_name=` parameter of the constructor of the `Source`. Example:

```python
import queuesim
from queuesim.random_dist import exp as exp_dist
from queuesim.stations import Source, ...

simulator = queuesim.Simulator()

count1 = 50_000
count2 = 50_000
get_i1 = exp_dist(200)
get_i2 = exp_dist(200)

source1 = Source(simulator, count1, get_i1, client_type_name="Clients A")
source2 = Source(simulator, count2, get_i2, client_type_name="Clients B")
```



## Process

At process stations the service times and the (optional) waiting time tolerances are defined via the `getS=` and `getNu=` attributes. These times always applies if there are no client type specific times. Client type specific times can be defined via the optional parameters `getS_client_type=` and `getNu_client_type=`. Both are of the type `dict` defining lambda expressions for different client types. Example:

```python
import queuesim
from queuesim.random_dist import exp as exp_dist
from queuesim.stations import Process, ...

simulator = queuesim.Simulator()

process = Process(simulator, exp_dist(100), c=3, getS_client_type = {"Clients A": exp_dist(120)})
```

Clients of type A will have a mean service time of 120 time units at this process station. All other clients will have a mean service time of 100 time units.



## DecideClientType

Clients can be branched in different directions using `DecideClientType` stations. At this stations the `set_next` method expects a client type name and a following station. Example:

```python
import queuesim
from queuesim.stations import DecideClientType, Dispose, ...

simulator = queuesim.Simulator()

decide = DecideClientType(simulator)
dispose1 = Dispose(simulator)
dispose2 = Dispose(simulator)

decide.set_next("Clients A", dispose1)
decide.set_next_default(dispose2)
```

## Example files

See [`example_sim_mmc_priorities2.ipynb`](example_sim_mmc_priorities2.ipynb) or [`example_sim_mmc_priorities2.py`](example_sim_mmc_priorities2.py) for the usage of different client types.