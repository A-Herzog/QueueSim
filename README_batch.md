# Batch arrival and batch service

In the default case, clients arrive one at a time and are also served one at a time. But batch arrival and batch service can also be modeled in QueueSim.


## Batch arrival

The constructor of the `Source` class has the optional parameter `getB=`. If a lambda expression is passed here. This expression is evaluated on each arrival event. The integer number returned is used to determine the number of clients to be generated in this arrival event. After being created at the same time the clients move through the system as individual objects.


## Batch processing

The constructor of the `Process` has the optional parameter `b=`. If a positive integer number is passed here, clients are served in batch mode. This means, if there are less than `b` clients waiting at the station, the service process is not started. On the other side, a single operator will be able to serve `b` clients at the same time.