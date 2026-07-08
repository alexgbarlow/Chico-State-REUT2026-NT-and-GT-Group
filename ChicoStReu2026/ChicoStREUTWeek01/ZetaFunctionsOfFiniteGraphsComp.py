from sage.all import *
from sage.all import *
from sage.all import *
#!/usr/bin/env python
# coding: utf-8

# In[1]:


from itertools import product as prdt

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
    # Y.show(layout='spring',       # or 'circular', 'spring', 'planar', 'tree'
    #     vertex_labels=True,
    #     figsize=(10, 10),       
    #     vertex_size=250,         
    #     edge_thickness=2)

# X = DiGraph({0:[1], 1:[2], 2:[0,1]})
# X.show()
# G = AdditiveAbelianGroup([3])
# # alpha= lambda e: G([e[0]])
# def alpha(e):
#     if e[0] == 0:
#         return G([1])
#     elif e[0] == 1 or e[0] == 2:
#         return G([0])
#     else:
#         return G([2])

# voltage_cover(X, G, alpha)


# In[2]:


from collections import defaultdict
import random as rm
'''
    Input: A (unoriented/undirected) graph g.
    Output: The line oriented graph induced by g.
'''
def line_orient_graph(g):
    UO_g_edges = list(g.edges())
    # print(UO_g_edges)
    UO_g_edges = [(o,t, "f", 0) for o,t,l in UO_g_edges]

    g_edges = list.copy(UO_g_edges)
    # print("BEFORE labeling: g_edges == ", g_edges)

    curr_counts = defaultdict(int) # Claude Code block
    result = []
    for (o,t,d,l) in UO_g_edges:
        n = curr_counts[(o, t, d, l)]
        result.append((o, t, d, n))
        curr_counts[(o, t, d, l)] += 1
    # print("AFTER labeling and BEFORE adding back edges: g_edges == ", g_edges)
    g_edges = result
    rev_edges = [(t, o, "b", l) for o,t,d,l in g_edges]
    g_edges += rev_edges
    # print("AFTER adding back edges: g_edges == ", g_edges)
    LO_g = dict()
    for o,t,d,l in g_edges:
        LO_g.setdefault((o, t, d, l), {})

    # print("BEFORE FILLING: LO_g == ", LO_g)
    cnt = 0
    for (o1,t1,d1,l1), adj_es in LO_g.items():
        for o2,t2,d2,l2 in g_edges:
            if t1 != o2 or (o2 == t1 and t2 == o1 and l2 == l1 and d1 != d2): 
                continue
            else:
                # print(f"l1 == {l1} and l2 == {l2}")
                adj_es.setdefault((o2, t2, d2, l2),f"{cnt}")
                cnt = cnt + 1

    # print("AFTER FILLING: LO_g == ", LO_g)
    return DiGraph(LO_g, loops = True)

# # G = Graph({0: [1,2], 1: [0,2], 2: [0,1]})
# # g1 = Graph({0: [0,0]}) # 2 line Boquet
# # g2 = Graph({0: [0,0,0]}) # 3 line Boquet
# # g3 = Graph({0: [1,1,1,1,1]}) # 5 line 2 vertex graph 
# # # g4 = Graph({0:[0,1], 1:[0,0]}) # Bowtie with 1 loop 
# # # print("g1 type: ", type(g1))
# # G.show()
# # g1.show()
# # g2.show()
# # g3.show()
# # # g4.show()
# # line_orient_graph(G).show()
# # line_orient_graph(g1).show()
# # line_orient_graph(g2).show()
# # line_orient_graph(g3).show()
# # # line_orient_graph(g4).show()

# # print((identity_matrix(4)-line_orient_graph(g1).adjacency_matrix()).smith_form(transformation=False))
# # print((identity_matrix(6)-line_orient_graph(g2).adjacency_matrix()).smith_form(transformation=False))
# # print((identity_matrix(10)-line_orient_graph(g3).adjacency_matrix()).smith_form(transformation=False))
# # # print((identity_matrix(10)-line_orient_graph(g4).adjacency_matrix()).smith_form(transformation=False))
# g1=Graph({0:[1], 1:[0,2], 2:[1,3], 3:[2,4], 4:[3]})
# g2=Graph({0:[1,2,3], 1:[0,2], 2:[0,1], 3:[0]})
# g3=Graph({0:[1,3], 1:[0,2], 2:[1,3], 3:[2,0,4], 4:[3]})
# g4=Graph({0: [1, 2], 1: [0, 2], 2: [0, 1, 3]})
# g5 = Graph({0:[1,2], 1:[0,2], 2:[0,1,3], 3:[2]})
# # V=4, E=4, χ=0

# g6 = Graph({0:[1,2], 1:[0,2], 2:[0,1,3], 3:[2,4], 4:[3]})
# # V=5, E=5, χ=0

