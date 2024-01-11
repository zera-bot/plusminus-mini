import mathcode
import render
import delimiters
import tokenizer
import methods
from comp import NumericalComponent
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

def NCToExpression(nc:NumericalComponent):
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
        if "/" in spim: s.append([nc.pi_multiple,f"[Frac]<{abs(nc.pi_multiple.numerator)},{nc.pi_multiple.denominator}>p"])
        else: 
            #s.append([nc.pi_multiple,spim+"p"])
            if abs(nc.pi_multiple)==1: 
                s.append([nc.pi_multiple,"i"])
            else:
                s.append([nc.pi_multiple,str(abs(nc.pi_multiple))+"i"])
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
    "recievedAns":False}

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
    "recievedAns":False},

    "SOLV":{
    "currentPower":4,
    "expr":"",
    "cursor":0,
    "hasAns":False,
    "inputs":[],
    "ans":[]}
}

def renderUpdate(): #given the data state, renderUpdate() will update the screen
    global data,currentMode,currentScreen
    currentScreen = render.generateArray(x,y)
    totalPoints = []

    if currentMode == "CALC":
        currentExpr = mathcode.render(data["expr"],data["cursor"]) if not data["recievedAns"] else data["expr"]
        pointsTL = render.generate(currentExpr)

        pointsBR = data["currentAns"] if data["currentAns"] != "-" else BaseExpression("-")
        pointsBRList = render.offsetPointList(pointsBR.points,x-pointsBR.width,y-pointsBR.height) if pointsBR else []

        totalPoints+=pointsTL.points
        totalPoints+=pointsBRList
    elif currentMode == "SOLV":
        if data["currentPower"]>=0:
            pointsTL = render.generate(mathcode.render(data["expr"],data["cursor"]))
            pointsBR = render.generate(f"[Power]<-,{str(data['currentPower'])}>")
            pointsBRList = render.offsetPointList(pointsBR.points,x-pointsBR.width,y-pointsBR.height)

            totalPoints+=pointsTL.points
            totalPoints+=pointsBRList
        else:
            if data["ans"]=="-":
                pointsTL = BaseExpression("-")
                totalPoints+=pointsTL.points
            else:
                for kind,k in enumerate(data["ans"]):
                    if k.isLong(): data["ans"][kind]=round(k,6)

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
    if action[0] == "menu":
        data = {}
        currentMode = "MENU"
    elif action[0] == "cursor":
        if currentMode == "CALC":
            if data["recievedAns"] == True: #doesnt matter if left or right
                data["recievedAns"]=False
                data["currentAns"]=""
                data["cursor"] = len(data["expr"])-1
            else:
                if parameters[0] == "left":
                    data["expr"],data["cursor"] = mathcode.incrementCursorLeft(data["expr"],data["cursor"])
                elif parameters[0] == "right":
                    data["expr"],data["cursor"] = mathcode.incrementCursorRight(data["expr"],data["cursor"])
        elif currentMode == "SOLV":
            if not data["hasAns"]:
                if parameters[0] == "left":
                    data["expr"],data["cursor"] = mathcode.incrementCursorLeft(data["expr"],data["cursor"])
                elif parameters[0] == "right":
                    data["expr"],data["cursor"] = mathcode.incrementCursorRight(data["expr"],data["cursor"])                
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
        elif currentMode == "SOLV":
            if not data["hasAns"]:
                data["expr"] = mathcode.isap(data["expr"],data["cursor"],parameters[0])
                data["cursor"]+=1
        elif currentMode == "MENU": #menu selection
            if parameters[0] == "1":
                currentMode = "CALC"
                data = defaultDatas["CALC"]
            elif parameters[0] == "2":
                currentMode = "SOLV"
                data = defaultDatas["SOLV"]
    elif action[0] == "delim":
        if currentMode == "CALC":
            if data["recievedAns"] == True:
                data["recievedAns"]=False
                data["currentAns"]=""
                data["expr"]=""
                data["cursor"]=0
            data["expr"],data["cursor"] = mathcode.addDelimiter(data["expr"],data["cursor"],parameters[0],
                                                                    delimiters.numbersOfParameters[parameters[0]])
        elif currentMode == "SOLV":
            if not data["hasAns"]:
                data["expr"],data["cursor"] = mathcode.addDelimiter(data["expr"],data["cursor"],parameters[0],
                                                        delimiters.numbersOfParameters[parameters[0]])
    elif action[0] == "clear":
        if currentMode == "CALC":
            data["recievedAns"] = False
            data["currentAns"] = False
            data["expr"] = ""
            data["cursor"] = 0
        elif currentMode == "SOLV":
            if data["hasAns"]:
                data = deepcopy(defaultDatas["SOLV"])
            else:
                data["expr"] = ""
                data["cursor"] = 0
    elif action[0] == "backspace":
        if currentMode == "CALC":
            if data["recievedAns"] == True:
                data["recievedAns"] = False
                data["currentAns"] = False
                data["expr"] = ""
                data["cursor"] = 0
            else:
                data["expr"],data["cursor"]=mathcode.backspace(data["expr"],data["cursor"])
        elif currentMode == "SOLV":
            if not data["hasAns"]:
                data["expr"],data["cursor"]=mathcode.backspace(data["expr"],data["cursor"])
    elif action[0] == "enter":
        if currentMode == "CALC":
            data["recievedAns"] = True

            try:
                answer = tokenizer.parse(tokenizer.tokenize(data["expr"]))
                if answer.isLong():
                    answer = round(answer,8)

                data["currentAns"] = NCToExpression(answer)
            except Exception as e:
                data["currentAns"] = "-"
        elif currentMode == "SOLV":
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
    
