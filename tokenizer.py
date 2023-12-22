import xmath, re, copy

from comp import NumericalComponent
from fractions import Fraction
from delimiters import lambdas

#s = "123+[Frac]<3,[Frac]<[Frac]<6+4,1>,7>>+4323" #string
s = "-1"


class NestedElementComponent():

    def __init__(self, index):
        self.index = index

    def __repr__(self):
        return "Nested Component " + str(self.index)

    def __int__(self):
        return self.index


"""
Tokenizer should take a string and transform it into a list or two of tokens.
For the s example, it should yield something like

List 1 (main list)
[ ("DELIM","Frac",3,NestedElementComponent(1)), ("OPERATOR","+"), ("LITERAL",4) ]

List 2 (dictionary containing only nested elements)
{"1":[("DELIM","Frac",6,7)]}

"""

#make sure that if a number is next to a variable it is multiplied
#(include implied multiplication)
"""
Tokenizer:

Mini-tokenize a list of each delimiter by converting the delimiters to a 
list like such:
[ ["DELIM","Frac","3","[Frac]<6,7>"], ["OTHER","+4"] ]

Then, use a while loop to detect any nested elements and add them to a mini-tokenized
dictionary.
The end result should be as such:

main = [ ["DELIM","Frac",3,NestedElementComponent(1)], ["OTHER","+4"] ]
nests = {"1":["DELIM","Frac",6,7]}

"""


def findOpenIndex(d: dict):
    n = 0
    while True:
        try:
            k = d[str(n)]
            n += 1
        except:
            break
    return str(n)


def ssB(string, a, b):
    # get a substring between characters a and b of a string
    # a inclusive, b exclusive
    return string[a:b]


def splitStringByNonNestedCommas(s):
    # go through string, if comma is inside brackets, ignore
    # otherwise split with commas
    l = []
    currentLiteral = ""

    bracketList = []
    for c in [*s]:
        if c == "<": bracketList.append("<")
        elif c == ">": bracketList.append(">")

        if "<" in bracketList and ">" in bracketList:
            bracketList.remove("<")
            bracketList.remove(">")

        if len(bracketList) == 0 and c == ",":
            l.append(currentLiteral)
            currentLiteral = ""
        else:
            currentLiteral += c

    if currentLiteral != "": l.append(currentLiteral)
    return l


"""
Exploring a nested list and pulling an element (no need to generate an ID because lists point to a
reference in memory)
"""


def findFirstNestedElement(l):
    if isinstance(l, list):
        for i in l:
            for jind, j in enumerate(i):
                try:
                    if "[" in j: return i, jind
                except TypeError:
                    continue
    elif isinstance(l, dict):
        for k, v in l.items():
            for ind, i in enumerate(v):
                for jind, j in enumerate(i):
                    try:
                        if "[" in j: return i, jind
                    except TypeError:
                        continue


def miniTokenizeMain(s: str):
    main = []

    currentLiteral = ""
    indexToSkipTo = -1
    for ind, c in enumerate([*s]):
        if ind < indexToSkipTo: continue

        if c == "[":
            #add current literal to list
            if currentLiteral != "":
                main.append(["OTHER", currentLiteral])
            currentLiteral = ""

            #start parsing delimiter
            startingInd = ind
            pseudoInd = ind
            while s[pseudoInd] != "]":
                pseudoInd += 1

            delimName = ssB(s, startingInd + 1, pseudoInd)

            # find end of delimiter (after all of the delimiter's entries)
            # after we parse this delimiter we will tell the computer to not read
            # until after the already parsed delimiter

            # get start and end of triangle brackets of delimiter (and form substring)
            bracketList = ["<"]
            inputsStartingInd = pseudoInd + 1
            inputsEndingInd = pseudoInd + 1
            while len(bracketList) != 0:
                inputsEndingInd += 1
                if s[inputsEndingInd] == "<": bracketList.append("<")
                elif s[inputsEndingInd] == ">": bracketList.append(">")

                if "<" in bracketList and ">" in bracketList:
                    bracketList.remove("<")
                    bracketList.remove(">")

            #delimiterInputsString is the stuff inside the triangle brackets
            delmiterInputsString = ssB(s, inputsStartingInd + 1,
                                       inputsEndingInd)

            main.append([
                "DELIM", delimName,
                *splitStringByNonNestedCommas(delmiterInputsString)
            ])
            indexToSkipTo = inputsEndingInd + 1
        else:
            currentLiteral += c

        if currentLiteral != "":
            main.append(["OTHER", currentLiteral])
        currentLiteral = ""

    return main


