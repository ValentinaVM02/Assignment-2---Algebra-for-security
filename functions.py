import random as random
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
            return [i]

# find degree of polynomial f
def get_degree(f):
    return -1 if (len(f) == 1 and (f[0] == 0)) else len(f) - 1 

# cleans the array from leading 0s
def clear_array(r):
    i = len(r) - 1 

    while r[i] == 0 and i > 0:
        r = r[0:i]
        i = i - 1 
    
    return r

# checks whether the inputs are in right format, i.e if modulus != 0
def input_check(f,g,m):
    return True if get_degree(f) == -1 else False, True if get_degree(g) == -1 else False, False if m >= 2 else True
    
# multiply 2 polynomials f,g with mod m
def polynomial_multiplication(f, g, m):

    
    # "--"IsZ - is set to True iff "--" = 0, i.e. if f = [0] => fIsZ = True
    fIsZ, gIsZ, mIsZ = input_check(f,g,m)

    # modulus = 0
    if mIsZ:
        return None

    # f = 0 or g = 0 (also covers the case where (f = 0, g != 0) and vice versa)
    if fIsZ or gIsZ:
        return [0]

    # self-explanatory
    l = len(f)
    k = len(g)

    # resulting array length can not be greater than the sum of length of the polynomial arrays. 
    result = [0] * (l + k - 1) 

    # i,j denote the index and the degree of the monomial, i.e. if i = 2 => f[2] = 5 => 5(X^2)
    # multiply every index i of f with every index j of g, add the resulting value to the i+j index.
    # i.e f[2] = 5, g[3] = 3, f[i](X^i)*g[j](X^j) = (f[i] * g[j]) (X^(i+j)) = 5(X^2) * 3(X^3) = 15(X^5)
    for i in range(l):
        for j in range(k):
            result[i+j] += f[i]*g[j]

    # turns all coefficients into modulo m values
    for e in range(0,len(result)):
        result[e] %= m

    return result


# polynomial long division
def polynomial_division(f,g,m):

    # "--"IsZ - is set to True iff "--" = 0, i.e. if f = [0] => fIsZ = True
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
        return [0],f 


    # inverse of lc(g)
    inv_lcg = mod_inv(g[-1],m)

    # initialize the array where len(array) = max(degree(f), degree(g)) + 1
    # remainder/quotient polynomial degree can not be greater than the degrees of the given parameters (since it is division)
    r, q = f, [ 0 ] * (max(get_degree(f),get_degree(g))+1)


    # the formula is from the algebra script we received, namely Algorithm 2.2.2.
    # while loop terminates when either remainder = 0 or degree(r) < degree(g) 
    while  get_degree(r) >= get_degree(g) and (get_degree(r) != -1):
        # denotes the power X in the given iteration
        i = get_degree(r) - get_degree(g)

        # the coefficient of X which is (lc(r) * lc(b)^-1, in this case r[-1] = lc(r) & inv_lcg = lc(g)^-1)
        c = (r[-1] * inv_lcg[0]) % m
        
        # holds the polynomial that will be subtracted from r
        t = [ 0 ] * (i+1)

        # lc(t) = c
        t[-1] = c

        # add the coefficient to the quotient array
        q[i] += (c) 
        
        # i = degree(r) - degree(g)
        # t = (lc(r) * inv(lc(g))) * (X^i)
        # g = given g
        tg = polynomial_multiplication(t, g, m)
        
        # tg = t * g
        # r = r - tg
        # the array is cleared from leading zeroes
        r = clear_array(polynomial_arithmetic_subtraction(m,r,tg)) 
    

    # returns the quotient and remainder (clear from leading zeroes)
    return clear_array(q),r

# 
# finds x,y and d, where d = gcd(f,g) and xf + yg = d (all values are mod m)
def polynomial_extended_euclidian(f,g,m):
    
    # undefined modulus
    if m == 0:
        return None

    # Base case for recursion
    if get_degree(f) == -1:
        return g, [0], [1]

    # remainder of the polynomial division f/g
    r = polynomial_division(g,f,m)[1]

    # for first recursive iteration, ext_euclidean for remainder and the value of the initial divisor 
    # for all the iteration afterwards, ext_euclidean for the previous divisor and remainder
    gcd,x1,y1 = polynomial_extended_euclidian(r,f,m)
    
    # 
    q = polynomial_division(g,f,m)[0]
    qx1 = polynomial_multiplication(q,x1,m)

    x = polynomial_arithmetic_subtraction(m,y1,qx1)
    y = x1

    return gcd,x,y

