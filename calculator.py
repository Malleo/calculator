def findNextOpr(txt):
    """
        Takes a string and returns -1 if there is no operator in txt, otherwise returns 
        the position of the leftmost operator. +, -, *, / are all the 4 operators

        >>> findNextOpr('  3*   4 - 5')
        3
        >>> findNextOpr('8   4 - 5')
        6
        >>> findNextOpr('89 4 5')
        -1
    """
    if len(txt)<=0 or not isinstance(txt,str):
        return "type error: findNextOpr"

    # --- YOU CODE STARTS HERE
    for character in txt:
        if ord(character) == 42 or ord(character) == 43 or ord(character) == 45 or ord(character) == 47:
            return txt.index(character)
    return -1
    # ---  CODE ENDS HERE


def isNumber(txt):
    """
        Takes a string and returns True if txt is convertible to float, False otherwise 

        >>> isNumber('1   2 3')
        False
        >>> isNumber('-  156.3')
        False
        >>> isNumber('29.99999999')
        True
        >>> isNumber('    5.9999 ')
        True
    """
    if not isinstance(txt, str):
        return "type error: isNumber"
    if len(txt)==0:
        return False

    # --- YOU CODE STARTS HERE
    txt = txt.strip()      # This takes off the whitespaces at the beginning and end of the string.
    try:
        temp = float(txt)  # If the program is able to do this, it means whatever is left in the string is convertible to float.
        return True        # Therefore, it must be a number.
    except:
        return False
    # ---  CODE ENDS HERE

def getNextNumber(expr, pos):
    """
        expr is a given arithmetic formula of type string
        pos is the start position in expr
          1st returned value = the next number (None if N/A)
          2nd returned value = the next operator (None if N/A)
          3rd returned value = the next operator position (None if N/A)

        >>> getNextNumber('8  +    5    -2',0)
        (8.0, '+', 3)
        >>> getNextNumber('8  +    5    -2',4)
        (5.0, '-', 13)
        >>> getNextNumber('4.5 + 3.15         /   5',0)
        (4.5, '+', 4)
        >>> getNextNumber('4.5 + 3.15         /   5',10)
        (None, '/', 19)
    """

    if len(expr)==0 or not isinstance(expr, str) or pos<0 or pos>=len(expr) or not isinstance(pos, int):
        return None, None, "type error: getNextNumber"
    # --- YOU CODE STARTS HERE
    expr=expr[pos:]  # Since we will be starting from position pos, we won't need to look any earlier in the string, so just remove the beginning.
    nextNumber = None
    nextOprPos = findNextOpr(expr)
    if nextOprPos == -1:  # This occurs when there are no more operators left after position pos.
        nextOpr = None
        nextOprPos = None  # They want getNextNumber to return None instead of -1.
    else:
        nextOpr = expr[nextOprPos]
        if isNumber(expr[0:nextOprPos]):  # Checks to see if the portion of the string before the operator is a number.
            expr = expr[0:nextOprPos]
            expr = expr.strip()  # Remove whitespaces.
            nextNumber = float(expr)  # Now that all spaces are removed, we can successfully convert the remaining string into a float number.
    if nextOprPos == None:  # Even if we ran out of operators, there may still be a number at the end of a string.
            if isNumber(expr[0:]):  # We test if the expression from the starting position pos until the end of the string is a number.
                expr = expr[0:]
                expr = expr.strip()  # Remove whitespaces.
                nextNumber = float(expr)  # If it's a number, then set that end of the string to nextNumber.
    if nextOprPos == None:  # So because I modified expr to equal expr[pos:] I have to factor in pos to the return the correct value of nextOprPos.
        return nextNumber, nextOpr, nextOprPos  # Because you can't add anything to Type None, I just needed another return statement.
    return nextNumber, nextOpr, nextOprPos+pos  # Returns everything. nextOprPos has to factor in the starting position in the string.
    # ---  CODE ENDS HERE

