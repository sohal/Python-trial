import math
import random 
import numpy as np
import sys

# Exercise 3 code : please ensure this is run in python3

class Calculator: #Make a class to hold functions
    def __init__(element, expression):
        element.i = 0 # position of pointer in "expression" string
        element.err_pos = -1 # states error positions 
        element.expr = expression #assigns the input "expression" to element.expr
        element.parenth_count = 0 # counter for the number of parenthesis
        element.error = None

    """collects numbers and checks for any wrongly entered characters e.g. letters"""
    def read_value(element):
        ei = element.i
        while(element.expr[ei:ei + 1].isdigit()): # while the pointed to character in the expression is a digit repeat this
            ei += 1 # increments ei to allow for while loop condition to check if the next character in the expression is still a number
        if(element.i == ei): # if element.i is still equivalent to ei it means the character pointed to is not a digit and hence must be a letter or inadequate symbol
            raise TypeError("Wrong character")#Exception/error
            return 0
        if(element.expr[ei:ei + 1]=="."):#if the ei pointer is on a "." then there is an invalid input(potentially a float)
            raise TypeError("non-integer number entered")#Exception/error
            return 0
        else:
            num = float(element.expr[element.i:ei]) # the number positioned between the initial pointer(element.i)
            #  and ei(the position of the final digit of a specific number) in the expression string is returned
            element.i = ei #the final digit of the number considered by this function from "expression" is where the new pointer is placed
            return num  #the whole number considered is returned

    def current_element(element):
        return element.expr[element.i:element.i+1] #returns whatever character the pointer ("element.i") is pointing to in the
        # element.expr(the initial expression string)

    #used to store the error position and reason for the error
    def error(element, reason):
        element.err_pos = element.i
        element.error = reason

    """if a space is found then go to next character"""
    def skip_spaces(element):
        while(element.current_element() == ' '):
            element.i += 1

    def parse_factors(element):
        number1 = element.parse_atom() #determines the number it comes across in the expression
        while(True):
            element.skip_spaces()
            op = element.expr[element.i:element.i+1]

            if(op != '/' and op != '*'):#when there is neither a * or / found in the "expression" where the pointer is at the number determined prior to it is returned
                return number1

            element.i += 1

            number2 = element.parse_atom()

            if(op == '/'):
                if(number2 == 0): #ensures that if you divide by a number it shall not be zero
                    raise TypeError("Divide by zero")
                    number1 = 0
                else:
                    number1 = number1 / number2 #conducts what mathematical operation 
            else:
                number1 = number1 * number2#conducts what mathematical operation 


    def tokenize(element):
        number1 = element.parse_factors()
        while(True):
            element.skip_spaces()
            op = element.expr[element.i:element.i+1]
            if(op != '-' and op != '+'): #when there is neither a + or - found in the "expression" where the pointer is at the number determined prior to it is returned
                return number1
            element.i += 1
            number2 = element.parse_factors()
            if(op == '-'):
                number1 = number1 - number2 #conducts what mathematical operation 
            else:
                number1 = number1 + number2 #conducts what mathematical operation 


            """ Check for sign of number """
    def get_sign(element):
        if(element.current_element() == '+'): # If sign is a '+' then return true
            element.i += 1
            return True
        elif (element.current_element() == '-'): # If sign is a '-' then return a false
            element.i += 1
            return False
        return True


    #Ensures all the open parenthesis are met by closed ones
    def parse_atom(element):
        
        element.skip_spaces()

        positive = element.get_sign()

        if(element.current_element() == '('):
            element.i += 1 #add one to total of elements
            element.parenth_count += 1 #add one to count of parenthesis
            res = element.tokenize()

            if(element.current_element() != ')'): #missing parenthesis when the current position of the pointer is not at a closed bracket
                raise TypeError("Missing closing parenthesis")#Exception
                return 0

            element.i += 1
            element.parenth_count -= 1
            return res if positive else -res

        number = element.read_value() #collects a number in the expression if the pointer (element.i) is pointing to one in "expression"
        return number

def calculate(expr): # this is the object of the above class
    ev = Calculator(expr)
    result = ev.tokenize() #calculates the result of the "expression"

    print("")
    print("-----------------------------------")

    if(ev.error is None): # when there has been no error print the expression and result of it
        print("{} = {}".format(expr, result))
    else: # prints an error if there is one
        print("error at pos {}".format(ev.err_pos))
        print(expr)
        for i in range(0, ev.err_pos - 1):
            print("-")
        print("^")
        for i in range(ev.err_pos, len(expr)):
            print("-")
        print("")
        print(ev.error)

    print("-----------------------------------")


expression = input("Enter values with ' before and at end of expression e.g '2+2' or '(9+9)/3' \n")
calculate(expression)

# example of expression: '2+2'
# output will be 4

#-----------------------------------------------------------------------------------------------------------------------------------------------------

