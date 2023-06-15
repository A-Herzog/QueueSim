# Distribution pseudo random numbers generators tests
# QueueSim defines random number generators for some distributions. To test these generators, random numbers are generated and plotted as histograms.


# Importing modules

import math

# Plotting modules
import matplotlib.pyplot as plt
import matplotlib.ticker as formater
import seaborn as sns

# Generating pseudo random numbers
import queuesim.random_dist as rnd

# Recording statistics
from queuesim.statistics import RecordDiscrete

# Defining general plot style
sns.set()


# Helper function for generating random numbers and showing the results of the tests

def generate_random_numbers(generator) -> RecordDiscrete:
    statistics = RecordDiscrete()
    for i in range(1_000_000):
        statistics.record(generator())
    return statistics


def show_results(mean: float, sd: float, statistics: RecordDiscrete) -> None:
    print("Defined mean = ", mean, sep="")
    print("Defined standard deviation = ", sd, sep="")
    print("Generated random numbers:", statistics.count)
    print("Actual mean = ", round(statistics.mean, 2), " (relative deviation: ", round(abs(statistics.mean - mean) / mean * 100, 2), "%)", sep="")
    if sd > 0:
        print("Actual standard deviation = ", round(statistics.sd, 2), " (relative deviation: ", round(abs(statistics.sd - sd) / sd * 100, 2), "%)", sep="")
    else:
        print("Actual standard deviation = ", round(statistics.sd, 2), " (absolute deviation: ", round(abs(statistics.sd - sd), 2), ")", sep="")


def plot_results(statistics: RecordDiscrete, name: str) -> None:
    hist_y_sum = sum(statistics.histogram)
    hist_y = statistics.histogram
    hist_x = [i * statistics.histogram_stepwide for i in range(len(hist_y))]

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.bar(hist_x, hist_y, width=statistics.histogram_stepwide * 0.75)
    ax.yaxis.set_major_formatter(formater.PercentFormatter(xmax=hist_y_sum, decimals=1))
    ax.set_title("Frequency distribution of the generated pseudo random numbers (" + name + ")")


# Deterministic

mean = 100

generator = rnd.deterministic(mean, as_lambda=True)
statistics = generate_random_numbers(generator)

print("")
print("Deterministic")
show_results(mean, 0, statistics)  # Deterministic: standard deviation = 0
plot_results(statistics, "one-point distribution")
plt.show()


# Exponential distribution

mean = 100

generator = rnd.exp(mean, as_lambda=True)
statistics = generate_random_numbers(generator)

print("")
print("Exponential distribution")
show_results(mean, mean, statistics)  # Exponential distribution: mean = standard deviation
plot_results(statistics, "exponential distribution")
plt.show()


# Log-normal distribution

mean = 100
sd = 40

generator = rnd.log_normal(mean, sd, as_lambda=True)
statistics = generate_random_numbers(generator)

print("")
print("Log-normal distribution")
show_results(mean, sd, statistics)
plot_results(statistics, "log-normal distribution")
plt.show()


# Gamma distribution

mean = 100
sd = 40

generator = rnd.gamma(mean, sd, as_lambda=True)
statistics = generate_random_numbers(generator)

print("")
print("Gamma distribution")
show_results(mean, sd, statistics)
plot_results(statistics, "gamma distribution")
plt.show()


# Trigangular distribution

low = 20
high = 100
most_likely = 80

mean = (low + most_likely + high) / 3
sd = math.sqrt((high - low)**2 + (high - most_likely)**2 + (most_likely - low)**2) / 6

generator = rnd.triangular(low, most_likely, high, as_lambda=True)
statistics = generate_random_numbers(generator)

print("")
print("Triangular distribution")
show_results(mean, sd, statistics)
plot_results(statistics, "triangular distribution")
plt.show()


# Uniform distribution

low = 20
high = 100
mean = (low + high) / 2
sd = (high - low) / math.sqrt(12)

generator = rnd.uniform(low, high, as_lambda=True)
statistics = generate_random_numbers(generator)

print("")
print("Uniform distribution")
show_results(mean, sd, statistics)
plot_results(statistics, "uniform distribution")
plt.show()


# Empirical values

options = {10: 5, 20: 15, 30: 25, 40: 15, 50: 5}
generator = rnd.empirical(options, as_lambda=True)
statistics = generate_random_numbers(generator)

statRecord = RecordDiscrete()
for key in options:
    for i in range(0, options[key]): statRecord.record(key)

print("")
print("Empirical values")
show_results(statRecord.mean, statRecord.sd, statistics)
plot_results(statistics, "empirical values")
plt.show()
