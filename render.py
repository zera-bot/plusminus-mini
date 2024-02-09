import renderformats
import math
from delimiters import functionDelimiters,numbersOfParameters
from tokenizer import tokenize
from copy import deepcopy

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

    return offsetPointList(l,-farthestPointInXDirection,-farthestPointInYDirection)

def isExpressionType(obj):
    a = isinstance(obj,BaseExpression)
    b = isinstance(obj,DelimiterExpression)
    c = isinstance(obj,CombinedExpression)
    if a or b or c: return True
    return False

class BaseExpression: #only store data for expressions
    def __init__(self,value,isSmall=False):
        if value == "": value = "_"
        self.value = value
        self.isSmall = isSmall

        points = []
        characters = [renderformats.smallNumbers[k] for k in [*value]] if isSmall else [renderformats.bigNumbers[k] for k in [*value]] 
        self.height = max([k["height"] for k in characters])
        self.width = sum([k["width"] for k in characters])
        
        horizontalOffset = 0
        for ch in characters:
            points+=offsetPointList(ch["points"],horizontalOffset,0)
            horizontalOffset+=ch["width"]

        self.points = points

    def setSize(self,small:bool):
        return BaseExpression(self.value,small)
    
    def isSmallExpression(self):
        return self.isSmall

class DelimiterExpression:
    def __init__(self,delim,inputs):
        expectedAmount = numbersOfParameters[delim]
        for i in range(expectedAmount-len(inputs)):
            inputs.append(BaseExpression("_"))

        self.delim = delim
        #below should be either of type DelimiterExpression or BaseExpression
        self.inputs = inputs 

        width = 0
        height = 0
        points = []

        if delim == "Frac":
            longestInputSize = max([k.width for k in inputs])+4

            points+=offsetPointList(inputs[0].points,math.floor((longestInputSize-inputs[0].width)/2),0)
            #draw the fraction line (1 pixel tall with 1 pixel spacing)
            fracLinePoints = []
            for i in range(longestInputSize):
                fracLinePoints.append((i,inputs[0].height+1))
            
            points+=fracLinePoints
            points+=offsetPointList(inputs[1].points,math.floor((longestInputSize-inputs[1].width)/2),inputs[0].height+3)

            width = longestInputSize
            height = inputs[0].height + inputs[1].height + 3
        elif delim == "Power":
            self.inputs[1] = self.inputs[1].setSize(True)
            inp0,inp1 = self.inputs[0],self.inputs[1]

            points+=inp0.points
            startingPoint = (inp0.width+2, -math.floor(inp1.height/2)) #for other input
            points+=offsetPointList(inp1.points,startingPoint[0],startingPoint[1])

            width = inp0.width+inp1.width+2
            height = inp0.height+math.floor(inp1.height/2)

            points = alignToBounds(points)
        elif delim == "Mod":
            modSymbol = renderformats.smallNumbers["%"] if self.inputs[0].isSmall else renderformats.bigNumbers["%"]
            offset=0

            height=self.inputs[0].height
            height = max([height,modSymbol["height"]])
            height = max([height,self.inputs[1].height])


            points+=offsetPointList(self.inputs[0].points,0,math.floor((height-self.inputs[0].height)/2))
            offset+=self.inputs[0].width+1

            points+=offsetPointList(modSymbol["points"],offset,math.floor((height-modSymbol["height"])/2))
            offset+=modSymbol["width"]+1
            

            points+=offsetPointList(self.inputs[1].points,offset,math.floor((height-self.inputs[1].height)/2))
            offset+=self.inputs[1].width+1

            width = offset
        elif delim == "Sqrt":
            #number size remains the same
            w=self.inputs[0].width
            h=self.inputs[0].height
            artificialPoints = [] #points making up the radical symbol

            c1 = 2+h-math.floor(h/2)
            #top of radical
            for i in range(3,6+w):
                artificialPoints.append((i,0))
            #top part of radical stem
            for i in range(1,c1):
                artificialPoints.append((3,i))
            #bottom part of radical stem
            for i in range(c1,c1+math.floor(h/2)):
                artificialPoints.append((2,i))
            #radical tail
            artificialPoints.append((0,h-1))
            artificialPoints.append((1,h))

            artificialPoints = offsetPointList(artificialPoints,1,1)
            points+=artificialPoints
            points+=offsetPointList(self.inputs[0].points,6,3)

            width = w+7
            height = h+3
        elif delim == "Paren":
            w = self.inputs[0].width
            h = self.inputs[0].height
            
            smallValue = 2 if self.inputs[0].isSmallExpression() else 4
            height = h
            width = w+smallValue+4

            if smallValue == 2: #if small 
                #opening paren
                points.append((1,0))
                points.append((1,h-1))
                for i in range(1,h-smallValue+1):
                    points.append((0,i))

                #the input
                points+=offsetPointList(self.inputs[0].points,3,0)

                #closing paren
                points.append((w+4,0))
                points.append((w+4,h-1))
                for i in range(1,h-smallValue+1):
                    points.append((w+5,i))
            elif smallValue == 4:
                #opening paren
                points.append((2,0))
                points.append((1,1))
                points.append((1,h-2))
                points.append((2,h-1))
                for i in range(2,h-smallValue+2):
                    points.append((0,i))

                #the input
                points+=offsetPointList(self.inputs[0].points,4,0)

                #closing paren
                points.append((w+5,0))
                points.append((w+6,1))
                points.append((w+6,h-2))
                points.append((w+5,h-1))
                for i in range(2,h-smallValue+2):
                    points.append((w+7,i))

            points=offsetPointList(points,1,1)
            height=height+1
            width=width+1
        elif delim == "Floor":
            w = inputs[0].width
            height = inputs[0].height
            width = w+8

            for i in range(height):
                points.append((0,i))
            points.append((1,height-1))
            points.append((2,height-1))

            points+=offsetPointList(inputs[0].points,4,0)

            for i in range(height):
                points.append((w+7,i))
            points.append((w+6,height-1))
            points.append((w+5,height-1))
        elif delim == "Ceil":
            w = inputs[0].width
            height = inputs[0].height
            width = w+8

            for i in range(height):
                points.append((0,i))
            points.append((1,0))
            points.append((2,0))

            points+=offsetPointList(inputs[0].points,4,0)

            for i in range(height):
                points.append((w+7,i))
            points.append((w+6,0))
            points.append((w+5,0))
        elif delim == "Abs":
            w = inputs[0].width
            height = inputs[0].height
            width = w+4

            for i in range(height):
                points.append((0,i))

            points+=offsetPointList(inputs[0].points,2,0)

            for i in range(height):
                points.append((w+3,i))
        elif delim in functionDelimiters:
            delimName = delim.lower() if delim not in ["W"] else delim
            delimPoints = BaseExpression(delimName,self.isSmallExpression())
            inputExpression = DelimiterExpression("Paren",self.inputs)

            height = max([delimPoints.height,inputExpression.height])
            width = delimPoints.width+inputExpression.width+1 #1 for spacing

            points+=offsetPointList(delimPoints.points,0,math.floor((height-delimPoints.height)/2))
            points+=offsetPointList(inputExpression.points,delimPoints.width+1,math.floor((height-inputExpression.height)/2))
        elif delim == "Choose":
            longestInputSize = max([k.width for k in inputs])+4

            points+=offsetPointList(inputs[0].points,math.floor((longestInputSize-inputs[0].width)/2),0)
            points+=offsetPointList(inputs[1].points,math.floor((longestInputSize-inputs[1].width)/2),inputs[0].height+3)

            width = longestInputSize
            height = inputs[0].height + inputs[1].height + 3

            self.width = width
            self.height = height
            self.points = points

            k = DelimiterExpression("Paren",[CombinedExpression([self])])
            points= k.points
            width = k.width
            height= k.height
        elif delim == "NthRoot":
            points+=self.inputs[0].points

            other = DelimiterExpression("Sqrt",[inputs[1]])
            points+=offsetPointList(other.points,self.inputs[0].width-2,
                                    self.inputs[0].height-6) #not sure about values
            
            width = self.inputs[0].width+other.width-2
            height = other.height+self.inputs[0].height-6
        elif delim == "LogBase":
            self.inputs[0] = self.inputs[0].setSize(True)

            delimPoints = BaseExpression("log",self.isSmallExpression())
            inputExpression = DelimiterExpression("Paren",[self.inputs[1]])
            maxHeight = max([delimPoints.height,inputExpression.height])
            
            height = maxHeight
            if maxHeight < math.floor((maxHeight-delimPoints.height)/2)+math.floor(delimPoints.height/2)+self.inputs[0].height:
                height += math.ceil(delimPoints.height) + self.inputs[0].height + 3 - maxHeight

            miniHeight = math.floor((maxHeight-delimPoints.height)/2)+math.floor(delimPoints.height/2)+3
            height = self.inputs[0].height+miniHeight

            offset=delimPoints.width+1
            points+=offsetPointList(delimPoints.points,0,math.floor((maxHeight-delimPoints.height)/2))
            
            points+=offsetPointList(self.inputs[0].points,offset,math.floor((maxHeight-delimPoints.height)/2)+math.floor(delimPoints.height/2)+3)
            offset+=self.inputs[0].width+1

            points+=offsetPointList(inputExpression.points,offset,math.floor((maxHeight-inputExpression.height)/2))
            offset+=inputExpression.width+1

            width = offset
        elif delim == "Factorial":
            symbol = BaseExpression("!",self.isSmallExpression())
            inputExpression = DelimiterExpression("Paren",self.inputs)
            
            height = max([symbol.height,inputExpression.height])
            width = symbol.width+inputExpression.width+1 #1 for spacing

            points+=offsetPointList(inputExpression.points,0,math.floor((height-inputExpression.height)/2))
            points+=offsetPointList(symbol.points,inputExpression.width+1,math.floor((height-symbol.height)/2))
        elif delim in ["X","Y","Z"]:
            letter = BaseException(delim.lower())
            height = letter.height
            width = letter.width
            points+=letter.points

        self.width = width
        self.height = height
        self.points = points

    def setSize(self,isSmall):
        return DelimiterExpression(self.delim,[k.setSize(isSmall) for k in self.inputs])
    
    def isSmallExpression(self):
        for i in self.inputs:
            if not i.isSmallExpression():
                return False #one big element -> element is of big size
        return True #otherwise, is small

