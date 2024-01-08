import xmath, re, copy

from comp import NumericalComponent
from fractions import Fraction
from delimiters import lambdas

#s = "123+[Frac]<3,[Frac]<[Frac]<6+4,1>,7>>+4323" #string
#s = "3+-1.5"


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
        for jind, j in enumerate(l):
            if isinstance(j,list):
                k = findFirstNestedElement(j)
                if k: return k

            try:
                if "[" in j: return l, jind
            except TypeError:
                continue
    return None


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
    s = s.replace("[Pi]", "p")
    s = s.replace("[E]", "e")
    s = s.replace("[i]", "i")

    s = s.replace("[X]", "[X]< >")
    s = s.replace("[Y]", "[Y]< >")
    s = s.replace("[Z]", "[Z]< >")

    #s = s.replace("*-", "*NumericalComponent(Fraction(\"-1,1\"))*")
    #s = s.replace("/-", "*NumericalComponent(Fraction(\"-1,1\"))/")
    #s = s.replace("+-", "-")
    main = miniTokenizeMain(s)

    #Now we will move through each nested delimiter and add them to the nests dictionary.
    while True:
        if findFirstNestedElement(main) == None: break
        n, nind = findFirstNestedElement(main)
        nestedToken = miniTokenizeMain(n[nind])
        n[nind] = nestedToken

    #combine numbers that have been separated into characters back together
    for ind, i in enumerate(main):
        if i[0] == "OTHER" and len(re.findall(r"[\+\-\*\/()~]", i[1])) == 0:
            currentLiteral = ""
            endingInd = ind

            while endingInd < len(
                    main) and main[endingInd][0] == "OTHER" and len(
                        re.findall(r"[\+\-\*\/()~]", main[endingInd][1])) == 0:
                currentLiteral += main[endingInd][1]
                endingInd += 1

            for _ in range(ind + 1, endingInd):
                try:
                    del main[ind + 1]
                except:
                    pass

            main[ind][1] = currentLiteral
            #do the funny

    return main


#main parsing

def parseSmallStatements(s: str):
    """
    !WARNING! Uses eval().
    """
    literals = re.split(r"[\+\-\*\/()]", s)
    operators = re.findall(r"[\+\-\*\/()]", s)

    evalString = ""

    for ind, i in enumerate(literals):
        n = i.replace("i", "")
        if i == "i": n = "1"
        if "i" in i:  #imaginary number
            evalString += "NumericalComponent(imaginary=Fraction(" + n + "))"
        elif "p" in i:  #pi multiple
            n = i.replace("p", "")
            if i == "p": n = "1"
            evalString += "NumericalComponent(pi_multiple=Fraction(" + n + "))"
        elif "e" in i:
            n = i.replace("e", "")
            if i == "e": n = "1"
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


def parse(main):
    parsedMain = copy.deepcopy(main)

    for ind, i in enumerate(parsedMain):
        #parse all small statements first
        if i[0] == "OTHER" and len(re.findall(r"[\+\-\*\/()]", i[1])) == 0:
            parsedMain[ind] = parseSmallStatements(i[1])
        elif i[0] == "DELIM":
            for j in range(2, len(i)):
                if isinstance(i[j], str):
                    i[j] = parseSmallStatements(i[j])
                elif isinstance(i[j], list):
                    i[j] = parse(i[j])
    
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
            sqrt_components = "[" 
            for k in i.sqrt_components:
                sqrt_components+=f"[Fraction(\"{str(k[0])}/1\"),Fraction(\"{str(k[1])}/1\")]"
            sqrt_components+="]"

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

def tortureTest():
    l = [
         r"[Power]<2,[Power]<2,2>>",
         r"[Frac]<[acos]<1>+[Frac]<3,1>,[Ln]<4>>",
         r"[Sqrt]<1+[Sqrt]<1+[Sqrt]<1+[Sqrt]<1+1>>>>",
         r"[Frac]<[Frac]<5,4>,[Frac]<6,4>+[Frac]<1,3>>",
         r"[NthRoot]<4,[Power]<2,[Power]<2,2>>>",
         r"3*-4",
         r"3.5/-3",
         r"[Paren]<4>/0.5",
         r"[Sqrt]<3>+[Sqrt]<9>",
         r"2[Sqrt]<3>-[Sqrt]<3>",
         r"[Frac]<7+2[Paren]<4+2>,3>",
         r"[Sqrt]<[Pi]>",
         r"[Paren]<[Frac]<[Frac]<2,3>,4>+[Frac]<5,2>>",
         r"[Choose]<7,[Power]<2,2>+1>",
         r"2+[Pi]",
         r"3",
         r"3+4",
         #complex
         r"[i][Pi]",
         r"[i][Pi][E]"
         r"[Sqrt]<[Power]<[i]+1,[i]>-1>",
         r"[Sqrt]<[Power]<[i],2>+[Power]<1,2>>",
         r"[NthRoot]<[Frac]<3,4>+[E],[Frac]<2[i],3>>",
         r"[Ln]<[Frac]<2,[Frac]<3,[sin]<5>+3>>-[sin]<3>>",
         r"[Frac]<[LogBase]<[Frac]<[Frac]<2+[Frac]<3,2>,5>,3>,[Frac]<3,[Frac]<1,2>>>,17>",
         r"[Frac]<[LogBase]<[Frac]<[Frac]<2+[Frac]<3,2>,2+[Frac]<3,2*2+[cos]<4>+3>>,3>,[Frac]<3,[Frac]<1,1+[acos]<1>>>>,17>",
         r"[Power]<[E],[i][Pi]>+1"
         ]

    for i in l:
        print(str(parse(tokenize(i))))