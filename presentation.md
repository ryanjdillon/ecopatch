# Backwards simulation

For the forward simulation, the psudo-code from Marks book was followed with the same parameterization. These parameters are set in the config file (see [README.md](README.md)).

The majority of the backwards simulation algorithm is in [`backward.py`](backward.py), with comments delimiting the sections described in the pseudo-code:

```python
    # STEP 1 - initialize fitness arrays
    print('\nInitialize vectors...')
    F0, F1, D = init_f(x_crit, x_max)

    # Print and/or log fitness values
    dtypes = numpy.dtype([('t',  int),      # timestep
                          ('state', float), # state
                          ('F0', float), # state
                          ('F1', float), # state
                          ('patch', int),    # organism id
                          ])

    landscape = numpy.zeros(n_timesteps*(x_max), dtypes)

    # STEP 2 - Iterate over timesteps, getting max fitness values
    for t in reversed(range(n_timesteps)):
        F0, D = max_v(x_crit, x_max, patches, F0, F1, D)

        # STEP 3 - Print/log fitness value and optimal index with t
        landscape = log_vals(t, x_crit, x_max, F0, F1, D, landscape)

        if display:
            print_vals(t, x_crit, x_max, F0, F1, D)

        # STEP 4 - Copy F0 to F1, updates fitness function to F(x,t,T)
        for x in range(0, x_max+1):
            F1[x] = F0[x]

        # STEP 5 - Reduce timestep
        t -= 1
```

I managed to get the pseudo code to work without fully understanding the concept of the model. A chat with Gabby and Tom sorted that out. Thanks guys! :thumbsup:


# Forward simulation

I didnt see the bit about the forward simulation in the book until after I winged it. The majority of the forward simulation algorithm is in [`forward.py`](forward.py), which goes through the following steps for each timestep and organism: 

```python
    # Get index for row corresponding to timestep and state
    idx = (landscape['t'] == t) & (landscape['state'] == o.state)
    # Move organism to optimal patch (i.e. D[x])
    o.patch = int(landscape[idx]['patch'])

    # Only update feeding and mortality for living organisms
    if o.alive==True:

        # Find food based on patch probability of finding food
        prob_food = patches[o.patch]['prob_food']
        cost = patches[o.patch]['cost']
        increment = patches[o.patch]['state_increment']

        food_found = numpy.random.choice([1,0], 1, p=[prob_food, 1-prob_food])

        # Subtract cost, add increment if food found
        # only allow state to be increased to maximum
        if food_found & (o.state-cost+increment <= x_max):
            o.state = o.state - cost + increment
        elif food_found & (o.state-cost+increment > x_max):
            o.state = float(x_max)
        elif food_found == 0:
            o.state = o.state - cost

        # Kill organism if critical state reached
        if o.state <= float(x_crit):
            o.alive = False

        # Kill organism based on patch probability of predation
        prob_pred = patches[o.patch]['prob_pred']
        alive_pred = numpy.random.choice([1,0], 1, p=[1-prob_pred, prob_pred])
        # if died from starvation or predation, set dead
        if (o.alive==False) | (alive_pred==False):
            o.alive = False
```

After winging it, I made a plotting app, using `Bokeh`, which revieled I had almost correct numbers, but there were still organisms in patch 1 (using `python` indexing convention), which shouldnt have been according to the optimal strategy landscape. See [the readme](README.md) for directions on running it.

I went to back to the book, but when reading it, it felt far more complicated than my interpretation of things, so I stopped reading. He quickly pointed out the errors, and I went and fixed them.

By far the longest use of my time on this was making the `Bokeh` app, but it helped quite a lot in the end seeing that my numbers were alright (I think), so time well spent. 
