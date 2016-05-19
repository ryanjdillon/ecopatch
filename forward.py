def simulation(conf, landscape, log=True):
    '''Forward simulate individuals over patch-selection fitness landscape'''
    import numpy

    import backward

    # Backward parameters
    n_timesteps = int(conf['n_timesteps'])
    x_crit = int(conf['x_crit'])
    x_max = int(conf['x_max'])
    cost = backward.flist(conf['cost'])
    prob_pred = backward.flist(conf['prob_pred'])
    prob_food = backward.flist(conf['prob_food'])
    state_increment = backward.flist(conf['state_increment'])

    # Forward parameters
    n_organisms = int(conf['n_organisms'])
    init_state = float(conf['init_state'])

    # Gen number of timesteps from landscape array
    n_timesteps = len(numpy.unique(landscape['t']))

    # Get list of patch dictionaries for cacluating survival
    patches = backward.get_patches(cost, prob_pred, prob_food, state_increment)

    # Initialize organisms into array
    organisms = list()
    for i in range(n_organisms):
        organisms.append(Organism(i, init_state, landscape))

    # Initialize output data array - row: t, organism_id, x, patch
    dtypes = numpy.dtype([('t',  int),      # timestep
                          ('id', int),    # organism id
                          ('alive', int),  # alive
                          ('patch', int),   # organism id
                          ('state', float), # state
                          ])

    locations = numpy.zeros((n_timesteps)*n_organisms, dtypes)

    # Run simulation, with no `0` timestep
    for t in range(n_timesteps):
        for i in range(len(organisms)):
            locations = log_organism(t, n_organisms, organisms[i], locations)
            organisms[i] = traverse_landscape(t, organisms[i], n_timesteps-1,
                                              x_crit, x_max, patches,
                                              landscape)

    # Save locastions array to binary numpy file for retrieval
    if log:
        numpy.save("locations.npy", locations)

    return locations


class Organism(object):
    '''Organisms class for optimization patch selection model'''
    #TODO implement option of manually specifying patch
    def __init__(self, i, init_state, landscape):
        idx = (landscape['state']==init_state) & (landscape['t']==0)
        self.id = i
        self.alive = True
        self.patch = int(landscape[idx]['patch'])
        self.state = init_state


def traverse_landscape(t, o, t_max, x_crit, x_max, patches, landscape):
    '''Choose patch then process growth and mortality'''
    import numpy

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

    return o


def log_organism(t, n_organisms, o, locations):
    '''Save fitness values to array for archiving'''

    # Increment y index by t*n_organisms + organism id for each timestep
    idx = (t*n_organisms)+o.id

    # Fill row with t, organism id, current state, and current patch
    locations['t'][idx] = t
    locations['id'][idx] = o.id
    locations['alive'][idx] = o.alive
    locations['patch'][idx] = o.patch
    locations['state'][idx] = o.state

    return locations


def print_locations(locations):
    '''Print rows of locations array for cleaner viewing'''

    for i, (t, id, alive, patch, state) in enumerate(locations):
        print('[%4i] %3i %4i %2i %2i %2i' % (i, t, id, alive, state, patch))


if __name__ == '__main__':

    import backward

    # Read config file
    config_file = 'simulations.cfg'
    conf = backward.get_conf(config_file, 'DEFAULT')

    landscape = backward.simulation(conf, display=False, log=False)

    locations = simulation(conf, landscape, log=True)