class CombinedExpression:
    def __init__(self,inputs):
        self.inputs = inputs
        points = []

        maxHeight = max([k.height for k in self.inputs])
        hOffset = 0
        for i in inputs:
            points+=offsetPointList(i.points,hOffset,math.floor((maxHeight-i.height)/2))
            hOffset+=i.width+1
        self.height = maxHeight
        self.width = sum([k.width for k in self.inputs])+len(inputs)
        self.points=points

    def setSize(self,isSmall):
        return self
    
    def isSmallExpression(self):
        return False




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
def replacePrincipalVariables(s):
    s = s.replace("[Pi]","P")
    s = s.replace("[i]","i")
    s = s.replace("[E]","E")
    return s

def replacePrincipalVariablesInList(l):
    newL = deepcopy(l)
    for ind,i in enumerate(newL):
        if isinstance(i,list):
            newL[ind] = replacePrincipalVariablesInList(i)
        elif isinstance(i,str):
            newL[ind] = replacePrincipalVariables(i)
    return newL


def generate(expression:str=None,tokens=None):
    if expression:
        expression = replacePrincipalVariables(expression)
        tokens = tokenize(expression)
    else: #inputs are lists (THIS IS SO BAD LOL)
        tokens = replacePrincipalVariablesInList(tokens)

    #combine elements
    def v0(l):
        newL = deepcopy(l)

        currentOther = ""
        firstCurrentOtherIndex = 0

        indicesToDelete = []
        for ind,t in enumerate(newL):
            if t[0] == "OTHER":
                if currentOther == "": firstCurrentOtherIndex = ind
                currentOther += t[1]
            elif t[0] == "DELIM":
                if currentOther != "":
                    #remove the current literal
                    newL[firstCurrentOtherIndex]=currentOther
                    currentOther = ""

                    for i in range(firstCurrentOtherIndex+1,ind):
                        indicesToDelete.append(i)
                    
                #evaluate delimiter
                for jind,j in enumerate(t[2:]):
                    if isinstance(j,list):
                        t[jind+2] = v0(t[jind+2])

        if currentOther != "":
            newL[firstCurrentOtherIndex]=currentOther
            for i in range(firstCurrentOtherIndex+1,len(newL)):
                indicesToDelete.append(i)

        for i in reversed(indicesToDelete):
            try:
                del newL[i]
            except IndexError: pass
        return newL
    
    tokens = v0(tokens)

    #convert all to expressions
    def doItem(l):
        newL = deepcopy(l)
        for ind, i in enumerate(newL):
            if isinstance(i, list) and i[0] == "DELIM":
                updatedList = i.copy()
                for jind,j in enumerate(updatedList[2:]):
                    if isinstance(j,str):
                        updatedList[2+jind]=BaseExpression(j)
                    if isinstance(j,list):
                        updatedList[2+jind]=generate(tokens=j)
                newL[ind] = DelimiterExpression(i[1],updatedList[2:])
            elif isinstance(i,str): # if its a base expression
                newL[ind]=BaseExpression(i)
            elif isinstance(i,list):
                newL[ind]=generate(tokens=i)

        return newL

    tokens = doItem(tokens)
    return CombinedExpression(tokens)