def tokenize(s):
    s = s.replace(")(",")*(")
    s = s.replace("][","]*[")
    
    s = s.replace(" ", "")
    s = s.replace("[Pi]", "~pi")
    s = s.replace("[E]", "~e")
    s = s.replace("[i]", "~i")

    s = s.replace("[X]", "[X]< >")
    s = s.replace("[Y]", "[Y]< >")
    s = s.replace("[Z]", "[Z]< >")

    s = s.replace("*-", "*NumericalComponent(Fraction(\"-1,1\"))*")
    s = s.replace("/-", "*NumericalComponent(Fraction(\"-1,1\"))/")
    s = s.replace("+-", "-")

    main = []
    nests = {}  #dict containing nested elements

    main = miniTokenizeMain(s)

    #Now we will move through each nested delimiter and add them to the nests dictionary.
    while True:
        if findFirstNestedElement(main) == None: break
        n, nind = findFirstNestedElement(main)

        availableDictionaryNum = findOpenIndex(nests)
        nestedToken = miniTokenizeMain(n[nind])

        n[nind] = NestedElementComponent(availableDictionaryNum)
        nests[availableDictionaryNum] = nestedToken

    #Do the same with nests.
    while True:
        if findFirstNestedElement(nests) == None: break
        n, nind = findFirstNestedElement(nests)

        availableDictionaryNum = findOpenIndex(nests)
        nestedToken = miniTokenizeMain(n[nind])

        n[nind] = NestedElementComponent(availableDictionaryNum)
        nests[availableDictionaryNum] = nestedToken

    #combine numbers that have been separated into characters back together
    for ind, i in enumerate(main):
        if i[0] == "OTHER" and len(re.findall(r"[\+\-\*\/()]", i[1])) == 0:
            currentLiteral = ""
            endingInd = ind

            while endingInd < len(
                    main) and main[endingInd][0] == "OTHER" and len(
                        re.findall(r"[\+\-\*\/()]", main[endingInd][1])) == 0:
                currentLiteral += main[endingInd][1]
                endingInd += 1

            for _ in range(ind + 1, endingInd):
                try:
                    del main[ind + 1]
                except:
                    pass

            main[ind][1] = currentLiteral
            #do the funny

    #un-nest the lists in the nested item dict
    for k, v in nests.items():
        nests[k] = v[0]

    return main, nests


#main parsing


def convertStringToLiteral(s: str):
    if "~i" in s:  #imaginary number
        return NumericalComponent(imaginary=Fraction(s.replace("~i", "")))
    elif "~pi" in s:  #pi multiple
        return NumericalComponent(pi_multiple=Fraction(s.replace("~pi", "")))
    elif "~e" in s:
        return NumericalComponent(Fraction(s.replace("~e", "")) * xmath.e)
    else:
        return NumericalComponent(Fraction(s))


def parseSmallStatements(s: str):
    """
    !WARNING! Uses eval().
    """
    literals = re.split(r"[\+\-\*\/()]", s)
    operators = re.findall(r"[\+\-\*\/()]", s)

    evalString = ""

    for ind, i in enumerate(literals):
        n = i.replace("~i", "")
        if i == "~i": n = "1"
        if "~i" in i:  #imaginary number
            evalString += "NumericalComponent(imaginary=Fraction(" + n + "))"
        elif "~pi" in i:  #pi multiple
            n = i.replace("~pi", "")
            if i == "~pi": n = "1"
            evalString += "NumericalComponent(pi_multiple=Fraction(" + n + "))"
        elif "~e" in i:
            n = i.replace("~e", "")
            if i == "~e": n = "1"
            evalString += "NumericalComponent(Fraction(" +n+ ")*xmath.e)"
        else:
            evalString += "NumericalComponent(Fraction(" + i + "))"

        if ind != len(literals) - 1:
            evalString += operators[ind]

    return eval(evalString)


"""
Parsing a tokenized output:

There will be a function for parsing small statements like "3+4-5" and a function for
parsing things like delimiters.

Delimiters will be parsed at the base level by the parse function.
"""