from PIL import Image,ImageDraw
def renderCurrentScreen(path="image.png"):
    global currentScreen
    img = Image.new("RGB",(x,y),(255,255,255,255))
    draw = ImageDraw.Draw(img)

    for point in currentScreen:
        draw.point(point,(0,0,0,255))

    img.save(path)

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

def tortureTest():
    tests = [
        ["type",["3"]],
        ["type",["+"]],
        ["type",["4"]],
        ["type",["i"]],
        ["enter",[]],
        ["menu",[]],
        ["type",["2"]],
        ["type",["1"]],
        ["enter",[]],
        ["type",["0"]],
        ["enter",[]],
        #["type",["-"]],
        ["type",["0"]],
        ["enter",[]],
        ["type",["0"]],
        ["enter",[]],
        ["type",["-"]],
        ["type",["1"]],
        ["enter",[]],
        ["menu",[]],
        ["type",["1"]],
        ["delim",["Frac"]],
        ["delim",["Power"]],
        ["type",["4"]],
        ["cursor",["right"]],
        ["type",["5"]],
        ["cursor",["right"]],
        ["cursor",["right"]],
        ["type",["6"]],
        ["cursor",["right"]],
        ["type",["-"]],
        ["type",["2"]],
        ["type",["i"]],
        ["enter",[]]
    ]

    for ind,i in enumerate(tests):
        updateScreen(i)
        renderCurrentScreen(f"systemTortureTest/{str(ind+1)}.png")


#replace these values with the real key inputs later
equalsKey = "="
rightKey = "right"
leftKey = "left"
menuKey = "menu"
backspaceKey = "backspace"
clearKey = "clear"

delimInputs = {
    "Frac": "Frac",
    "Power": "Power",
    "Mod": "Mod",
    "Sqrt": "Sqrt",
    "NthRoot": "NthRoot",
    "LogBase": "LogBase",
    "Ln": "Ln",
    "Factorial": "Factorial",
    "Abs": "Abs",
    "Choose": "Choose",
    "W": "W",
    "Floor": "Floor",
    "Ceil": "Ceil",
    "Paren": "Paren",

    "acos": "acos",
    "asin": "asin",
    "atan": "atan",
    "cos": "cos",
    "sin": "sin",
    "tan": "tan",

    "acosh": "acosh",
    "asinh": "asinh",
    "atanh": "atanh",
    "cosh": "cosh",
    "sinh": "sinh",
    "tanh": "tanh",
} # delimiters -- key is 
typeInputs = [
    "0","1","2","3","4","5","6","7","8","9",
    "+","-","*","/","."
    "e","p","i"
]#single chars
def parseInput(inp):
    if inp in typeInputs:
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
    elif inp == clearKey:
        updateScreen(["clear",[]])

    for key,v in delimInputs.items():
        if inp == key:
            updateScreen(["delim",[v]])
    

tortureTest()