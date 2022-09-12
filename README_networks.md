# Queueing networks

Since the connection of the stations is completely user-defined (by using the `set_next` methods of the stations) any type of queueing network can be implemented. Retry or rework can be implemented easily.

For larger networks consisting only of sources, process stations and dispose stations there is a helper function `build_network_model` in `queuesim.models` hat can build station networks based on transitions matrices. Lets assume we have a single source object named `source`, two process station objects `process1` and `process2` and a dispose object `dispose`. We want to send 80% of the clients from the source to `process1` and 20% to `process2`. When leaving `process2` all clients are to be sent to `process1`. When leaving `process1` 30% or the clients are sent to `process2` and 70% well leave the system.

A model implementing this network can be created by:

```python
simulator = Simulator()
source = Source(...)
process1 = Process(...)
process2 = Process(...)
dispose = Dispose()

connections1=[[0.8, 0.2]]  # 80% of the clients go to process1, 20% to process2
connections2=[[0.0, 0.3, 0.7], [1, 0, 0]]  # Most clients leave system after process1, some go to process2; all clients from process2 go to process1

build_network_model([source],[process1,process2],[dispose],connections1,connections2)

simulator.run()
```

Assume we have m<sub>1</sub> sources, m<sub>2</sub> process stations and m<sub>3</sub> dispose stations, then the first transition rates matrix has the shape m<sub>1</sub> &times; m<sub>2</sub> and the second transition rates matrix has the shape m<sub>2</sub> &times; (m<sub>2</sub>+m<sub>3</sub>).

## Displaying the queueing network

If you want to get a graphical representation of your queueing network, you can use `queueim.build_graph(list_of_sources)` to get a digraph which can be plotted using `networkx`:

```python
dg = build_graph([source])
fig, ax = plt.subplots(figsize=(19, 9))
nx.draw(dg, ax=ax, with_labels=True, node_color='#CCCCFF', node_size=2000, arrowsize=30, width=2)
```

## Example Jupyter notebook

See [`example_sim_network.ipynb`](example_sim_network.ipynb) for a complete example of creating a queueing network using `build_network_model`.
