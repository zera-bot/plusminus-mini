import mathcode
import render
import delimiters
import tokenizer
import methods
from comp import NumericalComponent
from render import CombinedExpression,BaseExpression
from copy import deepcopy

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
                pointData = [NCToExpression(k) for k in data["ans"]]
                voffset = 0

                for d in pointData:
                    totalPoints+=render.offsetPointList(d.points,0,voffset)
                    voffset+=d.height+2 #padding
    elif currentMode == "MENU":
        pass #do later lmao

    currentScreen=totalPoints

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
                data["currentAns"] = NCToExpression(tokenizer.parse(tokenizer.tokenize(data["expr"])))
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
        ["type",["0"]],
        ["enter",[]],
        ["type",["0"]],
        ["enter",[]],
        ["type",["-"]],
        ["type",["2"]],
        ["enter",[]],
        ["type",["0"]],
        ["enter",[]],
        ["type",["4"]],
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
        renderUpdate()
        renderCurrentScreen(f"systemTortureTest/{str(ind+1)}.png")

tortureTest()