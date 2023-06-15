# Allen Cunneen approximation (GI/G/c model)
# For models with general inter-arrival and service times there are no exact analytic solutions. The Allen Cunneen formula will give some approximation results.


# Importing modules

# Erlang module
from queuesim.analytic import ac_approx_table

# Plotting modules
import matplotlib.pyplot as plt
import matplotlib.ticker as formater
import seaborn as sns

# Defining general plot style
sns.set()
percent_formater = formater.PercentFormatter(xmax=1, decimals=0)


# Mean waiting time as a function of the coefficient of variation of the service times

# Arrival rate
l = 1 / 100

# Service rate
mu = 1 / 80

# Number of operators
c = 1

# Coefficient of variation of the inter-arrival times
cv_i = 1  # exponential distribution has always cv_i = 1

# Coefficient of variation of the service times range
cv_s_range = [i / 10 for i in range(5, 16)]

# Allen Cunneen results for different values of cv_s
results = ac_approx_table([(l, mu, c, cv_i**2, cv_s**2) for cv_s in cv_s_range])

# Display results table
print(results)


# Plot results

fig, ax = plt.subplots(figsize=(16, 9))

ax.plot(results["CV[S]"], results["E[W]"], 'r')
ax.tick_params(axis='y', labelcolor='r')
ax.set_xlabel("Coefficient of variation of the service times CV[S]")
ax.set_ylabel("E[W]", color='r')
ax.xaxis.set_major_formatter(percent_formater)

ax = ax.twinx()
ax.plot(results["CV[S]"], results["rho"], 'g')
ax.tick_params(axis='y', labelcolor='g')
ax.set_ylabel("Utilization $\\rho$", color='g')
ax.yaxis.set_major_formatter(percent_formater)

ax.set_title("Allen Cunneen model at different coefficients of variation of the service times")

plt.show()

# The mean waiting time is increasing at increasing variations of the service times (at fixed utilization).
