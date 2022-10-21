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