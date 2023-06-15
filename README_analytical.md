# Calculating analytical results

Simple queueing models can be solved analytically by using the Erlang formula or at least approximate analytically by using the Allen Cunneen formula.

While the Erlang formulas require exponentially distributed inter-arrival and service times, the Allen Cunneen formula allows inter-arrival and service times of any type. Only the expected value and the coefficient of variation need to be known.

The function for calculating the analytical values are located in the `queuesim.analytic` module. There are classes for calculating the performance indicators for individual input values and helper function for getting tables for ranges of input parameters.



## `erlang_b` class

The `erlang_b` and the helper function `erlang_b_table` can be used to calculate values of the Erlang-B formula.
For a complete example see [`example_analytic_erlang_b.ipynb`](example_analytic_erlang_b.ipynb) or [`example_analytic_erlang_b.py`](example_analytic_erlang_b.py).

```python
from queuesim.analytic import erlang_b, erlang_b_table

# Calculate single value

a = 5  # Workload
c = 7  # Number of operators

erl = erlang_b(a, c)

print("Utilization (at system entry):", erl.rho_offered)
print("Real utilization of the operators:", erl.rho_real)
print("Average number of clients in system: ", erl.EN)
print("Probability for a new arriving client of being blocked:", erl.p_blocked)

# Calculate multiple values

input_parameters_list = [(a, c) for a in range(1,7)]  # List of tuples (a, c)

results = erlang_b_table(input_parameters_list)

# result is a DataFrame containing columns for a, c, rho_offered, rho_real, E[N], P(blocked)
```



## `erlang_c` class

The `erlang_c` and the helper function `erlang_c_table` can be used to calculate values of the Erlang-C formula.
For a complete example see [`example_analytic_erlang_c.ipynb`](example_analytic_erlang_c.ipynb) or [`example_analytic_erlang_c.py`](example_analytic_erlang_c.py).

```python
from queuesim.analytic import erlang_c, erlang_c_table

# Calculate single value

l = 1/100  # Arrival rate lambda
mu = 1/80  # Service rate mu
c = 1  # Number of operators

erl = erlang_c(l, mu, c)

print("Workload:", erl.a)
print("Utilization:", erl.rho);
print("Average queue length: ", erl.ENQ)
print("Average number of clients in system: ", erl.EN)
print("Average waiting time: ", erl.EW)
print("Average residence time: ", erl.EV)

# Calculate multiple values

l_range = [1 / mean_i for mean_i in range(61, 100)]

input_parameters_list = [(l, mu, c) for l in l_range]  # List of tuples (lambda, mu, c)

results = erlang_c_table(input_parameters_list)

# result is a DataFrame containing columns for lambda, mu, a, c, rho, E[N_Q], E[N], E[W], E[V]
```



## `erlang_c_ext` class

The `erlang_c_ext` and the helper function `erlang_c_ext_table` can be used to calculate values of the extended Erlang-C formula (including impatience and a limited system size).
For a complete example see [`example_analytic_erlang_c_ext.ipynb`](example_analytic_erlang_c_ext.ipynb) or [`example_analytic_erlang_c_ext.py`](example_analytic_erlang_c_ext.py).

```python
from queuesim.analytic import erlang_c_ext, erlang_c_ext_table

# Calculate single value

l = 1/100  # Arrival rate lambda
mu = 1/90  # Service rate mu
nu = 1/300  # Cancelation rate nu
c = 1  # Number of operators
K = 100  # Maximum number of clients in system

erl = erlang_c_ext(l, mu, nu, c, K)

print("Utilization (at system entry):", erl.rho_offered)
print("Real utilization of the operators:", erl.rho_real)
print("Probability for a new arriving client of being blocked:", erl.p_blocked)
print("Percentage of the clients canceling waiting:", erl.PA)
print("Average queue length: ", erl.ENQ)
print("Average number of clients in system: ", erl.EN)
print("Average waiting time: ", erl.EW)
print("Average residence time: ", erl.EV)

# Calculate multiple values

l_range = [1 / mean_i for mean_i in range(50, 100)]

input_parameters_list = [(l, mu, nu, c, K) for l in l_range]  # List of tuples (lambda, mu, nu, c, K)

results = erlang_c_ext_table(input_parameters_list)

# result is a DataFrame containing columns for lambda, mu, nu, a, c, K, rho_offered, rho_real, P(blocked), P(A), E[N_Q], E[N], E[W], E[V]

```



## `ac_approx` class

The `ac_approx` and the helper function `ac_approx_table` can be used to calculate values of the Allen Cunneen approximation formula.
For a complete example see [`example_analytic_ac_approx.ipynb`](example_analytic_ac_approx.ipynb) or [`example_analytic_ac_approx.py`](example_analytic_ac_approx.py).

```python
from queuesim.analytic import ac_approx, ac_approx_table

# Calculate single value

l = 1/100  # Arrival rate lambda
mu = 1/80  # Service rate mu
c = 1  # Number of operators
scv_i = 1  # Squared coefficient of variation of the inter-arrival times
scv_s = 0.5  # Squared coefficient of variation of the service times

ac = ac_approx(l, mu, c, scv_i, scv_s)

print("Workload:", ac.a)
print("Utilization:", ac.rho);
print("Average queue length: ", ac.ENQ)
print("Average number of clients in system: ", ac.EN)
print("Average waiting time: ", ac.EW)
print("Average residence time: ", ac.EV)

# Calculate multiple values

l_range = [1 / mean_i for mean_i in range(61, 100)]

input_parameters_list = [(l, mu, c, scv_i, scv_s) for l in l_range]  # List of tuples (lambda, mu, c, SCV[I], SCV[S])

results = approx_ac_table(input_parameters_list)

# result is a DataFrame containing columns for lambda, mu, a, c, rho, CV[I], CV[S], SCV[I],SCV[S], E[N_Q], E[N], E[W], E[V]
```



## Example files

The following four examples (plain Python files and Jupyter notebooks) show how to use the functions offered at `queuesim.analytic`:

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