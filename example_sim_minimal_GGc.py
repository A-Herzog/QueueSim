# Minimal G/G/c simulator
# This example shows how to simulate a G/G/c model (without using any QueueSim classes).


# Importing modules

# Generating multiple pseudo random numbers as an array and fast array processing
import numpy as np

# Comparison with analytical results
from queuesim.analytic import erlang_c


# Model parameters

# Means inter-arrival time
mean_i = 100

# Means service time
mean_s = 240

# Number of operators
c = 3

# Number of arrivals to be simulated
count = 1_000_000


# Generate random arrival times and service times

# Instead of `np.random.exponential` any other random distribution could also be used. The simulation process is not limited to exponential inter-arrival and service times.

arrival_times = np.cumsum(np.random.exponential(mean_i, count))  # Absolute arrival times, not inter-arrival times
service_times = np.random.exponential(mean_s, count)


# The complete simulation code

waiting_sum = 0
server_free_at = np.zeros(c)

for (time, service_time) in zip(arrival_times, service_times):
    index = np.argmin(server_free_at)  # Find next free server
    service_start = max(time, server_free_at[index])
    waiting_sum += service_start - time
    server_free_at[index] = service_start + service_time  # Store new time when server gets idle again


# Output simulation results

service_sum = np.sum(service_times)
l = 1 / np.mean(arrival_times[1:] - arrival_times[:-1])  # Calculate lambda from absolut arrival times

EW = waiting_sum / count
EV = (waiting_sum + service_sum) / count
ENQ = EW * l  # Since Little holds for all types of inter-arrival and service time distributions
EN = EV * l  # we can calculate E[NQ] and E[N] from E[W] and E[V] and do not need to record them directly
rho = service_sum / arrival_times[-1] / c  # Sum of all service times divided by last arrival time divided by c

print("Simulation results")
print("E[NQ]=", round(ENQ, 2), sep="")
print("E[N]=", round(EN, 2), sep="")
print("E[W]=", round(EW, 2), sep="")
print("E[V]=", round(EV, 2), sep="")
print("\N{greek small letter rho}=", round(rho * 100, 1), "%", sep="")


# Comparison with analytics results (Erlang C)

result = erlang_c(1 / mean_i, 1 / mean_s, c)

print("Erlang C results")
print("E[NQ]=", round(result.ENQ, 2), sep="")
print("E[N]=", round(result.EN, 2), sep="")
print("E[W]=", round(result.EW, 2), sep="")
print("E[V]=", round(result.EV, 2), sep="")
print("\N{greek small letter rho}=", round(result.rho * 100, 1), "%", sep="")
