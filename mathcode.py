import re

#remove these two variables when done
s = "[Frac]<3,a[Frac]<6,7>>" # string
c = 0 # cursor
#char value n is BEFORE n'th character
#char before cursor = cursor-1
#char after cursor = cursor

def render(string,cursor):
    return string[:cursor]+"|"+string[cursor:]

def incrementCursorRight(string,cursor):
    cursor+=1
    if cursor > len(string)-1: cursor = 0
    if cursor != 0 and string[cursor-1] == "[":
        while s[cursor-1] != "<": cursor+=1
    return string,cursor

def incrementCursorLeft(string,cursor):
    cursor-=1
    if cursor < 0: cursor = len(string)-1
    if string[cursor] == "<":
        while string[cursor] != "[": cursor-=1
    return string,cursor

def backspace(string,cursor):
    if cursor == 0: return string,cursor # 1
    elif string[cursor-1] == ">" or string[cursor-1] == ",": return incrementCursorLeft(string,cursor) #3, 4
    elif string[cursor-1] == "]": #delete standalone delimiters
        delimStartingBound = cursor-1
        delimEndingBound = cursor

        while string[delimStartingBound] != "[": #find starting bound of delimiter
            delimStartingBound-=1

        string = string[:delimStartingBound]+string[delimEndingBound+1:]
        cursor = delimStartingBound
        return string,cursor
    elif string[cursor-1] == "<": #2, delete entire delimiter
        delimStartingBound = cursor
        delimEndingBound = cursor

        while string[delimStartingBound] != "[": #find starting bound of delimiter
            delimStartingBound-=1

        bracketList = ["<"]
        while len(bracketList)>0:
            delimEndingBound+=1
            if string[delimEndingBound] == "<": bracketList.append("<")
            if string[delimEndingBound] == ">": bracketList.append(">")
            if "<" in bracketList and ">" in bracketList:
                bracketList.remove("<")
                bracketList.remove(">")

        string = string[:delimStartingBound]+string[delimEndingBound+1:]
        cursor = delimStartingBound
        return string,cursor
    else:
        string,cursor = incrementCursorLeft(string,cursor)
        string = string[:cursor]+string[cursor+1:]
        return string,cursor

def addDelimiter(string,cursor,delimName,numberOfParameters=1):
    delimString = f"[{delimName}]<"+"".join(["," for k in range(numberOfParameters-1)])+">"
    string = string[:cursor]+delimString+string[cursor:]
    cursor+=len(delimName)+3
    return string,cursor

print(render(s,c))
s,c = incrementCursorRight(s,c)
print(render(s,c))
s,c = incrementCursorLeft(s,c)
print(render(s,c))
s,c = backspace(s,c)
print(render(s,c))
s,c = addDelimiter(s,c,"Frac",2)
print(render(s,c))