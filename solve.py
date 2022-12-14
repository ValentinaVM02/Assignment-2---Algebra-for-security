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
import json
from random import randrange
import random as random



    
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
    
    q = clear_array(q)

    # returns the quotient and remainder (clear from leading zeroes)
    return q,r

# 
# finds x,y and d, where d = gcd(f,g) and xf + yg = d (all values are mod m)
def polynomial_extended_euclidian(f,g,m):
    
    # undefined modulus
    if m == 0:
        return None, None, None

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


def irreducible_polynomial_generator(n,p):
    # create an array (len=n) of random coeff in range(0,p)
    polynomial = element_gen(n,p)
    reducibles = [[]] 

    while (not polynomial_irreducibility_check(polynomial,p)) or (polynomial in reducibles):
        if (polynomial not in reducibles):
            reducibles.append(polynomial)
        polynomial = element_gen(n,p)
    
    # degree(f) = n & f is irreducible
    return polynomial


def finite_field_addition(mod, f, g, p_mod):
    #calculates the sum of the same degree polynomials 
    a = polynomial_arithmetic_additon(mod, f, g)
    #calculates the answer using the polynomial division where the answer is the remeinder of the calculation
    q, r = polynomial_division(a, p_mod, mod)
    #any leading zeros from the answer
    return clear_array(r)


def finite_field_subtraction(mod, f, g, p_mod):
    #calculates the difference of the same degree polynomials
    a = polynomial_arithmetic_subtraction(mod, f, g)
    #calculates the answer using the polynomial division where the answer is the remeinder of the calculation
    q, r = polynomial_division(a, p_mod, mod)
    
    return clear_array(r)


def finite_field_multiplication(mod, f, g, p_mod):
    a = polynomial_multiplication(f, g, mod)
    q, r = polynomial_division(a, p_mod, mod)
    
    return clear_array(r)


def finite_field_division(mod, f, g, p_mod):
    
    q , r = polynomial_division(f, g, mod)

    r_q, q =  polynomial_division(q, p_mod, mod)
    
    q_r , r =  polynomial_division(r, p_mod, mod)
    
    return clear_array(q) , clear_array(r)


def finite_field_inversion(mod, f, p_mod):
    d, x, y = polynomial_extended_euclidian(f,p_mod, mod)
    q_f, r_f = polynomial_division(x,p_mod,mod)
    
    if len(d) == 1:
        return r_f
    else:
        return None
        

# provide the prime dividers of a number
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


# check whether a number is prime
def is_prime(n):
  for i in range(2,n):
    if (n%i) == 0:
      return False
  return True


# check whether a polynomial equals 1
def is_one(f):
    if len(f) == 0:
        return False
    if f[0] != 1:
        return False
    for i in range (1, len(f)):
        if f[i] != 0:
            return False
    return True


