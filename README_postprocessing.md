# Post-processing times

If an operator performs activities with reference to a client whose service has just been completed, this is referred to as a post-processing time. Post-processing times occur particularly in the call center area. At process stations, post-processing times can be defined via the optional parameter `getS2=`. Example:

```python
from queuesim.random_dist import exp as exp_dist

get_s=ex_dist(80)
get_s2=exp_dist(60)

process = Process(simulator, get_s, c, getS2=get_s2)
```


## Example Jupyter notebook

See also [`example_sim_call_center.ipynb`](example_sim_call_center.ipynb).