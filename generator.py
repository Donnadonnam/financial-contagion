import networkx as nx
import numpy as np

def generate_random_data(seed=42, random_graph='ER', H=None, distribution='exponential', alpha=0.14,  n=30):
    if random_graph == 'ER':
        G = generate_er(n, p=0.8, seed=seed)
    elif random_graph == 'SF':
        G = generate_scale_free(n, seed=seed)
    elif random_graph == 'CP':
        G = generate_core_periphery(n, p=0.7, seed=seed)

    distributions = {
        'exponential' : lambda size: np.random.exponential(1, size=size),
        'pareto' : lambda size: np.random.pareto(1, size=size),
        'lognormal' : lambda size: np.random.lognormal(0, 1, size=size)
    }

    adj = nx.to_numpy_array(G)
    outdegree = adj.sum(0)
    indegree = adj.sum(-1)

    liabilities = adj * distributions[distribution]((n, n))

    internal_assets = liabilities.sum(-1).reshape((n, 1))
    internal_liabilities = liabilities.sum(0).reshape((n, 1))

    external_assets = np.array([G.degree(u) for u in G]) * distributions[distribution]((n, 1))
    external_liabilities = alpha * external_assets

    P_bar = internal_liabilities + external_liabilities

    A = np.copy(liabilities)
    for i in range(liabilities.shape[0]):
        A[i] /= P_bar[i]

    wealth = external_assets + internal_assets - external_liabilities - internal_liabilities

    # if np.any(wealth < 0):
        # return generate_random_data(seed=seed, random_graph=random_graph, distribution=distribution, alpha=alpha)
    # else:
    return A, P_bar, liabilities, adj, internal_assets, internal_liabilities, outdegree, indegree, external_assets, external_liabilities, wealth, G


def generate_core_periphery(n, p, p_cc = 0.8, p_cp = 0.4, p_pp = 0.1, seed=100):
    n_c = int(n ** p)
    n_p = n - n_c

    sizes = [n_c, n_p]
    p = [[p_cc, p_cp], [p_cp, p_pp]]

    return nx.generators.community.stochastic_block_model(sizes, p, seed=seed, directed=True)

def generate_scale_free(n, seed=100):
    return nx.DiGraph(nx.generators.directed.scale_free_graph(n, alpha=0.5, beta=0.25, gamma=0.25, seed=seed))

def generate_er(n, p=0.8, seed=100):
    return nx.generators.random_graphs.gnp_random_graph(n, p, seed=seed, directed=True)

def generate_sbm_pair(n, D, stochastic=False, seed=100):
    sizes = [n//2, n//2]

    if stochastic:
        p = [[1, D], [D, 1]]
        G = nx.DiGraph(nx.generators.community.stochastic_block_model(sizes, p, seed=seed, directed=False))
    else:
        p = [[1, 0], [0, 1]]
        G = nx.generators.community.stochastic_block_model(sizes, p, seed=seed, directed=False)

        for i in range(0, n // 2 - D, D):
            for j in range(D):
                for k in range(D):
                    G.add_edge(i + j, n // 2 + i + k)

        G =  nx.DiGraph(G)

    liabilities = nx.to_numpy_array(G)
    outdegree = liabilities.sum(0)
    indegree = liabilities.sum(-1)

    internal_assets = liabilities.sum(-1).reshape((n, 1))
    internal_liabilities = liabilities.sum(0).reshape((n, 1))

    external_assets =  n * np.ones((n, 1))
    external_liabilities = np.ones((n, 1))

    P_bar = internal_liabilities + external_liabilities

    A = np.copy(liabilities)
    for i in range(liabilities.shape[0]):
        A[i] /= P_bar[i]

    wealth = external_assets + internal_assets - external_liabilities - internal_liabilities

    return A, P_bar, liabilities, internal_assets, internal_liabilities, outdegree, indegree, external_assets, external_liabilities, wealth, G
