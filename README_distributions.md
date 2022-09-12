# Random number distributions

At many stations random numbers are used for handling clients. This can be inter-arrival times, service times, waiting time tolerances etc. User-defined lambda expressions are used to generate these numbers. Each time a random number is needed the corresponding lambda expression is evaluated. This allows to use any random number distribution and also to define any complex function for this. (For example the inter-arrival times can be adjusted depending on the current number of clients in the system etc.)

To make thinks as easy as possible there are some lambda factory methods in `queuesim.random_dist`:

* Exponential distribution: `exp(mean)`
* Log-normal distribution: `log_normal(mean, sd)`
* Gamma distribution: `gamma(mean, sd)`
* Uniform distribution: `uniform(low, high)`
* Triangular distribution: `uniform(low, most_likely, high)`
* Deterministic: `deterministic(fixed_value)`
* Empirical: `empirical(options)` where `options` is a `dict` of values to rates

Since the gamma distribution is a generalization of the Erlang distribution, the quite common Erlang distribution is also covered.

Note that the parameters for `log_normal` and `gamma` are `mean` and `sd`. So no manual converting from mean and standard deviation to $\mu$, $\sigma$, ... is needed.

The generator functions will return strings containing lambda expressions. The strings are evaluated inside the stations on first usage. This is needed for serialization for multi-process simulation. If you do not want to use multi-process parallelization, you can also add the parameter `as_lambda=True` to get lambda expressions directly. The stations will understand both: strings and lambdas.