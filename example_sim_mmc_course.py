# Course of the number of clients in the system
# The notebook shows how to simulate a M/M/c model and record the number of clients in the system over the time.


# Importing modules

# Plotting modules
import matplotlib.pyplot as plt
import seaborn as sns

# Simulation
from queuesim.models import mmc_model, get_simulator_from_model

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
count = 500


# Simulation

# Build model
model = mmc_model(mean_i, mean_s, c, count, record_values=True)

# Run simulation
simulator = get_simulator_from_model(model)
simulator.run()


# Show course of the number of clients in the system

# Prepare values
wip = model['Process'].statistic_wip
times, values = wip.values

# Plot
fig, ax = plt.subplots(figsize=(16, 9))
ax.plot(times, values)
ax.set_title("Course of the number of clients in the system")
ax.set_xlabel("Time")
ax.set_ylabel("Number of clients in the system E[N]")
plt.show()