# only finds gcd, use it to check if the values for gcd are correct
def pol_gcd(f,g,m):

    if get_degree(f) == -1:
        return g

    return pol_gcd(polynomial_division(g,f,m)[1],f,m)

def irreducibility_input_check(f,p):
    return True if ((get_degree(f) == -1) or (get_degree(f) > 5)) else False, True if ((13 < p) or (p < 2)) else False

# function that checks for Eisenstein's Irreducibility Criterion 
def check(f,prime):

    # prime should not divide the leading coefficient
    if (f[-1] % prime == 0):
        return False
    
    # every other index should be divided by the prime 
    for i in range(1,len(f)):
        if (f[i] % prime != 0):
            return False
    
    # the constant should not be divided by prime^2
    if (f[0] % (prime * prime) == 0):
        return False

    return True


def polynomial_irreducibility_check(f,m):
    
    fIsW, pIsW = irreducibility_input_check(f,m)

    primes = [2,3,5,7,9,11,13]

    # prime not in range
    if pIsW:
        return None
    
    # polynomial degree incorrect
    if fIsW:
        return None

    # all linear polynomials are irreducible
    if get_degree(f) == 1:
        return True

     # all polynomials (!= 0) without a constant are reducible
    if f[0] == 0:
        return False
    
    # all polynomials = c + x^n are irreducible
    if f[0] != 0 and [f[i] == 0 for i in range(1,len(f)-1)]:
        return True
    
    
    # implement Eisenstein criteron
    for prime in primes:
        # check for every prime in range [2,13]
        if check(f,prime):
            return True

    return False

def irreducible_polynomial_generator(n,p):
    
    # create an array (len=n) of random coeff in range(0,p)
    polynomial = element_gen(n,p)

    # all the previously created reducible polynomials are stored here
    reducibles = [[]] 

    # the created polynomial should not be in the reducibles and should be irreducible
    while (not polynomial_irreducibility_check(polynomial,p)) or (polynomial in reducibles):
        
        # add to the reducibles if not there already
        if (polynomial not in reducibles):
            reducibles.append(polynomial)
        
        # create new polynomial for the next iteration
        polynomial = element_gen(n,p)
    
    # degree(f) = n & f is irreducible
    return polynomial


# create an array of random coefficients in given ranges
def element_gen(n,p):

    polynomial = [ 0 ] * (n+1)    

    for i in range(0,n):
        coeff = random.randint(0,(p-1))
        polynomial[i] = coeff

    # leading coefficient can not be zero
    polynomial[n] = random.randint(1,(p-1))
    
    return polynomial


# # Test cases for irreducibility check

# print(polynomial_irreducibility_check([0, 4, 0, 4],5)) # False since 4x + 4(x^3) is reducible
# print(polynomial_irreducibility_check([1,0,1],2)) # True since x^2 + 1 is irreducible

# Test cases for division

# print(polynomial_division([4,4,0,1],[0], 5)) # None since g is 0
# print(polynomial_division([0],[0], 5)) # None since 0/0 is undefined
# print(polynomial_division([0],[4,4,0,1], 5)) # 0, 0 since division of 0
# print(polynomial_division([2,1,1,4,2,3],[0,3,3,1,2], 5)) # q,r (arbitrary inputs)
# print(polynomial_division([4,4,0,1],[1,1], 0)) # None since modulus is 0


# Test cases for multiplication

# print(polynomial_multiplication([4,4,0,1],[0], 5)) # 0 (multiplication by zero)
# print(polynomial_multiplication([0],[0], 5)) # 0 (multiplication by 0)
# print(polynomial_multiplication([0],[4,4,0,1], 5)) # 0 (multiplication by 0)
# print(polynomial_multiplication([4,4,0,1],[1,1], 5)) # result 
# print(polynomial_multiplication([4,4,0,1],[1,1], 0)) # None since modulus 0