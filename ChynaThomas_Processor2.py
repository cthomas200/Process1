#Chyna Thomas

from sympy.logic.boolalg import SOPform, POSform
from sympy.abc import A,B,C,D

def bkmap(table, numVar):
    map = [(0,0), (0,1), (1,1), (1,0)]

    if numVar == 2:
        kmap = [[0,0],[0,0]]

        for inputs, output in table:
            row = inputs[0]
            column = inputs[1]
            kmap[row][column] = output

    elif numVar == 3:
        kmap = [[0]*4 for _ in range(2)]
        for inputs, output in table:
            row = inputs[0]
            pair = (inputs[1],inputs[2])
            column = map.index(pair)
            kmap[row][column] = output

    elif numVar == 4:
        kmap = [[0]*4 for _ in range(4)]

        for inputs, output in table:
            row = map.index((inputs[0],inputs[1]))
            column = map.index((inputs[2],inputs[3]))
            kmap[row][column] = output
    else: 
        return "Kmap not needed"
    return kmap

def validate(table, expr, symbols):
    for inputs, expected in table:
        values = dict(zip(symbols, inputs))
        res = int(bool(expr.subs(values)))

        if res != expected:
            return "Fail"
    return "Pass"

def simpSOP(table, numVar):
    labels = [A, B, C, D]
    symbols = labels[:numVar]

    ones = [findTerms(inputs) for inputs, output in table if output == 1]

    sop = SOPform(symbols, ones)
    
    sop_str = str(sop).replace("~", "`")
    print('Simplified SOP: ', sop_str)

    res = validate(table, sop, symbols)
    print('\nValidation: ', res)

def simpPOS(table, numVar):
    labels = [A, B, C, D]
    symbols = labels[:numVar]

    ones = [findTerms(inputs) for inputs, output in table if output == 1]
    pos = POSform(symbols, ones)

    pos_str = str(pos).replace("~", "`")
    print('Simplified POS: ', pos_str)

    res = validate(table, pos, symbols)
    print('\nValidation: ', res)



def findTerms(inputs):
    return int(''.join(map(str, inputs)), 2)


def sumofprod(table, numVar):
    labels = [chr(65 + i) for i in range(numVar)]
    mins = []
    nums = []

    for inputs, output in table:
        if output == 1:
            term = []
            nums.append(findTerms(inputs))
            for i in range(len(inputs)):
                if inputs[i] == 1:
                    term.append(labels[i])
                else:
                    term.append(f'`{labels[i]}')
            mins.append('(' + ' * '.join(term) + ')')
    print('Min terms: ', nums)
    print('Canonical Equation:')
    if not mins:
        return '0'
    return ' + '.join(mins)



def prodofsum(table, numVar):
    labels = [chr(65 + i) for i in range(numVar)]
    maxs = []
    nums = []

    for inputs, output in table:
        if output == 0:
            term = []
            nums.append(findTerms(inputs))

            for i in range(len(inputs)):
                if inputs[i] == 0:
                    term.append(labels[i])
                else:
                    term.append(f'`{labels[i]}')
            maxs.append('(' + ' + '.join(term) + ')')

    print('Max terms: ', nums)
    print('Canonical Equation:')
    if not maxs:
        return '1'
    return ' * '.join(maxs)

def main():

    numVar = int(input("How many variables (n>=2): "))
    if numVar < 2:
        raise ValueError('Number of variables must be at least 2')
    
    numRows = 2 ** numVar #2^n rows
    table = []

    print(f"Enter {numRows} rows as (ex: '0 0 1') ")
    seen = set() #Set for tracking duplicates
    for n in range(numRows):
        row = input(f'Row {n + 1}: ').split()
        if len(row) != numVar + 1: #Must be # of variables + output
            raise ValueError(f'Each row must have {numVar} inputs and 1 output')

        truthValues = [int(x) for x in row]
        if any(i not in (0,1) for i in truthValues):
            raise ValueError('All values must be either 0 or 1') #Validating values

        inputs = tuple(truthValues[:numVar])
        output = truthValues[numVar]
        if inputs in seen:
            raise ValueError(f'No duplicates: {inputs}') #Check for duplicates
        seen.add(inputs)

        table.append((inputs, output))
    table.sort(key=lambda x: x[0])
    print('--Truth table--\n ') #If no errors it'll print the table
    for row in table:
        print(row)

    print('\n Select: \n' 
    '1. Sum of Product (SOP)\n'
    '2. Product of Sum (POS)')
    converter = int(input('Choose option: ').strip())
    if converter == 1:
        print("\n--Unsimplified--\n")
        print(sumofprod(table, numVar))
        print("\n--Simplified--")
        simpSOP(table, numVar)
    elif converter == 2:
        print("\n--Unsimplified--\n")
        print(prodofsum(table, numVar))
        print("\n--Simplified--")
        simpPOS(table, numVar)
    else:
        print('Invalid input. Please choose 1 or 2.')

    print('\n--K-Map Grouping--')
    print(bkmap(table, numVar))

main()