# g7 = Graph({0:[1,2], 1:[0,2], 2:[0,1,3,4], 3:[2], 4:[2]})
# # V=5, E=5, χ=0

# g8 = Graph({0:[1,3], 1:[0,2], 2:[1,3,4], 3:[0,2], 4:[2]})
# # V=5, E=5, χ=0

# g9 = Graph({0:[1,2], 1:[0,2], 2:[0,1,3], 3:[2,4,5], 4:[3], 5:[3]})
# # V=6, E=7, χ=-1

# g10 = Graph({0:[1,2], 1:[0,2], 2:[0,1]})
# # Triangle: V=3, E=3, χ=0

# g11 = Graph({0:[1,3], 1:[0,2], 2:[1,3], 3:[0,2]})
# # 4-cycle: V=4, E=4, χ=0

# g12 = Graph({0:[1,4], 1:[0,2], 2:[1,3], 3:[2,4], 4:[0,3]})
# # 5-cycle: V=5, E=5, χ=0

# g13 = Graph({
#     0:[1,3,2],
#     1:[0,2],
#     2:[1,3,0],
#     3:[0,2]
# })
# # Square with diagonal: V=4, E=5, χ=-1

# g14 = Graph({
#     0:[1,5],
#     1:[0,2,4],
#     2:[1,3],
#     3:[2,4],
#     4:[3,5,1],
#     5:[4,0]
# })

# # Hexagon with chord: V=6, E=7, χ=-1
# # g1.show()
# # g2.show()
# # g3.show()

# g15 = Graph({
#     0:[1,2,3],
#     1:[0,2,3],
#     2:[0,1,3],
#     3:[0,1,2, 4],
#     4: [3]
# })
# G1=line_orient_graph(g1)
# G2=line_orient_graph(g2)
# G3=line_orient_graph(g3)
# G4=line_orient_graph(g4)
# G15=line_orient_graph(g15)
# ec1 = g1.order()-len(list(g1.edges()))
# ec2 = g2.order()-len(list(g2.edges()))
# ec3 = g3.order()-len(list(g3.edges()))
# ec4 = g4.order()-len(list(g4.edges()))
# ec15 = g15.order()-len(list(g15.edges()))
# EC1 = G1.order()-len(list(G1.edges()))
# EC2 = G2.order()-len(list(G2.edges()))
# EC3 = G3.order()-len(list(G3.edges()))
# EC4 = G4.order()-len(list(G4.edges()))
# # G1.show()
# # g2.show()
# # G2.show()
# # # G3.show()
# # g15.show()
# # G15.show()
# # print(f"ec1 == {ec1}        ec2 == {ec2}        ec3 == {ec3}        ec15 == {ec15}")
# # print(f"EC1 == {EC1}        EC2 == {EC2}        EC3 == {EC3}")
# def add_one_deg1_vert(g: Graph):
#     h = g.copy()
#     connection_vert = rm.randint(0, h.order()-1)
#     new_vert = h.order()
#     h.add_vertex(new_vert)
#     h.add_edge(connection_vert, new_vert)
#     return h


# def add_random_deg1_chain_verts(g: Graph):
#     h = g.copy()
#     connection_vert = rm.randint(0, h.order()-1)
#     num_new_verts = rm.randint(0,10)
#     for cnt in range(h.order(), h.order()+num_new_verts+1):
#         h.add_vertex(cnt)
#         h.add_edge(connection_vert, cnt)
#     return h

# def identity_checker(g: Graph):
#     G=line_orient_graph(g)
#     ec = g.order()-len(list(g.edges()))
#     EC = G.order()-len(list(G.edges()))
#     R.<u> = PolynomialRing(ZZ) 
#     a = g.adjacency_matrix()
#     L = G.adjacency_matrix()
#     deg_list = [g.degree(v) for v in g.vertices()]
#     d = diagonal_matrix(deg_list)
#     LHS = det(identity_matrix(ZZ,G.order()) - L*u) 
#     RHS = (1-u^2)**((-1)*ec)*det(identity_matrix(ZZ,g.order())-a*u+(d-identity_matrix(ZZ,g.order()))*u**2)

#     if ec == 0:
#         zero_set = [d for d in SNF_comp_for_PFO(g).diagonal() if d == 0]
#         print(f" The number of 0\'s on the diagonal of the PF operator's SNF  == {len(zero_set)}")

#     # print(f" LHS {det(identity_matrix(ZZ,G.order()) - L*u)} RHS {(1-u^2)**((-1)*ec)*det(identity_matrix(ZZ,g.order())-a*u+(d-identity_matrix(ZZ,g.order()))*u**2)}")
#     print("(LHS == RHS) == ", LHS == RHS)

