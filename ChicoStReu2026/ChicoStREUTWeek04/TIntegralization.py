from sage.all import *

def T_stickelberger_stuff(p, n, t):
    X = DiGraph(loops=True, multiedges=True)
    X.add_edge(0, 0, (0, 0)) 
    
    for i in range(1, p**n):        
        for j in range(1, i+1):
            if i % p != 0:      
                X.add_edge(0, 0, (i, j))
    DELTA = AdditiveAbelianGroup([euler_phi(p**n)])
    QQ_DELTA = GroupAlgebra(DELTA, QQ)
    gen = DELTA.gen(0)
    GEN = QQ_DELTA(gen)
    # print("gen ==", gen)
    zeta_p = primitive_root(p**n)
    def phi(i):
        if i == 0:
            return DELTA.zero()
        
        k = discrete_log(Mod(i, p**n), Mod(zeta_p, p**n))
        return k*gen
    
    def alpha(e):
        label = e[2]              
        i = label[0]
        if i == 0:
            return phi(1)         
        else:
            return -phi(i)
    
    lhs_sum_lst = []
    for a in range(1, p**n + 1):
        if gcd(a, p) == 1:
            lhs_sum_lst.append((a * QQ_DELTA(-phi(a)))/(p**n))
    lhs_sum_lst = [(QQ_DELTA(phi(t)) + QQ_DELTA(-t))*(QQ_DELTA(elt)) for elt in lhs_sum_lst]

    rhs_sum_lst = [QQ_DELTA.zero()]
    for e in X.edges():
        rhs_sum_lst.append(alpha(e))
    rhs_sum_lst = [QQ_DELTA(-1)*QQ_DELTA(elt) for elt in rhs_sum_lst]

    # print(f"n == {n}, LHS == {lhs_sum_lst}")
    print("LHS SUM == ", sum(lhs_sum_lst))
    print
    # print("RHS == ", rhs_sum_lst)
    # print("RHS SUM == ", sum(rhs_sum_lst) )
for n in range(1, 5):
    T_stickelberger_stuff(3,n,5)