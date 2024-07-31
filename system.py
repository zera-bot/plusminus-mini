import mathcode
import render
import delimiters
import tokenizer
import methods
import renderformats
from comp import NumericalComponent, DecimalRepresentation
from render import CombinedExpression,BaseExpression
from copy import deepcopy

menuScreenPoints = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 11), 
                    (1, 12), (1, 13), (1, 14), (1, 15), (1, 16), (1, 17), (1, 18), (1, 19), (2, 1), (2, 9), 
                    (2, 11), (2, 19), (3, 1), (3, 9), (3, 11), (3, 19), (4, 1), (4, 4), (4, 7), (4, 9), 
                    (4, 11), (4, 13), (4, 16), (4, 17), (4, 19), (5, 1), (5, 3), (5, 4), (5, 5), (5, 6), 
                    (5, 7), (5, 9), (5, 11), (5, 13), (5, 15), (5, 17), (5, 19), (6, 1), (6, 7), (6, 9), 
                    (6, 11), (6, 14), (6, 17), (6, 19), (7, 1), (7, 9), (7, 11), (7, 19), (8, 1), (8, 9), 
                    (8, 11), (8, 19), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), 
                    (9, 9), (9, 11), (9, 12), (9, 13), (9, 14), (9, 15), (9, 16), (9, 17), (9, 18), 
                    (9, 19), (11, 3), (11, 4), (11, 5), (11, 6), (11, 7), (11, 13), (11, 14), (11, 17), 
                    (12, 2), (12, 8), (12, 12), (12, 15), (12, 18), (13, 2), (13, 8), (13, 12), (13, 15), 
                    (13, 18), (14, 2), (14, 8), (14, 12), (14, 15), (14, 18), (15, 3), (15, 7), (15, 13), 
                    (15, 16), (15, 17), (17, 3), (17, 4), (17, 5), (17, 6), (17, 7), (17, 13), (17, 14), 
                    (17, 15), (17, 16), (17, 17), (18, 2), (18, 8), (18, 12), (18, 18), (19, 2), (19, 8), 
                    (19, 12), (19, 18), (20, 2), (20, 8), (20, 12), (20, 18), (21, 3), (21, 4), (21, 5), 
                    (21, 6), (21, 7), (21, 13), (21, 14), (21, 15), (21, 16), (21, 17), (23, 2), (23, 3), 
                    (23, 4), (23, 5), (23, 6), (23, 7), (23, 8), (23, 12), (23, 13), (23, 14), (23, 15), 
                    (23, 16), (23, 17), (23, 18), (24, 3), (24, 18), (25, 4), (25, 18), (26, 3), (26, 18), 
                    (27, 2), (27, 3), (27, 4), (27, 5), (27, 6), (27, 7), (27, 8), (27, 18), (29, 2), 
                    (29, 3), (29, 4), (29, 5), (29, 6), (29, 7), (29, 8), (29, 12), (29, 13), (29, 14), 
                    (30, 2), (30, 5), (30, 15), (30, 16), (31, 2), (31, 5), (31, 17), (31, 18), (32, 2), 
                    (32, 5), (32, 15), (32, 16), (33, 3), (33, 4), (33, 12), (33, 13), (33, 14), (35, 12), 
                    (35, 13), (35, 14), (35, 15), (35, 16), (35, 17), (35, 18), (36, 12), (36, 15), 
                    (36, 18), (37, 12), (37, 15), (37, 18), (38, 12), (38, 15), (38, 18)]
