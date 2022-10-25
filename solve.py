##
# 2WF90 Algebra for Security -- Software Assignment 2
# Polynomial and Finite Field Arithmetic
# solve.py
#
#
# Group number:
# 28 
#
# Author names and student IDs:
# Atilla Rzazade (1552848)
# Daua Karajeanes (1619675)
# Valentina Marinova (1665154)
# Gergana Valkova (1676385)
##

# Import built-in json library for handling input/output 
from dataclasses import field
import json
from operator import truediv
from re import A


def solve_exercise(exercise_location : str, answer_location : str):
    """
    solves an exercise specified in the file located at exercise_location and
    writes the answer to a file at answer_location. Note: the file at
    answer_location might not exist yet and, hence, might still need to be created.
    """
    
    # Open file at exercise_location for reading.
    with open(exercise_location, "r") as exercise_file:
        # Deserialize JSON exercise data present in exercise_file to corresponding Python exercise data 
        exercise = json.load(exercise_file)
        

    ### Parse and solve ###

    # Check type of exercise
    if exercise["type"] == "polynomial_arithmetic":
        # Check what task within the polynomial arithmetic tasks we need to perform
        if exercise["task"] == "addition":
            # Solve polynomial arithmetic addition exercise
            pass
        elif exercise["task"] == "subtraction":
            # Solve polynomial arithmetic subtraction exercise
            pass
        # et cetera
    else: # exercise["type"] == "finite_field_arithmetic"
        # Check what task within the finite field arithmetic tasks we need to perform
        if exercise["task"] == "addition":
            # Solve finite field arithmetic addition exercise
            pass
        # et cetera


    # Open file at answer_location for writing, creating the file if it does not exist yet
    # (and overwriting it if it does already exist).
    with open(answer_location, "w") as answer_file:
        # Serialize Python answer data (stored in answer) to JSON answer data and write it to answer_file
        json.dump(answer, answer_file, indent=4)
    
def polynomial_arithmetic_additon(mod, f, g):
    min_length = min(len(g), len(f))
    # copying the longer array into the answer array
    if len(g) < len(f):
        a = [i for i in f]
    else:
        a = [i for i in g]
    
    #fills the answer array with the addition of the terms of the two polynomials
    for i in range(min_length):
        if (i < min_length):
            a[i] = g[i] + f[i] 
            #makes sure that the end result is in the given mod
            while (a[i] >= mod):
                a[i] = a[i] - mod

    return a

def polynomial_arithmetic_subtraction(mod, f, g):
    # copying the longer array into the answer array
    min_length = min(len(g), len(f))
    if len(g) < len(f):
        a = [i for i in f]
    else:
        a = [i for i in g]
    
    #fills the answer array with the subtraction of the terms of the two polynomials
    for i in range(min_length):
        if (i < min_length):
            a[i] = f[i] - g[i] 
            #makes sure that the end result is in the given mod
            while (a[i] < 0):
                a[i] = a[i] + mod

    return a

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


# clears the array from leading 0s
def clean_array(r):
    i = len(r) - 1 

    while r[i] == 0 and i > 0:
        r = r[0:i]
        i = i - 1 
    
    return r  


def input_check(f,g,m):
    return True if get_degree(f) == -1 else False, True if get_degree(g) == -1 else False, False if m >= 2 else True

    

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
        return None, None

    # case : g = 0
    if (gIsZ):
        return None, None

    # case: f = 0 and g != 0
    if (fIsZ) and (get_degree(g) > 0):
        return [0], [0]


    # self explanatory, if g has higher degree then return quotient = 0, remainder = f
    if get_degree(f) < get_degree(g):
        return [0],f 

    
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




# print(polynomial_irreducibility_check([1,1,0,1],2))

# print(polynomial_extended_euclidian([4,4,0,1],[1,1],5))
# print(polynomial_extended_euclidian([4,4,0,1],[1,1],5))


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

def finite_field_addition(mod, f, g, p_mod):
    a = polynomial_arithmetic_additon(mod, f, g)
    q, r = polynomial_division(a, p_mod, mod)
    
    return clean_array(r)

# for testing:
# user_file = open('exercise10 (3).json', 'r')
# file_contents = user_file.read()
# user_file.close()
# parsed_json = json.loads(file_contents)

# print(finite_field_addition(parsed_json['integer_modulus'], parsed_json['f'], parsed_json['g'], parsed_json['polynomial_modulus']))

def finite_field_subtraction(mod, f, g, p_mod):
    a = polynomial_arithmetic_subtraction(mod, f, g)
    q, r = polynomial_division(a, p_mod, mod)
    
    return clean_array(r)

# for testing:
# print(finite_field_subtraction(2, [0,1,1], [0,1,1], [1,1,0,1]))

def finite_field_multiplication(mod, f, g, p_mod):
    a = polynomial_multiplication(f, g, mod)
    q, r = polynomial_division(a, p_mod, mod)
    return clean_array(r)


def finite_field_division(mod, f, g, p_mod):

    q , r = polynomial_division(f, g, mod)

    if get_degree(q) > get_degree(p_mod)-1:
        q , r_q =  polynomial_division(q, p_mod, mod)
    
    if get_degree(r) > get_degree(p_mod)-1:
        q_r , r =  polynomial_division(q, p_mod, mod)
    
    return clean_array(q) , clean_array(r)

def decomposition (n):
    i = 2
    decomp = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            decomp.append(i)
    if n > 1:
        decomp.append(n)
    return decomp

def is_prime(n):
  for i in range(2,n):
    if (n%i) == 0:
      return False
  return True

def is_one(f):
    if len(f) == 0:
        return False
    if f[0] != 1:
        return False
    for i in range (1, len(f)):
        if f[i] != 0:
            return False

    return True

def finite_field_primitivity_check(mod, f, p_mod):
    ord = (mod**get_degree(f)) - 1
    
    if is_prime(ord):
        return True

    check = True  
    powers = []
    results = []  
      
    ord_dec = set(decomposition(ord)) # get the prime divisors only once
    for dec in ord_dec:
        powers.append(ord // dec)
    for power in powers:
        total = f
        for i in range (power-1):
            total = finite_field_multiplication(mod, f, total, p_mod)
        results.append(total)
    for result in results:
        if is_one(result):
            check = False 
    
    return check