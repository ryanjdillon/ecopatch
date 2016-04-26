def run_simulation(n_timesteps, n_organisms, x_crit, x_max, ):
    '''Loop throu timesteps and individuals'''

    # State parameters
    state = dict()
    state['n_timesteps'] = 20 # T / "Horizon" / max. time-step
    state['x_crit'] = 3 # critical state value, forager dies
    state['x_max'] = 10 # max state value, at energy capacity
    state['mod'] = 1 # param. for gradual F(x,T,T) ??

    # TODO describe
    energy_reserves = range(0, x_max+1, mod) # value 1-10
    init_reserve = 6

    # Patch parameters
    cost = [1, 1, 1] # alpha
    prob_pred = [0.000, 0.004, 0.020] # beta
    prob_food = [0.0, 0.4, 0.6] # lambda
    state_increment = [0, 3, 5] # epsilon
    expected = [0.0, 1.2, 3.3]

    # Create patch array
    patches = list()
    for (A, B, L, Y, E) in zip(cost, prob_pred, prob_food, state_increment, expected):
        patches.append(new_patch(A, B, L, Y, EA))

    # Init organisms
    organisms = list()
    for _ in range(n_organisms):
        organisms.append({'alive': 1,
                          'reserve': init_reserve,
                          'food':,
                          'new_state':,})

    # STEP 1. - initialize f vectors
    F0 = dict() # F(x,t,T) - i.e. terminal F
    F1 = dict() # F(x,t+1,T) - i.e. dynamic F

    D = dict() # optimal patch index

    for x in range(x_crit, x_max, 1):
        F0[x] = chop(x, x_crit, x_max)
        #TODO F1?

    while t > 0:
        # STEP 2. - Heart of algorithm
        for x in range(x_crit+1, x_max, 1):
            vm = 0
            for p in range(n_patches):
                A = patches[p]['cost']
                B = patches[p]['prob_pred']
                L = patches[p]['prob_food']
                Y = patches[p]['state_increment']
                v = compute_state(x, A, B, L, Y, x_crit, x_max, F1):
                # Get maximum VM
                if v > vm:
                    vm = v
                    D[x] = p

        F0[x_crit] = 0

        #STEP 3. - print value of t and values of D(x)
        for x in range(x_crit+1, C, 1):
            print('D['+x+']: ', D[x])
            print('F0['+x+']: ', D[x])

        # STEP 4.
        for x in range(0, x_max, 1):
            F1[x] = F0[x]

        # STEP 5.
        t -= 1

    return None


def new_patch(cost, prob_pred, prob_food, state_increment, expected):
    '''Create new patch dictionary'''

    patch = dict()
    patch['cost'] = cost
    patch['prob_pred'] = prob_pred
    patch['prob_food'] = prob_food
    patch['state_increment'] = state_increment
    patch['expected'] = expected

    return patch


def compute_v(x, A, B, L, Y, x_crit, x_max, F1):
    '''compute V_i

    Chapter 2 algorithm, step2
    x prime = chop(x-A+Yi, x_crit, x_max)
    x double prime = chop(x-A, x_crit, x_max)
    '''


    v_patch = (1-B)*(L*f1[chop(x-A+Y, x_crit, x_max)] + \
                     (1-L)*F1[chop(x-A, x_crit, x_max)])

    return v_patch


def select_patch(n_patches, patch_params):

    for i in range(n_patches):
        if x > x_crit:
            f0.append(1)
            f1.append(0)
        elif x <= x_crit:
            f0.append(0)
            f1.append(1)


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


