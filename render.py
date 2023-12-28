import renderformats
import math
from delimiters import functionDelimiters
from tokenizer import tokenize,NestedElementComponent
from copy import deepcopy

from PIL import Image,ImageDraw

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

class BaseExpression: #only store data for expressions
    def __init__(self,value,isSmall=False):
        #value is the given tokenized list.
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
            height = h+2
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




        # IDEA: for delimiters using words like sin,
        # instead of inserting points from the raw table
        # use the BaseExpression class and get the list of points from there
        # as it will do all the hard work





        self.width = width
        self.height = height
        self.points = points
        # CALCULATE ALL POINTS IN THIS EXPRESSION SO IT CAN BE TREATED AS ITS OWN
        # EXPRESSION INSTEAD OF RELYING ON POINTERS TO THE REAL EXPRESSIONS

    #this doesnt work but do this later
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
    s = s.replace("[Pi]","p")
    s = s.replace("[i]","i")
    s = s.replace("[E]","e")
    return s

def generate(expression:str=None,tokens=None,nestedTokens=None):
    if expression:
        expression = replacePrincipalVariables(expression)
        tokens,nestedTokens = tokenize(expression)
    else: #inputs are lists (THIS IS SO BAD LOL)
        for ind,i in enumerate(tokens):
            #if i:
            for jind,j in enumerate(i):
                if isinstance(i,str):
                    r = tokens[ind][jind]
                    tokens[ind][jind]=replacePrincipalVariables(r)
        for k,v in nestedTokens.items():
            if not isinstance(v,list): continue
            for ind,i in enumerate(v):
                if isinstance(i,str):
                    nestedTokens[k][ind]=replacePrincipalVariables(nestedTokens[k][ind])
                elif isinstance(i,list):
                     for jind,j in enumerate(i):
                        if isinstance(i,str):
                            nestedTokens[k][ind][jind]=replacePrincipalVariables(nestedTokens[k][ind][jind])


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

    #important step
    for k, v in nestedTokens.items():
        if not isinstance(v,list): continue
        if not isinstance(v[0],list): continue
        if isinstance(v,list): # very important
            #newParsedNests = {}
            #get all parsed nests values that it uses
            #for i in v:
            #    if isinstance(i,NestedElementComponent):
            #        key = i.index
            #        newParsedNests[str(i)] = nestedTokens[str(i)]

            newParsedNests = deepcopy(nestedTokens)
            #get all parsed nests values that it uses
            del newParsedNests[k]

            nestedTokens[k]=generate(tokens=v,nestedTokens=newParsedNests)

    #now start
    
    nestsWithoutNestedElements = []
    nestsWithNestedElements = []

    for k, v in nestedTokens.items():
        if not isinstance(v,list): continue
        if v[0] == "DELIM":
            containsNestedElements = False
            for j in v:
                if isinstance(j, NestedElementComponent):
                    nestsWithNestedElements.append((k, v))
                    containsNestedElements = True
                    break
            if not containsNestedElements:
                nestsWithoutNestedElements.append((k, v))

    # then, create a base expresion for
    # all delimiters in the parsedNests list that DON'T have a
    # NestedElementComponent item in one of their inputs
    if len(nestedTokens) > 0:
        for key, v in nestsWithoutNestedElements: #for each delim
            updatedList = v.copy()
            for ind,i in enumerate(updatedList[2:]):
                updatedList[2+ind]=BaseExpression(i)

            nestedTokens[key] = DelimiterExpression(v[1],updatedList[2:])

    # then, evaluate all delimiters in the parsedNests list that DO have a
    # NestedElementComponent item in one of their inputs (in reversed order)
    if len(nestsWithNestedElements) > 0:
        for key, v in reversed(nestsWithNestedElements):
            for cind, component in enumerate(v[2:]):
                if isinstance(component, NestedElementComponent):
                    v[cind + 2] = nestedTokens[component.index]

            updatedList=v.copy()
            for ind,i in enumerate(updatedList[2:]):
                if isinstance(i,str):
                    updatedList[2+ind]=BaseExpression(i)

            nestedTokens[key] = DelimiterExpression(v[1],updatedList[2:])

    # then, replace all NestedElementComponent in the parsedMain list with the
    # evaluated ones
    for i in tokens:
        if not isinstance(i, list): continue
        for cind, component in enumerate(i[2:]):
            if isinstance(component, NestedElementComponent):
                i[cind + 2] = nestedTokens[component.index]

    #do main list
    for ind, i in enumerate(tokens):
        if isinstance(i, list) and i[0] == "DELIM":
            updatedList = i.copy()
            for jind,j in enumerate(updatedList[2:]):
                if isinstance(j,str):
                    updatedList[2+jind]=BaseExpression(j)

            tokens[ind] = DelimiterExpression(i[1],updatedList[2:])
        elif isinstance(i,str): # if its still a base expression
            tokens[ind]=BaseExpression(i)

    return CombinedExpression(tokens)
    print(tokens,nestedTokens)

#drawing and testing (may be removed later)
def drawExpression(expression,size,path="image.png"):
    if not (isinstance(expression,BaseExpression) or isinstance(expression,DelimiterExpression) or isinstance(expression,CombinedExpression)):
        raise TypeError
    img = Image.new("RGB",size,(255,255,255,255))
    draw = ImageDraw.Draw(img)

    for point in expression.points:
        draw.point(point,(0,0,0,255))

    img.save(path)

def tortureTest():
    l = [r"[Power]<a,2>[Power]<c,2>",
         r"[Frac]<a+[Power]<a,2>,l+1>",
         r"[Frac]<a,c/2>",
         r"a+[Frac]<1,a+[Frac]<1,a+[Frac]<1,a>>>",
         r"[Sqrt]<1+[Sqrt]<1+[Sqrt]<1+[Sqrt]<1+a>>>>",
         r"[Paren]<[Frac]<[Power]<d,2>,d[Power]<a,2>>+[Frac]<[Power]<d,2>,d[Power]<a,2>>>",
         r"[Choose]<7,[Power]<2,2>+1>",
         r"[Choose]<d,2>[Power]<a,2>[Power]<c,d-2>-[Frac]<1,1-a>[Frac]<1,1-[Power]<a,2>>",

         #unofficial
         "123[Frac]<3,[Frac]<[Frac]<6+4,1>,7>>+4323i",
         "[Frac]<3,[Power]<7,4>>",
         "[Frac]<3,[Sqrt]<[Frac]<3,[Power]<7,4>>>>",
         "[Paren]<[Power]<7,4>>",
         "[Power]<e,e>",
         "[Mod]<3,[Frac]<4,5>>",
         "[Abs]<[Floor]<[Ceil]<[Frac]<4,5>>>>",
         "[Frac]<[acos]<3>+3[cos]<[Frac]<4,5>>,[Ln]<4>>",
         "[Sqrt]<[Power]<i+1,i>-1>",
         "[Paren]<[Frac]<[Frac]<2,3>,4>+[Frac]<5,2>>",
         "[NthRoot]<2,2i>",
         "[NthRoot]<[Frac]<3,4>+e,[Frac]<2i,3>>",
         ]
    
    for ind,m in enumerate(l):
        array = generate(m)
        drawExpression(array,(128,64),f"tortureTest/{str(ind+1)}.png")

#mozilla torture test + other (current implementation)
tortureTest()