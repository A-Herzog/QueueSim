# Analytic and simulation results for a simple M/M/c model


# Importing modules

# Plotting modules
import matplotlib.pyplot as plt
import matplotlib.ticker as formater
import seaborn as sns

# Simulation
from queuesim.models import mmc_model, mmc_results, get_simulator_from_model

# Analytic calcution
from queuesim.analytic import erlang_c

# Defining general plot style
sns.set()


# Model parameters

# Mean inter-arrival time
mean_i = 100

# Mean service time
mean_s = 800

# Number of operators
c = 10

# Number of arrivals to be simulated
count = 100_000


# Simulation

# Build model
model = mmc_model(mean_i, mean_s, c, count)

# Run simulation
simulator = get_simulator_from_model(model)
simulator.run()

# Show results
print(mmc_results(model))
print("")


# Analytic results (Erlang C)

analytic = erlang_c(1 / mean_i, 1 / mean_s, c)
print("Erlang C results")
print("E[N_Q]=", round(analytic.ENQ, 2), sep="")
print("E[N]=", round(analytic.EN, 2), sep="")
print("E[W]=", round(analytic.EW, 2), sep="")
print("E[V]=", round(analytic.EV, 2), sep="")
print("rho=", round(analytic.rho * 100, 2), "%", sep="")


# Frequency distribution of the waiting times of the clients

# Get frequency distribution of the waiting times
stat = model['Dispose'].statistic_client_waiting

# Build histogram values
hist_y_sum = sum(stat.histogram)
hist_y = stat.histogram
hist_x = [i * stat.histogram_stepwide for i in range(len(hist_y))]

# Build P(W=t) by Erlang C formula
erlang_hist_x = range(0, len(stat.histogram) * stat.histogram_stepwide, stat.histogram_stepwide)
erlang_hist_y = []
last = 0
for t in erlang_hist_x:
    value = analytic.Pt(t)
    erlang_hist_y.append(value - last)
    last = value

# Show histogram
fig, ax = plt.subplots(figsize=(16, 9))
ax.bar(hist_x, hist_y, width=stat.histogram_stepwide * 0.75)
ax.set_ylim([0, max(hist_y[1:])])
ax.yaxis.set_major_formatter(formater.PercentFormatter(xmax=hist_y_sum, decimals=1))
ax.tick_params(axis='y', labelcolor='b')
ax.set_ylabel("Probability from simulation", color='b')
ax.set_xlabel("Waiting time")

ax = ax.twinx()
ax.plot(erlang_hist_x, erlang_hist_y, 'r', linewidth=2)
ax.set_ylim([0, hist_y[1] / hist_y_sum])
ax.yaxis.set_major_formatter(formater.PercentFormatter(xmax=1, decimals=1))
ax.tick_params(axis='y', labelcolor='r')
ax.set_ylabel("Probability from Erlang C", color='r')

ax.set_title("Frequency distribution of the waiting times of the clients")
plt.show()