# def deg1_edge_removal(g: Graph):
#     edges_to_remove = []
#     for u, v, label in g.edge_iterator():
#         if g.degree(u) == 1 or g.degree(v) == 1:
#             edges_to_remove.append((u, v))
#     g.delete_edges(edges_to_remove)
#     return g

# def compare_LHS_RHS(g1, g2):
#     G1=line_orient_graph(g1)
#     ec1 = g1.order()-len(list(g1.edges()))
#     R.<u> = PolynomialRing(ZZ) 
#     a1 = g1.adjacency_matrix()
#     L1 = G1.adjacency_matrix()
#     deg_list1 = [g1.degree(v) for v in g1.vertices()]
#     d1 = diagonal_matrix(deg_list1)
#     LHS1 = det(identity_matrix(ZZ,G1.order()) - L1*u)
#     RHS1 = (1-u^2)**((-1)*ec1)*det(identity_matrix(ZZ,g1.order())-a1*u+(d1-identity_matrix(ZZ,g1.order()))*u**2)

#     G2=line_orient_graph(g2)
#     ec2 = g2.order()-len(list(g2.edges()))
#     R.<u> = PolynomialRing(ZZ) 
#     a2 = g2.adjacency_matrix()
#     L2 = G2.adjacency_matrix()
#     deg_list2 = [g2.degree(v) for v in g2.vertices()]
#     d2 = diagonal_matrix(deg_list2)
#     RHS2 = (1-u^2)**((-1)*ec2)*det(identity_matrix(ZZ,g2.order())-a2*u+(d2-identity_matrix(ZZ,g2.order()))*u**2)
#     LHS2 = det(identity_matrix(ZZ,G2.order()) - L2*u)

#     print(f"LHS before and after adding deg1 vertices is unchanged == {LHS1 == LHS2}")
#     if LHS1 != LHS2:
#         return g1, g2
#     print(f"RHS before and after adding deg1 vertices is unchanged == {RHS1 == RHS2}")
#     if RHS1 != RHS2:
#         return g1,g2
#     print(f"All sides are equal == {LHS1 == RHS2}")




# def SNF_comp_for_PFO(g: Graph):
#     G = line_orient_graph(g)
#     L = G.adjacency_matrix()
#     SNF_PFO = (identity_matrix(ZZ, G.order()) - L).smith_form(transformation=False)
#     # print("SNF of the Perron-Frob Operator == ")
#     # print(SNF_PFO)
#     return SNF_PFO

# def SNF_deg1_comp(g_before: Graph):
#     R.<u> = PolynomialRing(ZZ) 
#     G_before = line_orient_graph(g_before)
#     L_before = G_before.adjacency_matrix()
#     SNF_BEFORE = SNF_comp_for_PFO(g_before)
#     ec_before  = g_before.order() - len(g_before.edges())
    
#     a_before = g_before.adjacency_matrix()
#     L_before = G_before.adjacency_matrix()
#     deg_list_before = [g_before.degree(v) for v in g_before.vertices()]
#     d_before = diagonal_matrix(deg_list_before)
#     LHS_BEFORE = det(identity_matrix(ZZ,G_before.order()) - L_before*u) 
#     RHS_BEFORE = (1-u^2)**((-1)*ec_before)*det(identity_matrix(ZZ,g_before.order())-a_before*u+(d_before-identity_matrix(ZZ,g_before.order()))*u**2)

#     g_after = deg1_edge_removal(g_before)
#     G_after = line_orient_graph(g_after)
#     L_after = G_after.adjacency_matrix()
#     SNF_AFTER = SNF_comp_for_PFO(g_after)
#     ec_after = g_after.order() - len(g_after.edges())
    
#     a_after = g_after.adjacency_matrix()
#     L_after = G_after.adjacency_matrix()
#     deg_list_after = [g_after.degree(v) for v in g_after.vertices()]
#     d_after = diagonal_matrix(deg_list_after)
#     LHS_AFTER = det(identity_matrix(ZZ,G_after.order()) - L_after*u) 
#     RHS_AFTER = (1-u^2)**((-1)*ec_after)*det(identity_matrix(ZZ,g_after.order())-a_after*u+(d_after-identity_matrix(ZZ,g_after.order()))*u**2)


#     SNFB_torpart = [d for d in SNF_BEFORE.diagonal() if d != 0]
#     SNFA_torpart = [d for d in SNF_AFTER.diagonal() if d != 0]
#     SNFB_prod = prod(SNFB_torpart)
#     SNFA_prod = prod(SNFA_torpart)
#     SNFB_1part = [d for d in SNF_BEFORE.diagonal() if d ==1]
#     SNFA_1part = [d for d in SNF_BEFORE.diagonal() if d ==1]
#     print(f"(LHS_BEFORE == LHS_AFTER) == {LHS_BEFORE == LHS_AFTER}")
#     print(f"(RHS_BEFORE == RHS_AFTER) == {RHS_BEFORE == RHS_AFTER}")
#     print(f" All four polynomials are equal  == {LHS_BEFORE == RHS_AFTER}")
#     print("The torsion part of the trimmed graph has order equal to the orignal == ", SNFB_prod == SNFA_prod)
#     print("The number of 1\'s along the diagonal are equal == ", len(SNFB_1part) == len(SNFA_1part))
#     print(f"SNFB_prod == {SNFB_prod}        SNFA_prod == {SNFA_prod}")
# # identity_checker(g1)
# # SNF_deg1_comp(g1)

