import copy
import itertools
import random
import sys


def simplify(clauses, symbol):
    global symbols
    global working

    if len(symbol) == 2:
        working.append("Removing every clause containing " + str(symbol) + " and removing every occurrence " + str(symbol[1]))
    else:
        working.append("Removing every clause containing " + str(symbol) + " and removing every occurrence of !" + str(symbol))

    # Removing every clause containing symbol
    # Removing every occurrence of !symbol
    for clause in list(clauses):
        symbolInClause = True
        if symbol in clause:
            clauses.remove(clause)
        else:
            while symbolInClause:
                if len(symbol) == 2:
                    if symbol[1] in clause:
                        clause.remove(symbol[1])
                        if not clause:
                            clauses.remove(clause)
                    else:
                        symbolInClause = False
                else:
                    if '!' + symbol in clause:
                        clause.remove('!' + symbol)
                        if not clause:
                            clauses.remove(clause)
                    else:
                        symbolInClause = False
    merged = list(itertools.chain.from_iterable(clauses))
    symbols = []
    if not clauses and not isinstance(values[symbol], str):
        if len(symbol) == 2:
            values[symbol] = False
            values[symbol[1]] = True
        else:
            values[symbol] = True
            values['!' + symbol] = False
    for symbol in merged:
        if len(symbol) == 2:
            symbol = symbol[1]
        if symbol not in symbols:
            symbols.append(symbol)
    working.append(copy.deepcopy(clauses))

    return clauses


def check(clauses):
    # Returns True if there exists at least one unit clause or there exists at least one pure literal.
    isNegative = False
    isPositive = False

    for clause in clauses:
        if len(clause) == 1:
            return True

    for symbol in symbols:
        for clause in clauses:
            if symbol in clause:
                isPositive = True
            if '!' + symbol in clause:
                isNegative = True
        if (isPositive and not isNegative) or (not isPositive and isNegative):
            return True
        isPositive = False
        isNegative = False

    return False


def DPLL(clauses):
    global symbols, working, values

    # If expression is empty, return True
    if not clauses:
        working.append("Expression is empty")
        return True

    allEmpty = True
    # If expression only contains empty clauses, return False
    for clause in clauses:
        if clause:
            allEmpty = False
            break
    if allEmpty:
        return False

    stop = check(clauses)

    # While there exists some unit clause, or some pure literal
    while stop:
        for symbol in symbols:
            # If {symbol} and {!symbol} both exist, return False
            if [symbol] in clauses and [('!' + symbol)] in clauses:
                working.append(str(symbol) + " and !" + str(symbol) + " in expression")
                return False
            else:
                clauses = simplify(clauses, symbol)

        stop = check(clauses)
    if not clauses:
        working.append("Expression is empty")
        return True

    # Selecting a random literal from the first shortest clause
    shortestClause = min(len(i) for i in clauses)
    for i in range(0, len(clauses)):
        if len(clauses[i]) == shortestClause:
            shortestClause = i
            break
    literal = random.choice(clauses[shortestClause])
    if DPLL(simplify(clauses, literal)):
        if len(literal) == 2:
            values[literal] = True
            values[literal[1]] = False
        else:
            values[literal] = True
            values['!' + literal] = False
        return True
    else:
        for symbol in symbols:
            # If {symbol} and {!symbol} both exist, return False
            if [symbol] in clauses and [('!' + symbol)] in clauses:
                return False

        return DPLL(simplify(clauses, '!' + random.choice(clauses[shortestClause])))


if __name__ == "__main__":

    # Handling input
    expression = ""
    if len(sys.argv) == 2:
        expression = sys.argv[1]
    else:
        print("Enter your expression in Conjunctive Normal Form (CNF):", end=" ")
        expression = input().replace(' ', '')

    # Variable Declaration
    symbols = []
    values = {}
    working = []
    openCount = 0
    closeCount = 0
    empty = True
    remove = []

    # Validation
    for mySymbol in expression:
        if mySymbol not in ['w', 'x', 'y', 'z', '!', '(', ')', ',']:
            print("Input error: unrecognized character (" + mySymbol + ")")
            exit()
        elif mySymbol not in ['!', '(', ')', ','] and mySymbol not in symbols:
            symbols.append(mySymbol)
            values[mySymbol] = False
            values['!' + mySymbol] = True
        if mySymbol == '(':
            openCount += 1
        elif mySymbol == ')':
            closeCount += 1
    if openCount != closeCount:
        print("Input error: Bracket error")
        exit()

    # Get individual clauses
    myClauses = expression.replace(' ', '').replace('(', '').split(')')[:-1]
    for myI in range(0, len(myClauses)):
        if myClauses[myI]:
            empty = False
            myClauses[myI] = myClauses[myI].split(',')
            if len(myClauses[myI]) == 1:
                if len(myClauses[myI][0]) == 1:
                    values[myClauses[myI][0]] = "True"
                    values['!' + myClauses[myI][0]] = "False"
                else:
                    values[myClauses[myI][0][1]] = "False"
                    values['!' + myClauses[myI][0][1]] = "True"
        else:
            remove.append(myClauses[myI])
    for myI in remove:
        myClauses.remove(myI)
    if empty:
        myClauses = []

    working.append(copy.deepcopy(myClauses))
    ans = DPLL(myClauses)
    count = 0
    hasElement = True
    for i in range(0, len(working)):
        if not hasElement:
            i = len(working) - 1
            print(working[i])
            break
        elif type(working[i]) == list:
            for element in working[i]:
                if element:
                    hasElement = True
                    break
                else:
                    hasElement = False

        print(working[i])
        if "in expression" in working[i]:
            break
    print("Therefore:", end=' ')
    if ans:
        print("Expression is satisfiable")
        print("Example truth assignment:")
        for symbol in values.keys():
            if len(symbol) == 1:
                print(symbol + " = " + str(values[symbol]))

    else:
        print("UNSAT")
