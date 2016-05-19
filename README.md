# ecopatch

A python implementation of the optimization patch model in Mark Mangel and Colin Whitcomb's book 'Dynamic Modeling in Behavioral Ecology' , 1998. [link](http://press.princeton.edu/titles/4309.html)

## Install

```
git clone git@github.com:ryanjdillon/ecopatch.git
cd ecopatch
pip install -r requirements.txt
```
It is recommened (but not necessary) that you use python `virtualenv`. If using a "venv", then make sure to activate it before installed the dependencies with `pip`.

## Configuration
The default configuration is taken from Mark Mangel's book and excel demonstration of the model, with the parameters defined under the line `[DEFAULT]` in the configuration file `simulations.cfg`.

Additional parameterizations can be tested by creating a new configuration group, and a new header line (e.g. `[sim]`).

### Parameters
The following parameters should be defined in each config group in the configuration file:

#### Backward simulation parameters
* **n_timesteps**: number of timesteps for the simulation
* **x_crit**: the state value at which the animal will die
* **x_max**: the maximum state the animal can reach through feeding, etc.
* **cost**: list of values corresponding to each patches' energetic cost per timestep
* **prob pred**: list of values corresponding to each patches' probability of predation
* **prob food**: list of values corresponding to each patches' probability of finding food
* **state_increment**: list of values corresponding to each patches' increase in state when food is found

#### Forward simulation parameters
* **n_organisms**: the number of organisms to simulate
* **init_state**: the state each animal begins with at the start of the simulation


## Running the simulations
This should be improved a little, but currently you can run both the backward and forward simulations, but running the `forward.py` file as a script.

```
python forward.py
```

This will generate the files `landscape.npy` and `locations.npy`, which are binary dumps of the simulation output data. These files can be loaded for exploration in a Python interpreter by typing the following:
```
import numpy
landscape = numpy.load('landscape.npy')
locations = numpy.load('locations.npy')
```
Due to the stochasticity of the forward simulation, the output will vary each time.

## Visualizing with Bokeh
The file `main.py` is a script which generates a data-visualization app that can be run from a web browser. After running the simulations (this part can be integrated), run the following command to lauch the app:

```
bokeh serve --show main.py
```