closingScreenPoints = [(36, 22), (36, 23), (36, 24), (36, 25), (36, 26), (36, 27), (36, 28), (36, 29), 
                       (37, 22), (37, 29), (38, 22), (38, 29), (39, 22), (39, 29), (40, 22), (40, 29), 
                       (41, 22), (41, 29), (42, 22), (42, 29), (43, 22), (43, 29), (44, 22), (44, 29), 
                       (45, 22), (45, 29), (46, 12), (46, 13), (46, 14), (46, 15), (46, 16), (46, 17), 
                       (46, 18), (46, 19), (46, 20), (46, 21), (46, 22), (46, 29), (46, 30), (46, 31), 
                       (46, 32), (46, 33), (46, 34), (46, 35), (46, 36), (46, 37), (46, 38), (46, 39), 
                       (47, 12), (47, 39), (48, 12), (48, 39), (49, 12), (49, 39), (50, 12), (50, 39), 
                       (50, 41), (50, 42), (50, 61), (51, 12), (51, 39), (51, 43), (51, 54), (51, 55), 
                       (51, 56), (51, 57), (51, 58), (51, 59), (51, 60), (52, 12), (52, 39), (52, 44), 
                       (52, 48), (52, 49), (52, 50), (52, 51), (52, 52), (52, 53), (52, 59), (53, 12), 
                       (53, 13), (53, 14), (53, 15), (53, 16), (53, 17), (53, 18), (53, 19), (53, 20), 
                       (53, 21), (53, 22), (53, 29), (53, 30), (53, 31), (53, 32), (53, 33), (53, 34), 
                       (53, 35), (53, 36), (53, 37), (53, 38), (53, 39), (53, 45), (53, 46), (53, 47), 
                       (53, 58), (54, 22), (54, 29), (54, 57), (55, 19), (55, 22), (55, 29), (55, 56), 
                       (56, 18), (56, 22), (56, 29), (56, 55), (57, 18), (57, 22), (57, 29), (57, 54), 
                       (58, 17), (58, 22), (58, 29), (58, 53), (59, 17), (59, 22), (59, 29), (59, 52), 
                       (60, 17), (60, 22), (60, 29), (60, 51), (61, 16), (61, 22), (61, 29), (61, 50), 
                       (62, 16), (62, 22), (62, 29), (62, 49), (63, 16), (63, 22), (63, 23), (63, 24), 
                       (63, 25), (63, 26), (63, 27), (63, 28), (63, 29), (63, 49), (64, 16), (64, 49), 
                       (65, 16), (65, 38), (65, 39), (65, 40), (65, 41), (65, 42), (65, 43), (65, 44), 
                       (65, 45), (65, 49), (66, 16), (66, 38), (66, 45), (66, 49), (67, 15), (67, 38), 
                       (67, 45), (67, 49), (68, 14), (68, 38), (68, 45), (68, 48), (69, 13), (69, 38), 
                       (69, 45), (69, 48), (70, 12), (70, 38), (70, 45), (70, 48), (71, 11), (71, 38), 
                       (71, 45), (71, 47), (72, 10), (72, 38), (72, 45), (72, 47), (73, 9), (73, 38), 
                       (73, 45), (74, 7), (74, 8), (74, 38), (74, 45), (75, 6), (75, 17), (75, 18), 
                       (75, 19), (75, 20), (75, 21), (75, 38), (75, 45), (76, 5), (76, 12), (76, 13), 
                       (76, 14), (76, 15), (76, 16), (76, 22), (76, 38), (76, 45), (77, 4), (77, 5), 
                       (77, 6), (77, 7), (77, 8), (77, 9), (77, 10), (77, 11), (77, 23), (77, 38), 
                       (77, 45), (78, 3), (78, 24), (78, 25), (78, 26), (78, 38), (78, 45), (79, 27), 
                       (79, 28), (79, 38), (79, 45), (80, 29), (80, 30), (80, 31), (80, 32), (80, 33), 
                       (80, 34), (80, 35), (80, 36), (80, 38), (80, 45), (81, 38), (81, 45), (82, 38), 
                       (82, 45), (83, 38), (83, 45), (84, 38), (84, 45), (85, 38), (85, 45), (86, 38), 
                       (86, 45), (87, 38), (87, 45), (88, 38), (88, 45), (89, 38), (89, 45), (90, 38), 
                       (90, 45), (91, 38), (91, 39), (91, 40), (91, 41), (91, 42), (91, 43), (91, 44), 
                       (91, 45)]


