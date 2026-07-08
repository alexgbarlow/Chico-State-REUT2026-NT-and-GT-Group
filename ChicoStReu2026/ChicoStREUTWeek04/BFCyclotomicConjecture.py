from sage.all import *
from itertools import product as prdt
import pickle

def voltage_cover(X, G, alpha):
    X_edges = list(X.edges())
    X_verts = list(X.vertices())
    # X_as_dict = X.to_dictionary(multiple_edges=True)
    Y = DiGraph(loops=True, multiedges=True)
    Y_verts = list(prdt(X_verts, G.list()))
    X_cross_G = list(prdt(X_edges, G.list()))
    # print(f"X_cross_G size == {len(X_cross_G)}")
    # print(f"Y_verts == {len(Y_verts)}")
    Y_edges = []
    for (e, g) in X_cross_G:
        # print("Heres e:", e)
        u, v, label = e
        tail = (u, g)
        head = (v, g+alpha(e))
        # print(f"{g}+alpha({e}) == {g+alpha(e)}")
        # print(f"g == {g}, alpha(e) == {alpha(e)}, g+alpha(e) == {g+alpha(e)}")
        Y_edges.append((tail, head, label))
    # for (e, g) in Y_cross_G:
    #     # 
    #     Y_edges.append(((e,g),(e, g+alpha(e)), None))
    
    Y.add_vertices(Y_verts)
    Y.add_edges(Y_edges)
    # print(f"# of edges X == {len(X.edges())}")
    # print(f"# of edges of Y == {len(Y.edges())}")
    # Y.show()
    return Y

def BF_minus_class_group_conjecture(p,n):
    X = DiGraph(loops=True, multiedges=True)
    X.add_edge(0, 0, (0, 0)) 
    
    for i in range(1, p**n+1):        
        for j in range(1, i+1):
            if i % p != 0:      
                X.add_edge(0, 0, (i, j))
            # print("X edge == ", (i,j))
    # X.show()
    DELTA = AdditiveAbelianGroup([euler_phi(p**n)])
    gen = DELTA.gen(0)
    # print("gen ==", gen)
    zeta_p = primitive_root(p**n)
    def phi(i):
        if i == 0:
            return DELTA.zero()
        
        k = discrete_log(Mod(i, p**n), Mod(zeta_p, p**n))
        # print(f"When i == {i}, k == {k}")
        return k * gen
    
    def alpha(e):
        label = e[2]              
        i = label[0]
        if i == 0:
            # print(f"-phi({1}) == {phi(1)}")
            return phi(1)         
        else:
            # print(f"-phi({i}) == {-phi(i)}")
            return -phi(i)        
        
    Y = voltage_cover(X, DELTA, alpha)
    # Y.show()
    BFO = identity_matrix(Y.order()) - Y.adjacency_matrix()
    # print(Y.adjacency_matrix())
    # print
    BF_SNF, non_var, non_var1 = BFO.smith_form()
    print(BF_SNF.diagonal())
    # print(BF_SNF)
    BF_TOR_ORD = prod([entry for entry in BF_SNF.diagonal() if entry != 0])
    print(f"p == {p}, n == {n}, BF_TOR_ORD == {factor(BF_TOR_ORD)}")
    print()
    # print(f"X edge cnt = {len(X.edges())}")
    # print(f"Y edge cnt = {len(Y.edges())}")
    # h_minus = cyclotomic_minus_class_number(p,n)
    # print(f"minus class number == {1},        BF group torsion part order == {BF_TOR_ORD}, BF factorized == {factor(BF_TOR_ORD)}      quotient == {BF_TOR_ORD/43}")
    return {'p': p, 'n': n, 'BF_TOR_ORD': factor(BF_TOR_ORD)}
    # print(f"Order of the torsion part of BF group == {BF_TOR_ORD}, RHS == {LHS}")
    # print(f"(LHS == RHS) == {BF_TOR_ORD == LHS}")
three_data = []
for n in range(1, 10):
    three_data.append(BF_minus_class_group_conjecture(3,n))

with open('three_data.pkl', 'wb', 'x') as file:
    pickle.dump(three_data, file)
    
two_data = []
for n in range(1, 10):
    two_data.append(BF_minus_class_group_conjecture(2,n))

with open('~/ChicoStReu2026//two_data.pkl', 'wb', 'x') as file:
    pickle.dump(two_data, file)