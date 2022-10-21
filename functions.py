from asyncio.windows_events import NULL
from operator import inv
from solve import polynomial_arithmetic_subtraction



# swaps the arrays
def swap(f,g):
    h = f
    f = g
    g = h
    return f,g

# find inverse of x for mod m
def mod_inv(x,mod):
    for i in range(1,mod):
        if ((x*i) % mod == 1):
            return i

# find degree of polynomial f
def get_degree(f):
    return -1 if (len(f) == 1 and (f[0] == 0)) else len(f) - 1 


# cleans the array from leading 0s
def clean_array(r):
    for i in range(len(r) - 1, 0, -1):
        if r[i] == 0:
            r = r[0:i] 
    return r  


def input_check(f,g,m):
    return True if get_degree(f) == -1 else False, True if get_degree(g) == -1 else False, False if m > 2 else True

    

# multiply 2 polynomials f,g with mod m
def polynomial_multiplication(f, g, m):

    fIsZ, gIsZ, mIsZ = input_check(f,g,m)

    # modulus = 0
    if mIsZ:
        return None

    # f = 0 or g = 0 (also covers the case where (f = 0, g != 0) and vice versa)
    if fIsZ or gIsZ:
        return [0]

    l = len(f)
    k = len(g)

    result = [0] * (l + k - 1) 

    for i in range(l):
        for j in range(k):
            result[i+j] += f[i]*g[j]

    for e in range(0,len(result)):
        result[e] %= m

    return result


# polynomial long division
def polynomial_division(f,g,m):

    fIsZ, gIsZ, mIsZ = input_check(f,g,m)

    # case : modulus = 0 
    if mIsZ:
        return None

    # case : g = 0
    if (gIsZ):
        return None

    # case: f = 0 and g != 0
    if (fIsZ) and (get_degree(g) > 0):
        return [0], [0]


    # self explanatory, if g has higher degree then return quotient = 0, remainder = f
    if get_degree(f) < get_degree(g):
        return 0,f 

    
    inv_lcg = mod_inv(g[-1],m)

    r, q = f, [ 0 ] * (max(get_degree(f),get_degree(g))+1)


    while  get_degree(r) >= get_degree(g) and (get_degree(r) != -1):
        i = get_degree(r) - get_degree(g)
        c = (r[-1] * inv_lcg) % m
        t = [ 0 ] * (i+1)
        t[-1] = c
        q[i] += (c) 
        tg = polynomial_multiplication(t, g, m)
        r = clean_array(polynomial_arithmetic_subtraction(m,r,tg)) 
    

    return clean_array(q),r



# INCOMPLETE
# finds x,y and d, where d = gcd(f,g) and xf + yg = d (all values are mod m)
def polynomial_extended_euclidian(f,g,m):

    # inverse of the lc(f) for the normalized output
    ilcf = [mod_inv(f[-1],m)]

    # swap polynomials if degree of F is smaller than G
    if get_degree(g) > get_degree(f):
        f, g = swap(f,g)

    # based on the ext.euc. algo. x = x1, v = y2
    x,v = [1],[1] 

    # y = y1, u = x2
    y,u = [0],[0]

    while get_degree(g) != -1:
        # get q and r
        q, r = polynomial_division(f,g,m)

        # to calculate (g,r) in the next iteration
        f = g
        g = r

        # dummy variables to hold x and y
        dx = x
        dy = y

        # the values are set for the next iteration
        x = u
        y = v
        
        # calculate the for next iterations of u and v (for g_i)
        u = polynomial_arithmetic_subtraction(m,dx,polynomial_multiplication(q,u,m))
        v = polynomial_arithmetic_subtraction(m,dy,polynomial_multiplication(q,v,m))

    # normalize x,y for xf + yg = gcd(f,g) 
    normX = polynomial_multiplication(x,ilcf,m)
    normY = polynomial_multiplication(y,ilcf,m)
    
    #gcd = f

    # add gcd return    
    return normX, normY#, gcd

def irreducibility_input_check(f,p):
    return False if ((get_degree(f) == -1) or (get_degree(f) > 5)) else True, False if ((13 < p) or (p < 2)) else True

def polynomial_irreducibility_check(f,p):
    
    fIsW, pIsW = irreducibility_input_check(f,p)

    # prime not in range
    if pIsW:
        return None
    
    # polynomial degree incorrect
    if fIsW:
        return None

    # all linear polynomials are irreducible
    if get_degree(f) == 1:
        return True

     # all polynomials (!= 0) without a constant is reducible
    if f[0] == 0:
        return True
    
    # all polynomials = c + x^n are irreducible
    if f[0] != 0 and [f[i] == 0 for i in range(1,len(f)-1)]:
        return True
    
    
    # implement Eisenstein criteron
            


    return True




print(polynomial_irreducibility_check([1,1,0,1],2))

# print(polynomial_extended_euclidian([4,4,0,1],[1,1],5))
print(polynomial_extended_euclidian([4,4,0,1],[1,1],5))


# print(polynomial_subtraction([0,0,0,1],[0,1],2))

# Test cases for division

# print(polynomial_division([4,4,0,1],[0], 5)) # None
# print(polynomial_division([0],[0], 5)) # None
# print(polynomial_division([0],[4,4,0,1], 5)) # 0, 0
# print(polynomial_division([4,4,0,1],[1,1], 5)) # q,r
# print(polynomial_division([4,4,0,1],[1,1], 0)) # None


# Test cases for multiplication  

# print(polynomial_multiplication([4,4,0,1],[0], 5)) # 0
# print(polynomial_multiplication([0],[0], 5)) # 0
# print(polynomial_multiplication([0],[4,4,0,1], 5)) # 0
# print(polynomial_multiplication([4,4,0,1],[1,1], 5)) # result
# print(polynomial_multiplication([4,4,0,1],[1,1], 0)) # None