def NCToExpression(nc):
    if isinstance(nc,DecimalRepresentation):
        return render.generate(str(nc))

    s = []
    if nc.real != 0: 
        sreal = str(nc.real)
        if "/" in sreal: s.append([nc.real,f"[Frac]<{nc.real.numerator},{nc.real.denominator}>"])
        else: s.append([nc.real,sreal])
    if nc.imaginary != 0:
        simag = str(nc.imaginary)
        if "/" in simag: s.append([nc.imaginary,f"[Frac]<{abs(nc.imaginary.numerator)},{nc.imaginary.denominator}>i"])
        else:
            if abs(nc.imaginary)==1: 
                s.append([nc.imaginary,"i"])
            else:
                s.append([nc.imaginary,str(abs(nc.imaginary))+"i"])
                
    if nc.pi_multiple != 0:
        spim = str(nc.pi_multiple)
        if "/" in spim: s.append([nc.pi_multiple,f"[Frac]<{abs(nc.pi_multiple.numerator)},{nc.pi_multiple.denominator}>P"])
        else: 
            #s.append([nc.pi_multiple,spim+"p"])
            if abs(nc.pi_multiple)==1: 
                s.append([nc.pi_multiple,"P"])
            else:
                s.append([nc.pi_multiple,str(abs(nc.pi_multiple))+"P"])
    for r in nc.sqrt_components:
        ssq = str(r[0])
        if "/" in ssq: s.append([r[0],f"[Frac]<{abs(r[0].numerator)},{r[0].denominator}>[Sqrt]<{r[1]}>"])
        else:
            if abs(r[0]) == 1:
                s.append([r[0],f"[Sqrt]<{r[1]}>"])
            else: 
                s.append([r[0],f"{abs(r[0])}[Sqrt]<{r[1]}>"])

    r = ""
    for i in s:
        r+= "+" if i[0]>0 else "-"
        r+=i[1]

    r = r.replace("+-","-")
    r = r.replace("--","-")
    if r == "": r = "0"
    if r[0]=="+": r = r[1:]

    #r is the formatted string
    return render.generate(r)

x,y=128,64
currentScreen = render.generateArray(x,y)
currentMode = "CALC" #CALC, SOLV, or MENU
data = {
    "expr":"",
    "cursor":0,
    "currentAns":"",
    "recievedAns":False,
    "scroll":0}

"""data = {
    "currentPower":4,
    "expr":"",
    "cursor":0,
    "hasAns":False,
    "inputs":[],
    "ans":[]
}"""
#0 current typed expression (top-left)
#1 cursor for 0
#2 current answer (bottom right)
#3 has answered question

defaultDatas = {
    "CALC":{
    "expr":"",
    "cursor":0,
    "currentAns":"",
    "recievedAns":False,
    "scroll":0},

    "SOLV":{
    "currentPower":4,
    "expr":"",
    "cursor":0,
    "hasAns":False,
    "inputs":[],
    "ans":[],
    "scroll":0}
}

def getMaxScreenHeight(expression):
    h = render.generate(expression).height

    if h < y-5: return 0
    else: return h-y+5

def getHorizontalScroll(expression):
    if expression.width <= x: return 0
    cursorPoint = 0

    #find cursor
    for point in expression.points:
        l = [(x_+point[0],y_+point[1])for x_,y_ in renderformats.smallNumbers["|"]["points"]]
        for i in l:
            if i not in expression.points: break
        else: #it is there
            cursorPoint = point[0]

    if cursorPoint <= x: return 0
    else: return x-cursorPoint-4

def renderUpdate(): #given the data state, renderUpdate() will update the screen
    global data,currentMode,currentScreen
    currentScreen = render.generateArray(x,y)
    totalPoints = []

    if currentMode == "CALC":
        currentExpr = mathcode.render(data["expr"],data["cursor"]) if not data["recievedAns"] else data["expr"]
        pointsTL = render.generate(currentExpr)

        pointsBR = data["currentAns"] if data["currentAns"] != "-" else BaseExpression("-")
        pointsBRList = render.offsetPointList(pointsBR.points,x-pointsBR.width,y-pointsBR.height) if pointsBR else []

        totalPoints+=render.offsetPointList(pointsTL.points,getHorizontalScroll(pointsTL),-data["scroll"])
        totalPoints+=pointsBRList
    elif currentMode == "SOLV":
        if data["currentPower"]>=0:
            pointsTL = render.generate(mathcode.render(data["expr"],data["cursor"]))
            pointsBR = render.generate(f"[Power]<x,{str(data['currentPower'])}>")
            pointsBRList = render.offsetPointList(pointsBR.points,x-pointsBR.width,y-pointsBR.height)

            totalPoints+=render.offsetPointList(pointsTL.points,getHorizontalScroll(pointsTL),-data["scroll"])
            totalPoints+=pointsBRList
        else:
            if data["ans"]=="-":
                pointsTL = BaseExpression("-")
                totalPoints+=pointsTL.points
            else:
                for kind,k in enumerate(data["ans"]):
                    if k.isLong(): data["ans"][kind]=DecimalRepresentation(k,6)

                pointData = [NCToExpression(k) for k in data["ans"]]
                voffset = 0

                for d in pointData:
                    totalPoints+=render.offsetPointList(d.points,0,voffset)
                    voffset+=d.height+2 #padding
    elif currentMode == "MENU":
        totalPoints=menuScreenPoints.copy()

    currentScreen=totalPoints
    #perhaps convert to list of 0s and 1s but idk save it for whenever i get the lcd
    #physically display

