def simulation(n_organisms, init_state, x_crit, x_max, landscape):
    '''Forward simulate individuals over patch-selection fitness landscape'''
    import numpy

    import backward

    # Gen number of timesteps from landscape array
    n_timesteps = len(numpy.unique(landscape[:,0]))

    # Get list of patch dictionaries for cacluating survival
    patches = backward.get_patches(cost, prob_pred, prob_food, state_increment,
                                   expected)
    # Initialize organisms into array
    organisms = list()
    for i in range(n_organisms):
        organisms.append(Organism(i, init_state))

    # Initialize output data array - row: t, organism_id, x, patch
    locations = numpy.zeros((n_timesteps*n_organisms, 4))

    # Run simulation, with no `0` timestep
    #TODO change things to be pythonic in indexing
    for t in range(1, n_timesteps+1):
        for i in range(len(organisms)):
            organisms[i] = traverse_landscape(t, organisms[i], x_crit, x_max,
                                              patches, landscape)
            locations = log_organism(t, n_organisms, organisms[i], locations)

    return locations


class Organism(object):
    '''Organisms class for optimization patch selection model'''
    def __init__(self, i, init_state):
        self.id = i
        self.alive = True
        self.patch = None
        self.state = init_state


def traverse_landscape(t, o, x_crit, x_max, patches, landscape):
    '''Choose patch then process growth and mortality'''
    import numpy

    # Get index for row corresponding to timestep and state
    idx = (landscape[:,0] == t) & (landscape[:,1] == o.state)

    # Move organism to optimal patch (i.e. D[x])
    print(t, o.state, o.patch)
    o.patch = int(landscape[idx][0][4])-1

    # Reduce energey based on patch cost
    o.state -= patches[o.patch]['cost']

    # Find food based on patch probability of finding food
    prob_food = patches[o.patch]['prob_food']
    food_found = numpy.random.choice([1,0], 1, p=[prob_food, 1-prob_food])

    # Increase state by 'state_increment' amount for patch
    # only allow state to be increased to maximum
    increment = patches[o.patch]['state_increment']
    if food_found & (o.state+increment <= x_max):
        o.state += increment
    else:
        o.state = float(x_max)

    # Kill organism if critical state reached
    if o.state <= x_crit:
        o.alive = False

    # Kill organism based on patch probability of predation
    prob_pred = patches[o.patch]['prob_pred']
    o.alive = numpy.random.choice([1,0], 1, p=[1-prob_pred, prob_pred])

    return o


def log_organism(t, n_organisms, o, locations):
    '''Save fitness values to array for archiving

    Row index positions
    -------------------
    0: t
    1: organism_id
    2: x
    3: patch
    '''

    # Increment y index by t*n_organisms + organism id for each timestep
    y_idx = ((t-1)*n_organisms)+o.id

    # Fill row with t, organism id, current state, and current patch
    locations[y_idx, 0] = t
    locations[y_idx, 1] = o.id
    locations[y_idx, 2] = o.state
    locations[y_idx, 3] = o.patch

    return locations


if __name__ == '__main__':

    import numpy

    import backward

    # Backward - state parameters
    n_timesteps = 20 # T / "Horizon" / max. time-step
    x_crit = 3 # critical state value, forager dies
    x_max = 10 # max state value, at energy capacity

    # Backward - patch parameters
    cost = [1, 1, 1] # alpha
    prob_pred = [0.000, 0.004, 0.020] # beta
    prob_food = [0.0, 0.4, 0.6] # lambda
    state_increment = [0, 3, 5] # epsilon
    expected = [0.0, 1.2, 3.3]

    # Forward - parameters
    n_organisms = 50
    init_state = 6.0

    try:
        landscape = numpy.load('landscape.npy')
    except:
        landscape = backward.simulation(n_timesteps, x_crit, x_max, cost,
                                        prob_pred, prob_food, state_increment,
                                        expected, display=True, log=True)

    locations = simulation(n_organisms, init_state, x_crit, x_max, landscape)

    # TODO visualize, bokeh?
