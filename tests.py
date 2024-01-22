from comp import *
from tokenizer import *
from render import *
from PIL import Image,ImageDraw

# draw functions
def drawExpression(expression,size,path="image.png"):
    if not (isinstance(expression,BaseExpression) or isinstance(expression,DelimiterExpression) or isinstance(expression,CombinedExpression)):
        raise TypeError
    img = Image.new("RGB",size,(255,255,255,255))
    draw = ImageDraw.Draw(img)

    for point in expression.points:
        draw.point(point,(0,0,0,255))

    img.save(path)

#tests
def compTest():
    a = NumericalComponent(frac(3),frac(4),frac(4),[[frac(2),frac(3)]])
    b = NumericalComponent(frac(-1),frac(3),frac(-4),[[frac(2),frac(3)],[frac(4),frac(5)]])

    c = NumericalComponent(Fraction(3,2),Fraction(6,7))

    f = lambda x: x**frac(2) - frac(4)*x
    g = lambda x: (x-frac(3))*(x+frac(5))*(x+frac(7))

    print("Printing Number:")
    print(c)

    print("Choose function:")
    print(c_choose(NumericalComponent(3),NumericalComponent(4)))
    print(c_choose(NumericalComponent(3),NumericalComponent(3)))
    print(c_choose(NumericalComponent(24),NumericalComponent(12)))

    print("Division by imaginary value:")
    v = NumericalComponent(frac(5),frac(5),frac(5),[[frac(5),frac(2)]])/NumericalComponent(imaginary=frac(4))
    print(v,complex(v))
    print(c/c)

    print("Square root:")
    print(c_sqrt(NumericalComponent(Fraction(3,5))))
    print(c_sqrt(NumericalComponent(-6)))
    print(c_sqrt(NumericalComponent(56)))

    d = NumericalComponent(Fraction(1),Fraction(3))
    e = NumericalComponent(Fraction(4),Fraction(5))

    print("Modulo:")
    print(d%e)

    print("Lambert W:")
    print(c_W(d))

    print("Type Conversion:")
    print(NumericalComponent(imaginary=4)-1)
    print(1-NumericalComponent(imaginary=4))
    print(1/NumericalComponent(3))

    print("Binary Operations:")
    bo0 = NumericalComponent(sqrt_components=[[5,4],[2,3],[6,6]])
    bo1 = NumericalComponent(sqrt_components=[[6,6],[2,3],[5,4]])

    print(NumericalComponent(1)==1)
    print(1==NumericalComponent(1))
    print(bo0==bo1)
    print(NumericalComponent(0,sqrt_components=[[80,0]])==0)
    print(NumericalComponent(sqrt_components=[[2,3]])==NumericalComponent(sqrt_components=[[3,2]]))

def renderTest():
    l = [r"[Power]<a,2>[Power]<c,2>",
         r"[Frac]<a+[Power]<a,2>,l+1>",
         r"[Frac]<a,c/2>",
         r"a+[Frac]<1,a+[Frac]<1,a+[Frac]<1,a>>>",
         r"[Sqrt]<1+[Sqrt]<1+[Sqrt]<1+[Sqrt]<1+a>>>>",
         r"[Paren]<[Frac]<[Power]<d,2>,d[Power]<a,2>>+[Frac]<[Power]<d,2>,d[Power]<a,2>>>",
         r"[Choose]<7,[Power]<2,2>+1>",
         r"[Choose]<d,2>[Power]<a,2>[Power]<c,d-2>-[Frac]<1,1-a>[Frac]<1,1-[Power]<a,2>>",

         #unofficial
         "a",
         "123[Frac]<3,[Frac]<[Frac]<6+4,1>,7>>+4323i",
         "[Frac]<3,[Power]<7,4>>",
         "[Frac]<3,[Sqrt]<[Frac]<3,[Power]<7,4>>>>",
         "[Paren]<[Power]<7,4>>",
         "[Power]<[E],[E]>",
         "[Mod]<3,[Frac]<4,5>>",
         "[Abs]<[Floor]<[Ceil]<[Frac]<4,5>>>>",
         "[Frac]<[acos]<3>+3[cos]<[Frac]<4,5>>,[Ln]<4>>",
         "[Sqrt]<[Power]<i+1,i>-1>",
         "[Paren]<[Frac]<[Frac]<2,3>,4>+[Frac]<5,2>>",
         "[NthRoot]<2,2i>",
         "[NthRoot]<[Frac]<3,4>+[E],[Frac]<2i,3>>",
         "[LogBase]<[E],17>",
         "[Frac]<[LogBase]<[Frac]<[Frac]<2+[Frac]<3,2>,2+[Frac]<3,2*2+[cos]<4>+3>>,3>,[Frac]<3,[Frac]<1,1+[acos]<1>>>>,17>",
         "[Frac]<[LogBase]<[Frac]<[Frac]<2+[Frac]<3,2>,5>,3>,[Frac]<3,[Frac]<1,2>>>,17>",
         "[Factorial]<[Frac]<2,[Frac]<3,[sin]<5>>>>",
         "[Ln]<[Frac]<2,[Frac]<3,[sin]<5>+3>>-[sin]<3>>",
         "[Sqrt]<[Frac]<3,4>-1>",
         "[Erf]<3x+1>"
         ]
    
    for ind,m in enumerate(l):
        array = generate(m)
        drawExpression(array,(128,64),f"tortureTest/{str(ind+1)}.png")

def parserTest():
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

compTest()
renderTest()
parserTest()