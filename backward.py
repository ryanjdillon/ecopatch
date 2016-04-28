def simulation(n_timesteps, x_crit, x_max, cost, prob_pred, prob_food,
        state_increment, expected, display=True, log=True):
    '''Loop through timesteps and individuals

    This code is written following the algorithm pseudo-code presented in Mark Mangel and
    Colin Whitcomb's book 'Dynamic Modeling in Behavioral Ecology', 1998,
    Chapter 2.

    Variations in state are in whole increments of 1. This could be configured
    to be more general.
    '''
    import numpy

    # Create patch array
    print('\nCreate patches...')
    get_patches(cost, prob_pred, prob_food, state_increment, expected)

    # STEP 1 - initialize fitness arrays
    print('\nInitialize vectors...')
    F0, F1, D = init_f(x_crit, x_max)

    # Print and/or log fitness values
    if display:
        print_vals('0', x_crit, x_max, F0, F1, D)
    if log:
        # one row for each x in timestep - t, x, F0, F1, D
        landscape = numpy.zeros((n_timesteps*(x_max), 5))
        log_vals(0, x_crit, x_max, F0, F1, D, landscape)

    # STEP 2 - Iterate over timesteps, getting max fitness values
    t = n_timesteps
    while t > 0:
        F0, D = max_v(x_crit, x_max, patches, F0, F1, D)

        # STEP 3 - Print/log fitness value and optimal index with t
        if display:
            print_vals(t, x_crit, x_max, F0, F1, D)
        if log:
            landscape = log_vals(t, x_crit, x_max, F0, F1, D, landscape)

        # STEP 4 - Copy F0 to F1, updates fitness function to F(x,t,T)
        for x in range(0, x_max+1, 1):
            F1[x] = F0[x]

        # STEP 5 - Reduce timestep
        t -= 1

    # Save landscape array to binary numpy file for retrieval
    if log:
        numpy.save("landscape.npy", landscape)

    return landscape


def init_f(x_crit, x_max):
    '''Initialize fitness arrays (F0 & F1) and optimal patch index array (D)'''
    import numpy

    F0 = numpy.zeros((x_max+1)) # F(x,t,T) ; basic units of x
    F1 = numpy.zeros((x_max+1)) # F(x,t+1,T) ; basic units of x
    D  = numpy.zeros((x_max+1)) # optimal patch index

    # Set values of x over critical value to 1 (alive)
    for x in range(x_crit, x_max+1, 1):
        if x > x_crit:
            F1[x] = 1

    return F0, F1, D


def max_v(x_crit, x_max, patches, F0, F1, D):
    '''Iterate over one timestep'''

    # Calculate probability of survival for each energy reserve and patch
    for x in range(x_crit+1, x_max+1, 1):
        vm = 0 # max energetic state per patch
        for i in range(len(patches)):
            A = patches[i]['cost']
            B = patches[i]['prob_pred']
            L = patches[i]['prob_food']
            Y = patches[i]['state_increment']

            v = compute_v(x, A, B, L, Y, x_crit, x_max, F1)

            # Save maximum fitness, and index location
            if v > vm:
                vm = v
                F0[x] = v
                D[x]  = i+1 # correct index to appear same as book

    return F0, D


def compute_v(x, A, B, L, Y, x_crit, x_max, F1):
    '''Compute fitness (prob. of survival) for a given state (energy reserve)

    Greater energy reserves result in increased fitness.

    v: probability of survival
    (1-B): probability surviving predation
    L:     probability of finding food
    (1-L): probabililty of not finding food
    x prime = chop(x-A+Yi, x_crit, x_max)
    x double prime = chop(x-A, x_crit, x_max)
    '''

    v = (1-B)*(L*F1[chop(x-A+Y, x_crit, x_max)] + \
               (1-L)*F1[chop(x-A, x_crit, x_max)])
    return v


def chop(x, x_crit, x_max):
    '''Update living boolean based on critical energy and max capacity'''

    # Critical energy, die if fall below
    if (x < x_crit):
        x_out = 0
    # Max capacity, x not allowed to be greater than this
    if x > x_max:
        x_out = x_max
    # Between the two
    elif (x >= x_crit) & (x <= x_max):
        x_out = x

    return x_out


def get_patches(cost, prob_pred, prob_food, state_increment, expected):
    '''Create a list of patch dictionaries'''

    patches = list()
    for (A, B, L, Y, E) in zip(cost, prob_pred, prob_food, state_increment, expected):
        patch = {'cost':A,
                 'prob_pred':B,
                 'prob_food':L,
                 'state_increment':Y,
                 'expected':E
                 }
        patches.append(patch)

    return patches


def log_vals(t, x_crit, x_max, F0, F1, D, landscape):
    '''Save fitness values to array for archiving'''

    for x in range(0, x_max, 1):
        # Increment y index by t*n_x for each timestep
        y_idx = ((t-1)*(x_max))+x
        # Fill row for t, x pair with fitness values and optimal patch index
        landscape[y_idx, 0] = t
        landscape[y_idx, 1] = x
        landscape[y_idx, 2] = F0[x]
        landscape[y_idx, 3] = F1[x]
        landscape[y_idx, 4] = D[x]

    return landscape


def print_vals(t, x_crit, x_max, F0, F1, D):
    '''Show values for x, F0, F1, D'''

    print('\ntime '+str(t)+'\n')
    for x in range(x_crit+1, x_max+1, 1):
        print('%3.0f, %6.3f, %6.3f, %6.3f' % (x, F0[x], F1[x], D[x]))


if __name__ == '__main__':

    # State parameters
    n_timesteps = 20 # T / "Horizon" / max. time-step
    x_crit = 3 # critical state value, forager dies
    x_max = 10 # max state value, at energy capacity

    # Patch parameters
    cost = [1, 1, 1] # alpha
    prob_pred = [0.000, 0.004, 0.020] # beta
    prob_food = [0.0, 0.4, 0.6] # lambda
    state_increment = [0, 3, 5] # epsilon
    expected = [0.0, 1.2, 3.3]

    landscape = simulation(n_timesteps, x_crit, x_max, cost, prob_pred,
                           prob_food, state_increment, expected,
                           display=True, log=True)
