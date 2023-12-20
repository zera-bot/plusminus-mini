s = "[Frac]<3,[Frac]<6,7>>+4" #string

class NestedElementComponent():
    def __init__(self,index):
        self.index = index

    def __repr__(self):
        return self.index
    
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

miniMain = [ ["DELIM","Frac",3,NestedElementComponent(1)], ["OTHER","+4"] ]
miniNests = {"1":["DELIM","Frac",6,7]}

"""

def findOpenIndex(d:dict):
    n = 0
    while True:
        try:
            k = d[str(n)]
            n+=1
        except: break

def ssB(string,a,b):
    # get a substring between characters a and b of a string
    # a inclusive, b exclusive
    return string[a:b]

def splitStringByNonNestedCommas(s):
    # go through string, if comma is inside brackets, ignore
    # otherwise split with commas
    l = []
    currentLiteral = ""

    bracketList = []
    for ind,c in enumerate([*s]):
        if c == "<": bracketList.append("<")
        elif c == ">": bracketList.append(">")

        if "<" in bracketList and ">" in bracketList:
            bracketList.remove("<")
            bracketList.remove(">")

        if len(bracketList) == 0 and c == ",":
            l.append(currentLiteral)
            currentLiteral = ""
        else:
            currentLiteral+=c

    if currentLiteral != "": l.append(currentLiteral)
    return l



def tokenize(s):
    main = []
    nests = {} #dict containing nested elements

    miniMain = []
    miniNests = {}

    currentLiteral = ""
    indexToSkipTo = -1
    for ind,c in enumerate([*s]):
        if ind < indexToSkipTo: continue

        if c == "[":
            #add current literal to list
            if currentLiteral != "":
                miniMain.append(["OTHER",currentLiteral])
            currentLiteral = ""

            #start parsing delimiter
            startingInd=ind
            pseudoInd = ind
            while s[pseudoInd] != "]": pseudoInd+=1

            delimName = ssB(s,startingInd+1,pseudoInd)

            # find end of delimiter (after all of the delimiter's entries)
            # after we parse this delimiter we will tell the computer to not read
            # until after the already parsed delimiter

            # get start and end of triangle brackets of delimiter (and form substring)
            bracketList = ["<"]
            inputsStartingInd = pseudoInd+1
            inputsEndingInd = pseudoInd+1
            while len(bracketList) != 0:
                inputsEndingInd+=1
                if s[inputsEndingInd] == "<": bracketList.append("<")
                elif s[inputsEndingInd] == ">": bracketList.append(">")

                if "<" in bracketList and ">" in bracketList:
                    bracketList.remove("<")
                    bracketList.remove(">")
            
            #delimiterInputsString is the stuff inside the triangle brackets
            delmiterInputsString = ssB(s,inputsStartingInd+1,inputsEndingInd)

            miniMain.append(["DELIM",delimName,*splitStringByNonNestedCommas(delmiterInputsString)])
            indexToSkipTo=inputsEndingInd+1
        else:
            currentLiteral+=c

    # add current literal to end of list just in case there is a literal at the end
    if currentLiteral != "":
        miniMain.append(["OTHER",currentLiteral])
    currentLiteral = ""

    print(miniMain)

            









print(tokenize(s))