# # identity_checker(g2)
# # deg1_edge_removal(g2).show()
# # SNF_deg1_comp(g2)

# # identity_checker(g3)
# # SNF_deg1_comp(g3)

# # identity_checker(g4)
# # SNF_deg1_comp(g4)

# # identity_checker(g5)
# # SNF_deg1_comp(g5)

# # identity_checker(g6)
# # SNF_deg1_comp(g6)

# # identity_checker(g7)
# # SNF_deg1_comp(g7)

# # identity_checker(g8)
# # SNF_deg1_comp(g8)

# # identity_checker(g9)
# # SNF_deg1_comp(g9)

# # identity_checker(g10)
# # SNF_deg1_comp(g10)

# # identity_checker(g11)
# # SNF_deg1_comp(g11)

# # identity_checker(g12)
# # SNF_deg1_comp(g12)

# # identity_checker(g13)
# # SNF_deg1_comp(g13)

# # identity_checker(g14)
# # SNF_deg1_comp(g14)

# # identity_checker(g15)
# # deg1_edge_removal(g15)
# # SNF_deg1_comp(g15)



# graph_list = []
# for cnt in range(0,1000):
#     num_v = rm.randint(5, 10)            
#     e_prob= 0.4            
#     g = Graph(num_v, multiedges=True)
    
#     extra_e = rm.randint(1,5)
#     for u in range(num_v):
#         for v in range(u, num_v+extra_e):
#             if u == v:
#                 # if rm.random() <= 0.25:
#                 #     g.add_edge(u,v)
#                 continue
#             elif rm.random() < e_prob:
#                 g.add_edge(u, v)
#     if g.is_connected() == True and g.order()-len(g.edges()) == 0:
#         graph_list.append(g)




# # """ THIS IS FOR GRAPHS WHERE EC==0"""
# # for cnt in range(0,10000):
# #     num_v = rm.randint(5, 10)            
# #     e_prob= 0.4            
# #     g = Graph(num_v, multiedges=True)
    
# #     extra_e = rm.randint(1,5)
# #     for u in range(num_v):
# #         for v in range(u, num_v+extra_e):
# #             if u == v:
# #                 # if rm.random() <= 0.25:
# #                 #     g.add_edge(u,v)
# #                 continue
# #             elif rm.random() < e_prob:
# #                 g.add_edge(u, v)
# #     if g.is_connected() == True and (g.order()-len(g.edges())) == 0:
# #         graph_list.append(g)




# graph_list = graph_list[:10]
# for g in graph_list:
#     h = add_random_deg1_chain_verts(g)
#     h = add_one_deg1_vert(g)
#     s = add_one_deg1_vert(g)
#     g.show()
#     h.show()
#     s.show()
#     identity_checker(g)
#     # SNF_comp_for_PFO(g)
#     # deg1_edge_removal(g)
#     SNF_deg1_comp(g)
#     print("MULTIPLE NEW EDGES")
#     compare_LHS_RHS(g, h)
#     print("ONE NEW EDGE")
#     compare_LHS_RHS(g, s)
#     print()

# In[3]:


# def cyclotomic_minus_class_number(p,n):
#     DC_G = DirichletGroup(p^n)
#     odd_DCharacters = [chi for chi in DC_G.list() if chi(p^n-1) == -1]
#     B_prod = prod([(-1/2)*chi.bernoulli(1) for chi in odd_DCharacters])
#     return 2*p^n*B_prod

# In[4]:


def pickle_minus_class_numbers():
    first_20_primes = [nextprime(n) for n in range(0, 72)]
    print(len(first_20_primes))

# In[5]:


import pickle
def BF_minus_class_group_conjecture(p,n):
    X = DiGraph(loops=True, multiedges=True)
    X.add_edge(0, 0, (0, 0)) 
    
    for i in range(1, p^n+1):        
        for j in range(1, i+1):
            if i % p != 0:      
                X.add_edge(0, 0, (i, j))
            # print("X edge == ", (i,j))
    # X.show()
    DELTA = AdditiveAbelianGroup([euler_phi(p^n)])
    gen = DELTA.gen(0)
    # print("gen ==", gen)
    zeta_p = primitive_root(p^n)
    def phi(i):
        if i == 0:
            return DELTA.zero()
        
        k = discrete_log(Mod(i, p^n), Mod(zeta_p, p^n))
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
    print(f"p == {p}, n == {n}, BF_TOR_ORD == {BF_TOR_ORD}")
    print()
    # K = CyclotomicField(p**n) 

    # z = K.gen()
    # g = z + z**-1
    # F = NumberField(g.minpoly(), 'a')
    # h_K = K.class_group().order()
    # h_F = F.class_group().order()
    # h_minus = h_K / h_F
    # print(f"X edge cnt = {len(X.edges())}")
    # print(f"Y edge cnt = {len(Y.edges())}")
    # h_minus = cyclotomic_minus_class_number(p,n)
    # print(f"minus class number == {1},        BF group torsion part order == {BF_TOR_ORD}, BF factorized == {factor(BF_TOR_ORD)}      quotient == {BF_TOR_ORD/43}")
    return {'p': p, 'n': n, 'BF_TOR_ORD': BF_TOR_ORD}
    # print(f"Order of the torsion part of BF group == {BF_TOR_ORD}, RHS == {LHS}")
    # print(f"(LHS == RHS) == {BF_TOR_ORD == LHS}")
    #-------------------------
    # def alpha(e):
    #     i = e[2][0]  
    #     print("i == ", i)             
    #     if i == 0:
    #         print("alpha(e_0) == ", DELTA([0]))
    #         return DELTA([0])      
    #     else:
    #         print("alpha(i) == ", (-1)*i * gen )
    #         return (-1)*i * gen 
three_data = []
for n in range(1, 10):
    three_data.append(BF_minus_class_group_conjecture(3,n))

with open('three_data.pkl', 'wb') as file:
    pickle.dump(three_data, file)
    
two_data = []
for n in range(1, 10):
    two_data.append(BF_minus_class_group_conjecture(2,n))

with open('two_data.pkl', 'wb') as file:
    pickle.dump(two_data, file)

# In[ ]:


def get_Sebastians_mults(g):
    num_spanning_trees = g.spanning_trees_count()
    G = line_orient_graph(g)
    EC = g.order()-len(list(g.edges()))
    BFO_geo_mult, BFO_alg_mult = get_BFO_mult(G, 2)
    ADJO_geo_mult, ADJO_alg_mult = get_ADJO_mult(G, -1)
    print(f"BFO GEO eigv == 2: {BFO_geo_mult}, BFO ALG eigv == 2: {BFO_alg_mult}      ADJO_geo_mult == -1: {ADJO_geo_mult}, ADJO ALG mult == -1: {ADJO_alg_mult}        Spanning Tree Count of OG graph == {num_spanning_trees}, EC == {EC}")

def get_BFO_mult(g, eigv):
    vertices = list(g.vertices())
    num_v = len(vertices)
    v_idx = {v: i for i, v in enumerate(vertices)}

    G = AdditiveAbelianGroup([0] * num_v)
    gens = G.gens()

    ADJ_O_M = matrix(ZZ, [to_vector(ADJ_O(g=g, G=G ,gen_i=i, vertices=vertices, gens=gens, v_idx=v_idx)) for i in range(num_v)]).transpose()
    BF_O_M = identity_matrix(ZZ, num_v) - ADJ_O_M
    BF_O_evects = BF_O_M.eigenvectors_right()
    for eigval, eigvects, alg_mult in BF_O_evects:
        if eigval == eigv:
                return len(eigvects), alg_mult
    print("ERROR01")
    # BF_O_E_spaces = BF_O.eigenspaces_right(format='galois')
    # eig_minus_eigv = [space for val, space in BF_O_E_spaces if int(val) == 2]

    # return eig_minus_eigv[0] if len(eig_minus_eigv) >= 1 else print("Problably not a Line-Oriented Graph."), get_alg_mult(BF_O.fcp(), eigv=eigv)

def get_ADJO_mult(g, eigv):
    vertices = list(g.vertices())
    num_v = len(vertices)
    v_idx = {v: i for i, v in enumerate(vertices)}

    G = AdditiveAbelianGroup([0] * num_v)
    gens = G.gens()

    ADJ_O_M = matrix(ZZ, [to_vector(ADJ_O(g=g, G=G ,gen_i=i, vertices=vertices, gens=gens, v_idx=v_idx)) for i in range(num_v)]).transpose()
    ADJ_O_evects = ADJ_O_M.eigenvectors_right()
    for eigval, eigvects, alg_mult in ADJ_O_evects:
        if eigval == eigv:
                return len(eigvects), alg_mult
    return print("ERROR02")
    # ADJ_O_E_spaces = ADJ_O_M.eigenspaces_right(format='galois')
    # ADJ_O_E_vectors = ADJ_O_M.eigenvectors_right(format='galois')

    # for val, spaces in ADJ_O_E_spaces:

    #     print("(val in ADJ_O_E_space) type(val) == ", type(val))

    # eig_minus_eigv = [space for val, space in ADJ_O_E_spaces if int(val) == -1]
    # print("eig_minus_eigv == ", eig_minus_eigv)
    # for val, spaces in ADJ_O_E_spaces:
    #     print(f"val == {val}")

    # print("get_ADJO_mult() eig_minus_eigv == ", eig_minus_eigv)
    # return eig_minus_eigv[0].dimension() if len(eig_minus_eigv) >= 1 else print("Problably not a Line-Oriented Graph."), 
            # get_alg_mult(ADJ_O_M.fcp(), eigv=eigv)