def updateScreen(action):
    global data,currentMode,currentScreen
    parameters = action[1]
    #action in format ["type", [stuff]]

    # menu stuff
    if action[0] == "menu":
        data = {}
        currentMode = "MENU"

    if currentMode == "MENU":
        if action[0] == "type":
            if parameters[0] == "1":
                currentMode = "CALC"
                data = defaultDatas["CALC"]
            elif parameters[0] == "2":
                currentMode = "SOLV"
                data = defaultDatas["SOLV"]
    
    # calculation modes
    if currentMode == "CALC":
        if action[0] == "cursor":
            if data["recievedAns"] == True: #doesnt matter if left or right
                data["recievedAns"]=False
                data["currentAns"]=""
                data["cursor"] = len(data["expr"])-1
            else:
                if parameters[0] == "left":
                    data["expr"],data["cursor"] = mathcode.incrementCursorLeft(data["expr"],data["cursor"])
                elif parameters[0] == "right":
                    data["expr"],data["cursor"] = mathcode.incrementCursorRight(data["expr"],data["cursor"])

                if not data["recievedAns"]:
                    if parameters[0] == "up":
                        data["scroll"]-=5
                        if data["scroll"]<0: data["scroll"]=0
                    elif parameters[0] == "down":
                        data["scroll"]+=5
                        if data["scroll"]>getMaxScreenHeight(data["expr"]): data["scroll"]=getMaxScreenHeight(data["expr"])
        elif action[0] == "type": #we are typing something
            if currentMode == "CALC":
                if data["recievedAns"] == True:
                    data["recievedAns"]=False
                    data["currentAns"]=""
                    data["expr"] = parameters[0]
                    data["cursor"] = 0
                else:
                    data["expr"] = mathcode.isap(data["expr"],data["cursor"],parameters[0])
                    data["cursor"]+=1
        elif action[0] == "delim":
            if data["recievedAns"] == True:
                data["recievedAns"]=False
                data["currentAns"]=""
                data["expr"]=""
                data["cursor"]=0
            data["expr"],data["cursor"] = mathcode.addDelimiter(data["expr"],data["cursor"],parameters[0],
                                                                    delimiters.numbersOfParameters[parameters[0]])
        elif action[0] == "clear":
            data["recievedAns"] = False
            data["currentAns"] = False
            data["expr"] = ""
            data["cursor"] = 0
        elif action[0] == "backspace":
            if data["recievedAns"] == True:
                data["recievedAns"] = False
                data["currentAns"] = False
                data["expr"] = ""
                data["cursor"] = 0
            else:
                data["expr"],data["cursor"]=mathcode.backspace(data["expr"],data["cursor"])
        elif action[0] == "enter":
            data["recievedAns"] = True
            try:
                answer = tokenizer.parse(tokenizer.tokenize(data["expr"]))
                if answer.isLong():
                    answer = DecimalRepresentation(answer,8)

                data["currentAns"] = NCToExpression(answer)
            except Exception:
                data["currentAns"] = "-"

    if currentMode == "SOLV":
        if action[0] == "cursor":
            if not data["hasAns"]:
                if parameters[0] == "left":
                    data["expr"],data["cursor"] = mathcode.incrementCursorLeft(data["expr"],data["cursor"])
                elif parameters[0] == "right":
                    data["expr"],data["cursor"] = mathcode.incrementCursorRight(data["expr"],data["cursor"])          
                elif parameters[0] == "up":
                    data["scroll"]-=5
                    if data["scroll"]<0: data["scroll"]=0
                elif parameters[0] == "down":
                    data["scroll"]+=5
                    if data["scroll"]>getMaxScreenHeight(data["expr"]): data["scroll"]=getMaxScreenHeight(data["expr"])
        elif action[0] == "type": #we are typing something
            if not data["hasAns"]:
                data["expr"] = mathcode.isap(data["expr"],data["cursor"],parameters[0])
                data["cursor"]+=1
        elif action[0] == "delim":
            if not data["hasAns"]:
                data["expr"],data["cursor"] = mathcode.addDelimiter(data["expr"],data["cursor"],parameters[0],
                                                        delimiters.numbersOfParameters[parameters[0]])
        elif action[0] == "clear":
            if data["hasAns"]:
                data = deepcopy(defaultDatas["SOLV"])
            else:
                data["expr"] = ""
                data["cursor"] = 0
        elif action[0] == "backspace":
            if not data["hasAns"]:
                data["expr"],data["cursor"]=mathcode.backspace(data["expr"],data["cursor"])

        elif action[0] == "enter":
            data["currentPower"]-=1
            data["inputs"].append(tokenizer.parse(tokenizer.tokenize(data["expr"])))

            data["expr"]=""
            data["cursor"]=0

            if data["currentPower"]<0: #calculate expression
                data["hasAns"]=True
                try:
                    if data["inputs"][0] == 0:
                        if data["inputs"][1] == 0:
                            if data["inputs"][2] == 0: #degree = 1
                                data["ans"]=methods.linearSolve(*data["inputs"][3:])
                            else:#degree = 2
                                data["ans"]=methods.quadraticSolve(*data["inputs"][2:])
                        else: #degree = 3
                            data["ans"]=methods.cubicSolve(*data["inputs"][1:])
                    else: #degree = 4
                        data["ans"]=methods.quarticSolve(*data["inputs"])
                except:
                    data["ans"]="-"
    
    renderUpdate()
    
