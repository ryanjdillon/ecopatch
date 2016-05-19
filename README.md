# ecopatch

A python implementation of the optimization patch model in Mark Mangel and Colin Whitcomb's book 'Dynamic Modeling in Behavioral Ecology' , 1998. [link](http://press.princeton.edu/titles/4309.html)
=======
A python implementation of Mark Mangler's optimization patch model

## Configuration
The following parameters are set in the configuration file `simulations.cfg`:

*Backward simulation parameters*
* n_timesteps: number of timesteps for the simulation
* x_crit: the state value at which the animal will die
* x_max: the maximum state the animal can reach through feeding, etc.
* cost: list of values corresponding to each patches' energetic cost per timestep
* prob pred: list of values corresponding to each patches' probability of predation
* prob food: list of values corresponding to each patches' probability of finding food
* state_increment: list of values corresponding to each patches' increase in state when food is found

*Forward simulation parameters*
* n_organisms: the number of organisms to simulate
* init_state: the state each animal begins with at the start of the simulation

The default configuration is taken from Mark Mangel's book and excel demonstration of the model, defined under the line `[DEFAULT]`.

Additional parameterizations can be tested by creating a new configuration group, and a new header line (e.g. `[sim]`).