# check if a certain polynomial is primitive
def finite_field_primitivity_check(mod, f, p_mod):
    ord = (mod**get_degree(f)) - 1 # determine its order
    
    if is_prime(ord):
        return True

    check = True # store the boolean value 
    powers = [] # store the powers to which the polynomial should be raised
    results = [] # store the results of the polynomial raised to the certain powers
      
    ord_dec = set(decomposition(ord)) # get the prime divisors only once
    for dec in ord_dec:
        powers.append(ord // dec) # calculate the needed powers and put them into the array
    for power in powers:
        total = f
        for i in range (power-1):
            total = finite_field_multiplication(mod, f, total, p_mod) # calculate the raised polynomials
        results.append(total) # add the results in the array
    for result in results:
        if is_one(result): # check if the result is 1, if it is then the polynomial is not primitive
            check = False 
    
    return check
# generate a random polynomial that is in field F
def random_element_in_F(mod, p_mod):
    a = []
    for i in range (len(p_mod)):
        a.append(randrange(0, mod)) # add numbers to the emptry array that are within mod and the legth of the array is withing p_mod
    q,r = polynomial_division(a, p_mod, mod)

    return clear_array(r)

# generate new polynomials until one of them is primitive
def primitive_element_generation(mod, p_mod):
    a = random_element_in_F(mod, p_mod) # generate a random polynomial in the field F
    while not finite_field_primitivity_check(mod, a, p_mod): # do a while loop until you find a primitive element
        a = random_element_in_F(mod, p_mod)

    return a

# for testing:
# user_file = open('exercise8 (2).json', 'r')
# file_contents = user_file.read()
# user_file.close()
# parsed_json = json.loads(file_contents)

# print(finite_field_division(parsed_json['integer_modulus'], parsed_json['f'], parsed_json['g'], parsed_json['polynomial_modulus']))


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
    m = exercise["integer_modulus"]   
    degree = exercise["degree"] if exercise["task"] == "irreducible_element_generation" else 0
    f = exercise["f"] if not(exercise["task"] == "irreducible_element_generation" or exercise["task"] == "primitive_element_generation") else []
    g = exercise["g"] if exercise["task"] in ["addition", "subtraction", "multiplication", "long_division",
                                                    "extended_euclidean_algorithm","divison"] else []
        
    
    # Check type of exercise
    if exercise["type"] == "polynomial_arithmetic":
        # Check what task within the polynomial arithmetic tasks we need to perform
        if exercise["task"] == "addition":
            result = polynomial_arithmetic_additon(m,f,g)
        elif exercise["task"] == "subtraction":
            result = polynomial_arithmetic_subtraction(m,f,g)
        elif exercise["task"] == "multiplication":
            result = polynomial_multiplication(f,g,m)
        elif exercise["task"] == "long_division":
            q,r = polynomial_division(f,g,m)
            answer = {"answer-q":q, "answer-r":r} if q != None else {"answer":None}
        elif exercise["task"] == "extended_euclidean_algorithm":
            gcd,a,b = polynomial_extended_euclidian(f,g,m)
            answer = {"answer-a":a, "answer-b":b, "answer-gcd":gcd} if gcd != None else {"answer":None}
        elif exercise["task"] == "irreducibility_check":
            isIrreducible = polynomial_irreducibility_check(f,m)
            answer = {"answer": isIrreducible} if isIrreducible != None else {"answer":None}
        elif exercise["task"] == "irreducible_element_generation":
            result = irreducible_polynomial_generator(degree,m) 
    else: # exercise["type"] == "finite_field_arithmetic"
        # Check what task within the finite field arithmetic tasks we need to perform
        poly_mod = exercise["polynomial_modulus"] 
        if exercise["task"] == "addition":
            result = finite_field_addition(m,f,g,poly_mod)
        elif exercise["task"] == "subtraction":
            result = finite_field_subtraction(m,f,g,poly_mod)
        elif exercise["task"] == "multiplication":
            result = finite_field_multiplication(m,f,g,poly_mod)
        elif exercise["task"] == "division":
            q, r = finite_field_division(m,f,g,poly_mod)
            answer = {"answer-q":q, "answer-r":r} if q != None else {"answer":None}
        elif exercise["task"] == "inversion":
            result = finite_field_inversion(m,f,poly_mod)
        elif exercise["task"] == "primitivity_check":
            result = finite_field_primitivity_check(m,f,poly_mod)
        elif exercise["task"] == "primitive_element_generation":
            result = primitive_element_generation(m, poly_mod)
    
    if exercise["task"] in ["addition","subtraction","multiplication","irreducible_element_generation"]:
            answer = {"answer": result} 


    # Open file at answer_location for writing, creating the file if it does not exist yet
    # (and overwriting it if it does already exist).
    with open(answer_location, "w") as answer_file:
        # Serialize Python answer data (stored in answer) to JSON answer data and write it to answer_file
        json.dump(answer, answer_file, indent=4)
    