def getScreen():
    global currentScreen
    return currentScreen

#input types:
"""
menu
(type) number, letter, operator, constant keys
(delim) insert delimiter
clear
backspace
left,right arrow
enter/equals button
"""


#replace these values with the real key inputs later
equalsKey = 3
rightKey = 34
leftKey = 33
upKey = 32
downKey = 31
menuKey = 29
backspaceKey = 17
clearKey = 18

shiftKey = 35
cmdKey = 36

delimInputs = {
    25: "Frac",
    23: "Power",
    2: "Mod",
    26: "Sqrt",
    27: "NthRoot",
    20: "LogBase",
    21: "Ln",
    69: "Factorial",
    22: "Abs",
    70: "Choose",
    73: "W",
    71: "Floor",
    72: "Ceil",
    24: "Paren",

    126: "acos",
    125: "asin",
    127: "atan",
    120: "cos",
    119: "sin",
    121: "tan",

    110: "acosh",
    109: "asinh",
    111: "atanh",
    115: "cosh",
    114: "sinh",
    116: "tanh",
} # delimiters -- key is 
#typeInputs = [
#    "0","1","2","3","4","5","6","7","8","9",
#    "+","-","*","/","."
#    "E","P","i"
#] #single chars

typeInputs = {
    0:"0",
    4:"1",
    5:"2",
    6:"3",
    9:"4",
    10:"5",
    11:"6",
    14:"7",
    15:"8",
    16:"9",

    7:"+",
    8:"-",
    12:"*",
    13:"/",
    1:".",

    28:"i",
    78:"P",
    128:"E"
}

_SHIFT = False
_CMD = False

def parseInput(inp):
    global _SHIFT,_CMD
    if _SHIFT: inp += 50
    if _CMD: inp += 100

    if inp in typeInputs.keys():
        updateScreen(["type",[inp]])
    elif inp == equalsKey:
        updateScreen(["enter",[]])
    elif inp == backspaceKey:
        updateScreen(["backspace",[]])
    elif inp == menuKey:
        updateScreen(["menu",[]])
    elif inp == leftKey:
        updateScreen(["cursor",["left"]])
    elif inp == rightKey:
        updateScreen(["cursor",["right"]])
    elif inp == upKey:
        updateScreen(["cursor",["up"]])
    elif inp == downKey:
        updateScreen(["cursor",["down"]])
    elif inp == clearKey:
        updateScreen(["clear",[]])
    elif inp == shiftKey:
        _SHIFT = not _SHIFT
        _CMD = False
    elif inp == cmdKey:
        _CMD = not _CMD
        _SHIFT = False

    for key,v in delimInputs.items():
        if inp == key:
            updateScreen(["delim",[v]])

