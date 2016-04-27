def simulate(n_timesteps, n_organisms, init_state, landscape):
    '''Forward simulate individuals over patch-selection fitness landscape'''
    import numpy

    # Initialize organisms into array
    organisms = list()
    for i in range(n_organisms):
        organisms.append(Organism(i, init_state))

    # Initialize output data array
    location = numpy.zeros((n_timesteps, n_organisms))

    # Run simulation
    for t in range(n_timesteps):
        for o in organisms:
            traverse_landscape(t, o, landscape)

    return locations


class Organism(object):
    '''Organisms class for optimization patch selection model'''
    def __init__(self, i, init_state):
        self.id = i
        self.alive = True
        self.patch = None
        self.state = init_state


def traverse_landscape(t, o, landscape):
    #TODO temp code finish
    if o.state > landscape:
        o.patch = 3

    return None


if __name__ == '__main__':

    #TODO
    # read landscape file from patch.py

    n_timesteps = 100 #TODO same as landscape?
    n_organisms = 50
    init_state = 6
    landscape = numpy.load('fitness')

    locations = simulate(n_organisms, init_state, landscape)

    # TODO visualize, bokeh?