def get_alg_mult(f, eigv):
    for eigvalue, mult in f:
        print("(get_alg_mult()) eigvalue == ", eigvalue)
        if eigvalue == eigv:
            return mult
        
def to_vector(x):
    # AdditiveAbelianGroup elements store coords directly
    return vector(ZZ, x)

def ADJ_O(g, G, gen_i, vertices, gens, v_idx):
    v = vertices[gen_i]
    result = G.zero()
    for u in g.neighbors(v):
        result += gens[v_idx[u]]
    return result

# def get_BF_geo_mult_helper(g: DiGraph):
#     vertices =list(g.vertices())
#     edges = list(g.edges())
#     num_e = len(edges)
#     G = AdditiveAbelianGroup([0]*len(vertices))
#     # G = Groups().Commutative().free(index_set=vertices)
#     ADJ_O = lambda v: sum(g.neighbors(v))
#     # col_basis_ADJ_O = [ADJ_O(v) for v in vertices]
#     # Build matrix column by column (operator applied to each basis element)
#     ADJ_O_M = matrix(ZZ, [to_vector(ADJ_O(v)) for v in gens]).transpose()
#     BF_O = (identity_matrix(num_e) - ADJ_O_M)

#     return BF_O.eigenspace(-1).dimension()
# def to_vector(x, rnk):
#         d = x.dict()   # {generator_index: coefficient}
# #         return vector(ZZ, [d.get(i, 0) for i in range(rnk)])
# get_BFO_geo_mult(DiGraph({'a': ['b','b', 'c'], 'b': ['a','b','c'], 'c': ['a']}))
get_Sebastians_mults(line_orient_graph(Graph({0: [0,0,0]})))

# In[ ]:


def check_stickelberger_stuff(p, n):
    X = DiGraph(loops=True, multiedges=True)
    X.add_edge(0, 0, (0, 0)) 
    
    for i in range(1, p^n):        
        for j in range(1, i+1):
            if i % p != 0:      
                X.add_edge(0, 0, (i, j))
    DELTA = AdditiveAbelianGroup([euler_phi(p^n)])
    ZZ_DELTA = GroupAlgebra(DELTA, ZZ)
    gen = DELTA.gen(0)
    GEN = ZZ_DELTA(gen)
    # print("gen ==", gen)
    zeta_p = primitive_root(p)
    def phi(i):
        if i == 0:
            return DELTA.zero()
        
        k = discrete_log(Mod(i, p^n), Mod(zeta_p, p^n))
        return k*gen
    
    def alpha(e):
        label = e[2]              
        i = label[0]
        if i == 0:
            return phi(1)         
        else:
            return -phi(i)
    # RHS = ZZ_DELTA.one() - sum(alpha(e) for e in X.edges())
    # # RHS = 1-sum([alpha(e) for e in X.edges()], hold=True)
    # # LHS = -sum([a*(-phi(a)) for a in range(0,p^n+1) if a % p != 0], hold=True)
    # units = [a for a in range(1, p^n + 1) if gcd(a, p) == 1]
    # LHS = -sum(a * ZZ_DELTA(-phi(a)) for a in units)
    # RHS = ZZ_DELTA.one() - sum(alpha(e) for e in X.edges())
    # LHS = -sum(a * ZZ_DELTA(-phi(a)) for a in range(1, p^n+1) if gcd(a,p) == 1)
    # RHS = ZZ_DELTA.one() - sum((alpha(e) for e in X.edges()), ZZ_DELTA.zero())
    # LHS = -sum((a * ZZ_DELTA(-phi(a)) for a in range(1, p^n+1) if gcd(a,p) == 1), ZZ_DELTA.zero())

    # RHS
    # rhs_sum = [ZZ_DELTA.one()]
    # for e in X.edges():
    #     rhs_sum = rhs_sum.append(ZZ_DELTA(alpha(e)))
    rhs_sum_lst = [ZZ_DELTA.zero()]
    for e in X.edges():
        rhs_sum_lst.append(alpha(e))
    rhs_sum_lst = [ZZ_DELTA(-1)*ZZ_DELTA(elt) for elt in rhs_sum_lst]


    # LHS
    lhs_sum_lst = []
    for a in range(1, p^n + 1):
        if gcd(a, p) == 1:
            lhs_sum_lst.append(a * ZZ_DELTA(-phi(a)))
    lhs_sum_lst = [ZZ_DELTA(-1)*ZZ_DELTA(elt) for elt in lhs_sum_lst]

    print(f"RHS == {rhs_sum_lst}, LHS == {lhs_sum_lst}")

