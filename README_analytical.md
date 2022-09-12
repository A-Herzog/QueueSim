# Calculating analytical results

Simple queueing models can be solved analytically by using the Erlang formula or at least approximate analytically by using the Allen Cunneen formula.

While the Erlang formulas require exponentially distributed inter-arrival and serivce times, the Allen Cunneen formula allows inter-arrival and serivce times of any type. Only the expected value and the coefficient of variation need to be known.

The function for calculating the analytical values are located in the `queuesim.analytic` module. There are classes for calculating the performance indicators for individual input values and helper function for getting tables for ranges of input parameters.

The following four example Jupyter notebooks show how to use the functions offered at `queuesim.analytic`:

* Erlang B formula for M/M/c/c models: [`example_analytic_erlang_b.ipynb`](example_analytic_erlang_b.ipynb)
* Erlang C formula for M/M/c models [`example_analytic_erlang_c.ipynb`](example_analytic_erlang_c.ipynb)
* Extended Erlang C formula (with impatient clients) for M/M/c/K+M models: [`example_analytic_erlang_c_ext.ipynb`](example_analytic_erlang_c_ext.ipynb)
* Allen Cunneen approximation formula for GI/G/c models: [`example_analytic_ac_approx.ipynb`](example_analytic_ac_approx.ipynb)