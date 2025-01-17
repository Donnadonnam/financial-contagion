import numpy as np

def generate_uniform_iid_shocks(C):
    X = np.zeros_like(C)
    for i in range(len(X)):
        X[i] = np.random.randint(low=0, high=int(C[i]))

    return X

def generate_beta_iid_shocks(C):
    X = np.zeros_like(C)
    for i in range(len(X)):
        # X[i] = C[i] * np.random.beta(a=1/2, b=1/2)
        X[i] = C[i] * np.random.beta(a=1, b=1)

    return X

def generate_point_iid_shocks(C):
    X = np.zeros_like(C)
    for i in range(len(C) // 2):
        X[i, 0] = C[i, 0]


    # X[-1, 0] = C[-1, 0]
    # X[-2, 0] = C[-2, 0]
    return X