def exeOpr(num1, opr, num2):

    #This function is just an utility function for calculator(expr). It is skipping type check

    if opr=="+":
        return num1+num2
    elif opr=="-":
        return num1-num2
    elif opr=="*":
        return num1*num2
    elif opr=="/":
        return num1/num2
    else:
        return "error in exeOpr"

    
def calculator(expr):
    """
        Takes a string and returns the calculated result if the arithmethic expression is value,
        and error message otherwise 

        >>> calculator("   -4 +3 -2")
        -3.0
        >>> calculator("-4 +3 -2 / 2")
        -2.0
        >>> calculator("-4 +3   - 8 / 2")
        -5.0
        >>> calculator("   -4 +    3   - 8 / 2")
        -5.0
        >>> calculator("23 / 12 - 223 + 5.25 * 4 * 3423")
        71661.91666666667
        >>> calculator("2 - 3*4")
        -10.0
        >>> calculator("4++ 3 +2")
        'error message'
        >>> calculator("4 3 +2")
        'input error line B: calculator'
    """


    if len(expr)<=0 or not isinstance(expr,str): #Line A     
        return "input error line A: calculator"
    
    # Concatenate '0' at he beginning of the expression if it starts with a negative number to get '-' when calling getNextNumber
    # "-2.0 + 3 * 4.0 ” becomes "0-2.0 + 3 * 4.0 ”. 
    expr=expr.strip()
    if expr[0]=="-":
        expr = "0 " + expr
    newNumber, newOpr, oprPos = getNextNumber(expr, 0)

    # Initialization. Holding two modes for operator precedence: "addition" and "multiplication"
    if newNumber is None: #Line B
        return "input error line B: calculator"
    elif newOpr is None:
        return newNumber
    elif newOpr=="+" or newOpr=="-":
        mode="add"
        addResult=newNumber     #value so far in the addition mode
    elif newOpr=="*" or newOpr=="/":
        mode="mul"
        addResult=0
        mulResult=newNumber     #value so far in the multiplication mode
        addLastOpr = "+"
    pos=oprPos+1                #the new current position
    curOpr=newOpr                  #the new current operator
    
    #Calculation starts here, get next number-operator and perform case analysis. Compute values using exeOpr
    while True:
    # --- YOU CODE STARTS HERE
        newNumber, newOpr, oprPos = getNextNumber(expr, pos)
        if newNumber is None and newOpr is not None:  # This means we found an expression before a new number (Two operations next to each other).
            return 'error message'
        if mode == 'mul':  # If we are either multiplying or dividing, we know this is the first priority in order of operations and we can just do the operation.
            mulResult = exeOpr(mulResult,curOpr,newNumber)
            if newOpr == "+" or newOpr == "-" or newOpr is None:       # If the next operator we find is addition or subtraction:
                mode="add"                                             # Switch mode to addition.
                addResult = exeOpr(addResult, addLastOpr, mulResult)   # Performs the previous addition operation.
                mulResult = 0                                          # We're going to eventually be adding everything up, so reset mulResult and keep totals stored in addResult.
                if newOpr is None:                                     # If we have no operators left, we've reached the end of the string and our total is addResult.
                    return addResult
        elif mode == 'add':  # If we are either adding or subtracting, we need to find a way to tell if we can perform the operation yet.
            if newOpr == '*' or newOpr == '/':  # If we are in adding mode, but the next operator is multiplication, we know that we have to switch to multiplication mode.
                mode = 'mul'
                addLastOpr = curOpr  # We need to keep track of what addition or subtraction operation we will need to perform in the future, so store the plus or minus sign within addLastOpr.
                mulResult = newNumber  # Keep track of the current number that we will be multiplying with.
            elif newOpr == '+' or newOpr == '-' or newOpr is None:  # If we have addition right before addition again, that means we can perform the operation.
                addResult = exeOpr(addResult, curOpr, newNumber)
                if newOpr is None:  # If we ran out of operators, we've reached the end of the string and gotten our total.
                    return addResult
        pos=oprPos+1  # Update the position as it goes through the expression linearly.
        curOpr=newOpr  # Update the current operator.
    # ---  CODE ENDS HERE