def parse(main, nests):
    parsedMain = copy.deepcopy(main)
    parsedNests = copy.deepcopy(nests)

    for ind, i in enumerate(parsedMain):
        #parse all small statements first
        if i[0] == "OTHER" and len(re.findall(r"[\+\-\*\/()]", i[1])) == 0:
            parsedMain[ind] = parseSmallStatements(i[1])
        elif i[0] == "DELIM":
            for j in range(2, len(i)):
                if isinstance(i[j], str):
                    i[j] = parseSmallStatements(i[j])

    #do the same for parsedNests
    #all delims
    for k, v in parsedNests.items():
        for j in range(2, len(v)):
            if isinstance(v[j], str):
                v[j] = parseSmallStatements(v[j])

    nestsWithoutNestedElements = []
    nestsWithNestedElements = []

    for k, v in parsedNests.items():
        if v[0] == "DELIM":
            containsNestedElements = False
            for j in v:
                if isinstance(j, NestedElementComponent):
                    nestsWithNestedElements.append((k, v))
                    containsNestedElements = True
                    break
            if not containsNestedElements:
                nestsWithoutNestedElements.append((k, v))

    # then, evaluate all delimiters in the parsedNests list that DON'T have a
    # NestedElementComponent item in one of their inputs
    if len(parsedNests) > 0:
        for key, v in nestsWithoutNestedElements:
            name = v[1]
            value = lambdas[name](*v[2:])
            parsedNests[key] = value

    # then, evaluate all delimiters in the parsedNests list that DO have a
    # NestedElementComponent item in one of their inputs (in reversed order)
    if len(nestsWithNestedElements) > 0:
        for key, v in reversed(nestsWithNestedElements):
            for cind, component in enumerate(v[2:]):
                if isinstance(component, NestedElementComponent):
                    #print(parsedNests[key][cind+2])
                    v[cind + 2] = parsedNests[component.index]

            name = v[1]
            value = lambdas[name](*v[2:])
            parsedNests[key] = value

    # then, replace all NestedElementComponent in the parsedMain list with the
    # evaluated ones
    for i in parsedMain:
        if not isinstance(i, list): continue
        for cind, component in enumerate(i[2:]):
            if isinstance(component, NestedElementComponent):
                i[cind + 2] = parsedNests[component.index]

    # then, evaluate all delimiters in the parsedMain list
    for ind, i in enumerate(parsedMain):
        if isinstance(i, list) and i[0] == "DELIM":
            name = i[1]
            value = lambdas[name](*i[2:])
            parsedMain[ind] = value

    # finally use the operators (+ - * /) to parse the expression using eval()
    finalString = ""
    for ind, i in enumerate(parsedMain):
        #implied multiplication part 1
        if isinstance(i, NumericalComponent):
            if ind - 1 >= 0:
                if isinstance(parsedMain[ind - 1], list) and parsedMain[ind-1][1] == ")":
                    finalString += "*"
            
            real = "Fraction(\"" + str(i.real.numerator) + "/" + str(
                i.real.denominator) + "\")"
            imag = "Fraction(\"" + str(i.imaginary.numerator) + "/" + str(
                i.imaginary.denominator) + "\")"
            pi_mul = "Fraction(\"" + str(i.pi_multiple.numerator) + "/" + str(
                i.pi_multiple.denominator) + "\")"
            sqrt_components = str([[
                "Fraction(\"" + str(k[0]) + "/" + str(k[0]) + ")",
                "Fraction(" + str(k[1]) + "/" + str(k[1]) + "\")"
            ] for k in i.sqrt_components])

            num = "NumericalComponent(real=" + real + ",imaginary=" + imag + ",pi_multiple=" + pi_mul + ",sqrt_components=" + sqrt_components + ")"
            finalString += num

            #implied multiplication
            if ind + 1 < len(parsedMain):
                if isinstance(parsedMain[ind + 1], NumericalComponent):
                    finalString += "*"
                if isinstance(parsedMain[ind + 1],list) and parsedMain[ind + 1][1] == "(":
                    finalString += "*"
        elif isinstance(i, list):  #operator
            finalString += i[1]

    return eval(finalString)


print(parse(*tokenize(s)))