print(check_stickelberger_stuff(3,2))   

# In[ ]:


def T_stickelberger_stuff(p, n, t):
    X = DiGraph(loops=True, multiedges=True)
    X.add_edge(0, 0, (0, 0)) 
    
    for i in range(1, p^n):        
        for j in range(1, i+1):
            if i % p != 0:      
                X.add_edge(0, 0, (i, j))
    DELTA = AdditiveAbelianGroup([euler_phi(p^n)])
    ZZ_DELTA = GroupAlgebra(DELTA, ZZ)
    gen = DELTA.gen(0)
    GEN = ZZ_DELTA(gen)
    # print("gen ==", gen)
    zeta_p = primitive_root(p)
    def phi(i):
        if i == 0:
            return DELTA.zero()
        
        k = discrete_log(Mod(i, p^n), Mod(zeta_p, p^n))
        return k*gen
    
    def alpha(e):
        label = e[2]              
        i = label[0]
        if i == 0:
            return phi(1)         
        else:
            return -phi(i)
 
    rhs_sum_lst = [ZZ_DELTA.zero()]
    for e in X.edges():
        rhs_sum_lst.append(alpha(e))
    rhs_sum_lst = [ZZ_DELTA(-1)*ZZ_DELTA(elt) for elt in rhs_sum_lst]


    lhs_sum_lst = []
    for a in range(1, p^n + 1):
        if gcd(a, p) == 1:
            lhs_sum_lst.append(a * ZZ_DELTA(-phi(a)))
    lhs_sum_lst = [ZZ_DELTA(-1)*ZZ_DELTA(elt) for elt in lhs_sum_lst]

    

# In[ ]:


def BF_p_power_conjecture(p, n):
    X = DiGraph(loops=True, multiedges=True)
    X.add_edge(0, 0, (0, 0)) 
    for i in range(1, p^n):        
        for j in range(1, i+1): 
            if i % p != 0:   
                X.add_edge(0, 0, (i, j))
            # print("X edge == ", (i,j))
  
    # X.show()
    DELTA = AdditiveAbelianGroup([euler_phi(p^n)])
    gen = DELTA.gen(0)
    # print("gen ==", gen)
    zeta_p = primitive_root(p)
    def phi(i):
        if i == 0:
            return DELTA.zero()
        
        k = discrete_log(Mod(i, p), Mod(zeta_p, p))
        return k * gen
    
    def alpha(e):
        label = e[2]              
        i = label[0]
        if i == 0:
            return phi(1)         
        else:
            return -phi(i)        
        
    Y = voltage_cover(X, DELTA, alpha)
    
    BFO = identity_matrix(Y.order()) - Y.adjacency_matrix()
    BF_SNF, non_var0, non_var1 = BFO.smith_form()
    # print(BF_SNF)
    BF_TOR_ORD = prod([entry for entry in BF_SNF.diagonal() if entry != 0])
    minus_class_number = cyclotomic_minus_class_number(p,n)
    h_minus_factorization = 0
    if is_prime(minus_class_number):
        h_minus_factorization = minus_class_number
    else:
        h_minus_factorization = factor(minus_class_number)
    print("minus_class_number == ",minus_class_number)
    print(f"p = {p}, n == {n},      BF torsion part order == {BF_TOR_ORD} = {factor(BF_TOR_ORD)},      minus class number == {minus_class_number} = {h_minus_factorization}")

# for n in range (1, 101):
#     p = next_prime(n)
BF_p_power_conjecture(3, 2)
print()

# In[ ]:



# def get_geo_mult(g):
#     G = line_orient_graph(g)
#     EC = G.order()-len(list(G.edges()))
#     if EC % 2 == 0 or ____:
#         print("ERROR: ASK SEBASTIAN")
#         return # number of spanning trees cannot be even.
    
#     return print(f"{get_ADJO_multiplicities()}")


# In[ ]:


import random as rm

