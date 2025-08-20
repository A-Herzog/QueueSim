# Minimal M/M/1 simulator
# This example shows how to simulate a M/M/1 model (without using any QueueSim classes).


# Importing modules

# Generating multiple pseudo random numbers as an array
import numpy as np

# Comparison with analytical results
from queuesim.analytic import erlang_c

# Plotting modules
import matplotlib.pyplot as plt
import matplotlib.ticker as formater

# Defining general plot style
plt.style.use('seaborn-v0_8')


# Model parameters

# Means inter-arrival time
mean_i = 100

# Means service time
mean_s = 80

# Number of arrivals to be simulated
count = 5_000_000


# The 4 line simulation code
# By exchanging `np.random.exponential` with other random number generators the model can be generalized to G/G/1.

waiting_sum = server_free_at = 0
for (time, s) in zip(np.cumsum(np.random.exponential(mean_i, count)), np.random.exponential(mean_s, count)):
    waiting_sum += max(0, server_free_at - time)
    server_free_at = max(server_free_at, time) + s


# Output simulation result

print("Simulation result")
print("E[W]=", round(waiting_sum / count, 2), sep="")


# Comparison with analytics results (Erlang C)

result = erlang_c(1 / mean_i, 1 / mean_s, 1)

print("Erlang C results")
print("E[NQ]=", round(result.ENQ, 2), sep="")
print("E[N]=", round(result.EN, 2), sep="")
print("E[W]=", round(result.EW, 2), sep="")
print("E[V]=", round(result.EV, 2), sep="")
print("\N{greek small letter rho}=", round(result.rho * 100, 1), "%", sep="")


# Mean waiting time as a function of the inter-arrival times using the minimal simulator

# Simulator as a function
def mm1_sim(mean_i: float, mean_s: float, count: int) -> float:
    waitingSum = server_free_at = 0
    for (time, s) in zip(np.cumsum(np.random.exponential(mean_i, count)), np.random.exponential(mean_s, count)):
        waitingSum += max(0, server_free_at - time)
        server_free_at = max(server_free_at, time) + s
    return waitingSum / count


# Parameters
mean_i = 100
mean_s_range = range(70, 91)
count = 500_000

# Run simulations
rho, EW = zip(*[(mean_s / mean_i, mm1_sim(mean_i, mean_s, count)) for mean_s in mean_s_range])

# Show results
_, ax = plt.subplots(figsize=(16, 9))
ax.plot(rho, EW)
ax.xaxis.set_major_formatter(formater.PercentFormatter(xmax=1, decimals=1))
ax.set_xlabel("Utilization $\\rho$")
ax.set_ylabel("Mean waiting time E[W]")
plt.show()
