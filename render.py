import renderformats
import math
from tokenizer import tokenize,NestedElementComponent
from copy import deepcopy

from PIL import ImageFont

def generateArray(x,y):
    return [0 for _ in range(x*y)]

def pointToIndex(x,y,gridX):
    return (gridX*(y))+x

def offsetPointList(l,offsetX,offsetY):
    returnList = l.copy()
    for ind,i in enumerate(l):
        returnList[ind]=(i[0]+offsetX,i[1]+offsetY)
    return returnList

def alignToBounds(l):
    farthestPointInXDirection = 0
    farthestPointInYDirection = 0
    for p in l:
        if p[0]<farthestPointInXDirection:
            farthestPointInXDirection=p[0]
        if p[1]<farthestPointInYDirection:
            farthestPointInYDirection=p[1]

    return offsetPointList(l,farthestPointInXDirection,farthestPointInYDirection)

class BaseExpression: #only store data for expressions
    def __init__(self,value,isSmall):
        #value is the given tokenized list.
        self.value = value
        self.isSmall = isSmall

        points = []
        characters = [renderformats.smallNumbers[k] for k in [*value]] if isSmall else [renderformats.bigNumbers[k] for k in [*value]] 
        self.height = max([k["height"] for k in characters])
        self.width = sum([k["width"] for k in characters])#+len(characters) possibly for margins
        
        horizontalOffset = 0
        for ch in characters:
            points+=offsetPointList(ch["points"],horizontalOffset,0)
            horizontalOffset+=ch["width"]#+1 for margins possibly

        self.points = points

    def setSize(self,isSmall:bool):
        return BaseExpression(self.value,isSmall)

class DelimiterExpression:
    def __init__(self,delim,inputs):
        self.delim = delim
        #below should be either of type DelimiterExpression or BaseExpression
        self.inputs = inputs 

        width = 0
        height = 0
        points = []

        if delim == "Frac":
            self.inputs = [k.setSize(True) for k in self.inputs]
            longestInputSize = max([k.width for k in inputs])+2

            points+=offsetPointList(inputs[0].points,math.floor((longestInputSize-inputs[0].width)/2),0)
            #draw the fraction line (1 pixel tall with 1 pixel spacing)
            fracLinePoints = []
            for i in range(longestInputSize):
                fracLinePoints.append((i,inputs[0].height+1))

            points+=offsetPointList(inputs[1].points,math.floor((longestInputSize-inputs[1].width)/2),inputs[0].height+3)

            width = longestInputSize
            height = inputs[0].height + inputs[1].height + 3
        if delim == "Power":
            self.inputs[1] = self.inputs[1].setSize(True)
            inp0,inp1 = self.inputs[0],self.inputs[1]

            points+=inp0.points
            startingPoint = (inp0.width+2, -math.floor(inp1.height/2)) #for other input
            points+=offsetPointList(inp1.points,startingPoint[0],startingPoint[1])

            width = inp0.width+inp1.width+2
            height = inp0.height+math.floor(inp1.height/2)

            points = alignToBounds(points)


        self.width = width
        self.height = height
        self.points = points
        # CALCULATE ALL POINTS IN THIS EXPRESSION SO IT CAN BE TREATED AS ITS OWN
        # EXPRESSION INSTEAD OF RELYING ON POINTERS TO THE REAL EXPRESSIONS

        print('calculate dimensions? thats a good question ask google')

    def setSize(self,isSmall):
        return DelimiterExpression(self.delim,[k.setSize(isSmall) for k in self.inputs])


"""
STEP 1:
use the tokenizer to give us a lost of tokens (not evaluated)

Convert any shallow operators back into strings so that the only things 
that are in the token list are delimiters and strings

assign a configuration (of lights to be on) for each element without nests inside 
of the nests list, then do the same for the ones with nested elements (in reverse) 
just like in the parser

STEP 2:
then sort of combine those elements

to represent the width and height of stuff I'll create a 
class designed to calculate and store the components and width/height data
"""
def generate(expression:str,array:list):
    array = deepcopy(array)
    tokens,nestedTokens = tokenize(expression)

    currentOther = ""
    firstCurrentOtherIndex = 0

    indicesToDelete = []
    for ind,t in enumerate(tokens):
        if t[0] == "OTHER":
            if currentOther == "": firstCurrentOtherIndex = ind
            currentOther += t[1]
        elif t[0] == "DELIM":
            if currentOther != "":
                tokens[firstCurrentOtherIndex]=currentOther
                currentOther = ""

                for i in range(firstCurrentOtherIndex+1,ind):
                    indicesToDelete.append(i)
    if currentOther != "":
        tokens[firstCurrentOtherIndex]=currentOther
        for i in range(firstCurrentOtherIndex+1,len(tokens)):
            indicesToDelete.append(i)

    for i in reversed(indicesToDelete):
        try:
            del tokens[i]
        except IndexError:
            pass
    
    nestsWithoutNestedElements = []
    nestsWithNestedElements = []

    for k, v in nestedTokens.items():
        if v[0] == "DELIM":
            containsNestedElements = False
            for j in v:
                if isinstance(j, NestedElementComponent):
                    nestsWithNestedElements.append((k, v))
                    containsNestedElements = True
                    break
            if not containsNestedElements:
                nestsWithoutNestedElements.append((k, v))

    
    print(tokens,nestedTokens)
        



array = generateArray(128,64)
s = "123[Frac]<3,[Frac]<[Frac]<6+4,1>,7>>+4323i" #string

print(generate(s,array))