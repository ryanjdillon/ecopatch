def run_simulation():
    '''Loop through timesteps and individuals

    This code is written following the algorithm pseudo-code presented in Mark Mangel and
    Colin Whitcomb's book 'Dynamic Modeling in Behavioral Ecology', 1998,
    Chapter 2.
    '''

    # State parameters
    state = dict()
    n_timesteps = 20 # T / "Horizon" / max. time-step
    x_crit = 3 # critical state value, forager dies
    x_max = 10 # max state value, at energy capacity
    mod = 1 # param. for gradual F(x,T,T) #TODO not used

    # Patch parameters
    cost = [1, 1, 1] # alpha
    prob_pred = [0.000, 0.004, 0.020] # beta
    prob_food = [0.0, 0.4, 0.6] # lambda
    state_increment = [0, 3, 5] # epsilon
    expected = [0.0, 1.2, 3.3]

    # Create patch array
    print('\nCreate patches...')
    patches = list()
    for (A, B, L, Y, E) in zip(cost, prob_pred, prob_food, state_increment, expected):
        patches.append(new_patch(A, B, L, Y, E))

    # STEP 1 - initialize fitness arrays
    print('\nInitialize vectors...')
    F0, F1, D = init_f(x_crit, x_max)
    print_vals(x_crit, x_max, F0, F1, D)

    # STEP 2 - Iterate over timesteps, getting max fitness values
    t = n_timesteps
    while t > 0:
        print('\ntime '+str(t)+'\n')
        t, F0, F1, D = process_timestep(t, x_crit, x_max, patches, F0, F1, D)

    return F0, F1


def process_timestep(t, x_crit, x_max, patches, F0, F1, D):
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

    # STEP 3 - Print fitness value and optimal index with t
    print_vals(x_crit, x_max, F0, F1, D)

    # STEP 4 - cope F0 to F1, updates fitness function to F(x,t,T)
    for x in range(0, x_max+1, 1):
        F1[x] = F0[x]

    # STEP 5 - reduce timestep
    t -= 1

    return t, F0, F1, D


def init_f(x_crit, x_max):
    '''Initialize fitness arrays (F0 & F1) and optimal patch index array (D)'''
    import numpy

    #TODO could improve with numpy filtering

    F0 = numpy.zeros((x_max+1)) # F(x,t,T) ; basic units of x
    F1 = numpy.zeros((x_max+1)) # F(x,t+1,T) ; basic units of x
    D  = numpy.zeros((x_max+1)) # optimal patch index

    # Set values of x over critical value to 1 (alive)
    for x in range(x_crit, x_max+1, 1):
        if x > x_crit:
            F1[x] = 1

    return F0, F1, D


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


def new_patch(cost, prob_pred, prob_food, state_increment, expected):
    '''Create new patch dictionary'''

    patch = dict()
    patch['cost'] = cost
    patch['prob_pred'] = prob_pred
    patch['prob_food'] = prob_food
    patch['state_increment'] = state_increment
    patch['expected'] = expected

    return patch


def print_vals(x_crit, x_max, F0, F1, D):
    '''Show values for x, F0, F1, D'''

    print('%3s %6s %6s %6s' % ('x', 'F0', 'F1', 'D'))
    for x in range(x_crit+1, x_max+1, 1):
        print('%3.0f, %6.3f, %6.3f, %6.3f' % (x, F0[x], F1[x], D[x]))


if __name__ == '__main__':
    F0, F1 = run_simulation()
