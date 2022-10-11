##
# 2WF90 Algebra for Security -- Software Assignment 2
# Polynomial and Finite Field Arithmetic
# solve.py
#
#
# Group number:
# group_number 
#
# Author names and student IDs:
# author_name_1 (author_student_ID_1) 
# author_name_2 (author_student_ID_2)
# author_name_3 (author_student_ID_3)
# author_name_4 (author_student_ID_4)
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
    
def polynoial_arithmetic_additon(mod, f, g):
    # check which array has bigger size
    # do a for loop to add each coefficient 
    #    => add the two coefficient 
    # --> if bigger than the mode => while (coef > mod) coef - mod = coef 
    # if one is shorter just copy the bigger terms from the longer polynomial

    smaller_size_g = False
    smaller_size = min(len(g), len(f))
    a = []

    #checks which is the smaller array
    if smaller_size == len(g):
        smaller_size_g = True
    
    #fills the answer array with terms
    for i in max(len(g), len(f)):
        if (i < smaller_size):
            a[i] = g[i] + f[i] 
            #makes sure that the end result is in the given mod
            while (a[i] >= mod):
                a[i] = a[i] - mod
        #when one of the polynomial is shorter the higher terms of the other polynomial are copied and checked that 
        # they are in the given mod 
        else:
            if smaller_size_g:
                a[i] = f[i]
            else:
                a[i] = g[i]
            while (a[i] >= mod):
                a[i] = a[i] - mod


def polynoial_arithmetic_subtraction(mod, f, g):
    # check which array has bigger size
    # do a for loop to subtract each coefficient 
    #    => subtract the two coefficient
    # --> if bigger than the mode => while (coef < 0) coef + mod = coef 
    # if one is shorter just copy the bigger terms from the longer polynomial

    smaller_size_g = False
    smaller_size = min(len(g), len(f))
    a = []

    #checks which is the smaller array
    if smaller_size == len(g):
        smaller_size_g = True
    
    #fills the answer array with terms
    for i in max(len(g), len(f)):
        if (i < smaller_size):
            a[i] = f[i] - g[i] 
            #makes sure that the end result is in the given mod
            while (a[i] < 0):
                a[i] = a[i] + mod
        #when one of the polynomial is shorter the higher terms of the other polynomial are copied and checked that 
        # they are in the given mod 
        else:
            if smaller_size_g:
                a[i] = f[i]
            else:
                a[i] = g[i]
            while (a[i] < 0):
                a[i] = a[i] + mod