for cnt in range(0,100):
    num_v = 8            
    e_prob= 0.4             
    g = Graph(num_v, multiedges=True, loops = True)
    
    # extra_e = rm.randint(1,5)
    extra_e = 40
    for u in range(num_v):
        for v in range(u, num_v+extra_e):
            if u == v:
                if rm.random() < 0.5:
                    g.add_edge(u,v)
            elif rm.random() < e_prob:
                g.add_edge(u, v)
    #num_v = rm.randint(3, 5)
    # g = graphs.RandomGNP(num_v, 1,)  # 3-5 vertices, edge prob == 1
    # g.show()
    G = line_orient_graph(g)
    # G.show()
    num_e_g = len(g.edges())
    G = line_orient_graph(g)
    adjm_G = G.adjacency_matrix()

    # print(f"Number of edges of G == {G.size()}")
    I_SNF= (identity_matrix(2*num_e_g)-adjm_G).smith_form(transformation=False)
    # print("Number of nonzero entries == ",sum(1 for x in I_SNF.diagonal() if x != 0))
    # print("Number of nonzero/not equal to 1 entries == ",sum(1 for x in I_SNF.diagonal() if x != 0 and x != 1))
    roots_lst = adjm_G.characteristic_polynomial().roots()
    AM1 = next((mult for val, mult in roots_lst if val == 1), 0)
    GM1 =(adjm_G - 1*identity_matrix(adjm_G.nrows())).nullity()
    
    
    nonzero_diags = [x for x in I_SNF.diagonal() if x != 0]
    EC = g.order()-num_e_g
    TORSPART = prod(nonzero_diags)
    print(f"AM1 == {AM1}, GM1 == {GM1}, #of !=0 entries == {sum(1 for x in I_SNF.diagonal() if x != 0)}, #of !=0,1 edges == {sum(1 for x in I_SNF.diagonal() if x != 0 and x != 1)}, #AM1+EC == {AM1 + EC}, # GM1+EC == {GM1 + EC}, ")
    print(f"TORSPART == {TORSPART}     EC == {EC}")
    print(f"#of spanning trees of the origninal graph == {g.spanning_trees_count()}, #of pairs of two vertices in G == {binomial(G.order(),2)}")
    print()
    if TORSPART + EC != 0:
        print("COUNTER EXAMPLE")
        g.show()
        G.show()
        break

# In[ ]:


import random as rm

for cnt in range(0,1):
    num_v = 5            
    e_prob= 0.5             
    g = Graph(num_v, multiedges=True, loops = True)
    
    # extra_e = rm.randint(1,5)
    extra_e = 15
    for u in range(num_v):
        for v in range(u, num_v+extra_e):
            if u == v:
                if rm.random() < 0.5:
                    g.add_edge(u,v)
            elif rm.random() < e_prob:
                g.add_edge(u, v)
    #num_v = rm.randint(3, 5)
    # g = graphs.RandomGNP(num_v, 1,)  # 3-5 vertices, edge prob == 1
    g.show()
    G = line_orient_graph(g)
    G.show()
    num_e_g = len(g.edges())
    G = line_orient_graph(g)
    adjm_G = G.adjacency_matrix()

    # print(f"Number of edges of G == {G.size()}")
    I_SNF= (identity_matrix(2*num_e_g)-adjm_G).smith_form(transformation=False)
    # print("Number of nonzero entries == ",sum(1 for x in I_SNF.diagonal() if x != 0))
    # print("Number of nonzero/not equal to 1 entries == ",sum(1 for x in I_SNF.diagonal() if x != 0 and x != 1))
    roots_lst = adjm_G.characteristic_polynomial().roots()
    # print("Algebraic multiplicity of the the eigen value equal to 1 ==", next((mult for val, mult in roots_lst if val == 1), 0))
    nonzero_diags = [x for x in I_SNF.diagonal() if x != 0]
    EC = g.order()-num_e_g
    TORSPART = prod(nonzero_diags)

    # print(f"TORSPART == {TORSPART}     EC == {EC}")
    if TORSPART + EC != 0:
        # print("COUNTER EXAMPLE")
        g.show()
        G.show()
        break
    # print("order:", G.order())
    # print("size:", G.size())
    # print("num_edges:", G.num_edges())
    # print("len(edges()):", len(G.edges()))
    # print("adj dims:", G.adjacency_matrix().dimensions())
    # print("adj nonzero:", G.adjacency_matrix().nnz())  # number of nonzero entries
    # print("type:", type(G))
    # EC = G.order()-num_e
    # I_SNF= (identity_matrix(ZZ, 2*num_e)-G.adjacency_matrix()).smith_form(transformation=False)
    # nonzero_diags = [x for x in I_SNF.diagonal() if x != 0]
    # TORSPART = prod(nonzero_diags)
    # print(f"Euler Characteristic == {EC} Order torsion part of the BF group == {TORSPART}")

# In[ ]:




# In[ ]:


g = Graph({0: [0,0, 0]}) # 3 line Boquet
num_e_g = len(g.edges())
G = line_orient_graph(g)
num_e = len(G.edges())
print(f"Number of edges of G == {G.size()}")
I_SNF= (identity_matrix(6)-G.adjacency_matrix()).smith_form(transformation=False)
nonzero_diags = [x for x in I_SNF.diagonal() if x != 0]
EC = g.order()-num_e_g
print("EC ==", EC)
TORSPART = prod(nonzero_diags)
print("TORSPART == ", TORSPART)
