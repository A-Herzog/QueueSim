# Parallelization

Due to the global interpreter lock Python can only run one simulation thread at time. To run multiple simulations (for example of a parameter study) in parallel **multiple processes** need to be used. A simulation process can be encapsulated by objects of the class `SimProcess` (offered by module `queuesim`). The constructor of `SimProcess` requires as parameter a `Dict` containing the model.

An list of `SimProcess` objects can be run in parallel by using the `run_parallel` function (also from `queuesim`).

```python
from queuesim import SimProcess, run_parallel
from queuesim.models import mmc_model

# Input parameters
mean_i = 100
mean_s_range = range(70, 93)
c = 1
count = 100_000

# Generate processes
processes=[SimProcess(mmc_model(mean_i, mean_s, c, count)) for mean_s in mean_s_range]

# Run processes and wait for termination of all processes
models, simulators = run_parallel(processes)
```


## Limitations

To send models to sub processes the data need to be serialized. Since only simple objects (numbers, strings, etc.) can be serialized, no lambda expressions for getting inter-arrival times, service times etc. can be used in the model. When using the convenience functions from `queuesim.random_dist` (see [Random number distributions](README_distributions.md)) this is no problem. The generator functions can return lambda expressions or strings that can be evaluated to lambda expressions. If the `as_lambda=True` parameter is not used, they will return strings. All stations of QueueSim can handle lambda expressions as well as strings for inter-arrival times, service times etc. The strings will be evaluated to function object on first use (this means: in the sub process, after serialization and unserialization).


## Example Jupyter notebook

See [`example_sim_mmc_series.ipynb`](example_sim_mmc_series.ipynb) for a complete example of using multiple simulation processes in parallel.
