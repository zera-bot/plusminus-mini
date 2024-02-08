from comp import c_sqrt as sqrt
from comp import NumericalComponent,frac
from fractions import Fraction
from math import factorial

import xmath

I = NumericalComponent(imaginary=Fraction(1))

#tools
def ncSum(l):
    s = NumericalComponent()
    for i in l:
        s += i
    return s

def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

#start

def substitute(f,x):
    return f(x)

# solve f(x) = 0 equations

def linearSolve(a,b): #ax+b=0
    return [-b/a]

def quadraticSolve(a,b,c): #ax^2+bx+c=0
    return unique([(-b - sqrt(-4*a*c + b**2))/(2*a), (-b + sqrt(-4*a*c + b**2))/(2*a)])

def cubicSolve(a,b,c,d): #ax^3+bx^2+cx+d=0
    return unique([ -(-3*c/a + b**2/a**2)/(3*(sqrt(-4*(-3*c/a + b**2/a**2)**3 + (27*d/a - 9*b*c/a**2 + 2*b**3/a**3)**2)/2 + 27*d/(2*a) - 9*b*c/(2*a**2) + b**3/a**3)**(1/3)) - (sqrt(-4*(-3*c/a + b**2/a**2)**3 + (27*d/a - 9*b*c/a**2 + 2*b**3/a**3)**2)/2 + 27*d/(2*a) - 9*b*c/(2*a**2) + b**3/a**3)**(1/3)/3 - b/(3*a),
             -(-3*c/a + b**2/a**2)/(3*(-1/2 - sqrt(3)*I/2)*(sqrt(-4*(-3*c/a + b**2/a**2)**3 + (27*d/a - 9*b*c/a**2 + 2*b**3/a**3)**2)/2 + 27*d/(2*a) - 9*b*c/(2*a**2) + b**3/a**3)**(1/3)) - (-1/2 - sqrt(3)*I/2)*(sqrt(-4*(-3*c/a + b**2/a**2)**3 + (27*d/a - 9*b*c/a**2 + 2*b**3/a**3)**2)/2 + 27*d/(2*a) - 9*b*c/(2*a**2) + b**3/a**3)**(1/3)/3 - b/(3*a), 
             -(-3*c/a + b**2/a**2)/(3*(-1/2 + sqrt(3)*I/2)*(sqrt(-4*(-3*c/a + b**2/a**2)**3 + (27*d/a - 9*b*c/a**2 + 2*b**3/a**3)**2)/2 + 27*d/(2*a) - 9*b*c/(2*a**2) + b**3/a**3)**(1/3)) - (-1/2 + sqrt(3)*I/2)*(sqrt(-4*(-3*c/a + b**2/a**2)**3 + (27*d/a - 9*b*c/a**2 + 2*b**3/a**3)**2)/2 + 27*d/(2*a) - 9*b*c/(2*a**2) + b**3/a**3)**(1/3)/3 - b/(3*a)
             ])

def cubicSolve2(a,b,c,d):
    # turn into depressed cubic of form x^3 + px + q
    third = 1/3
    p = (3*a*c - b**2)/(3*a**2)
    q = (2*b**3 -9*a*b*c + 27*d*a**2)/(27*a**3)

    root_term = sqrt((27*q**2 -4*q*p**3)/27)

    u0 = (-q + root_term)/2
    u1 = (-q - root_term)/2
    v0 = (q + root_term)/2
    v1 = (q - root_term)/2

    l = [u0**third - (v0**third) - (b/(3*a)),
         u1**third - (v0**third) - (b/(3*a)),
         u0**third - (v1**third) - (b/(3*a)),
         u1**third - (v1**third) - (b/(3*a))]
    # solve
    return unique(l)

def quarticSolve(a,b,c,d,e):
    # turn into a depressed quartic of form x^4+px^2+q+r
    p = (8*a*c -3*b**2)/(8*a**2)
    q = (b**3 - 4*a*b*c + 8*d*a**2)/(8*a**3)
    r = (-3*b**4 + 16*a*c*b**2 - 64*b*d*a**2 + 256*e*a**3)/(256*a**4)

    # factor into (y^2 + sy + t)(y^2 + uy + v)
    # find u
    totalSolutions = cubicSolve(NumericalComponent(1), 2*p, p**2 - 4*r, -q**2)
    def tryUIndex(ind): #from 0-2
        u = totalSolutions[ind] #not sure which root to use
        u = sqrt(u)
        s = -u

        # find t and v
        t = (u**3+p*u+q)/(2*u)
        v = t - q/u

        #now solve the original factors of the depressed quartic
        l = quadraticSolve(NumericalComponent(1),s,t)+quadraticSolve(NumericalComponent(1),u,v)
        return [m - ( b/(4*a) ) for m in l]

    def f(x):
        return a*x**4+ b*x**3+ c*x**2 +d*x + e

    threshold = 1e-8
    for i in range(len(totalSolutions)):
        isValid = True
        solns = tryUIndex(i)
        for j in solns:
            complexFormatSolution = complex(f(j))
            real = complexFormatSolution.real<threshold and complexFormatSolution.real>-threshold
            imag = complexFormatSolution.imag<threshold and complexFormatSolution.imag>-threshold
            if not (real and imag): isValid = False
        
        if isValid: return solns

def quarticSolve2(a,b,c,d):
    return [
        (-a/4 - sqrt((((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))/54)**(1/3) + ((2**(1/3)*(12*d + (b**2 - 3*a*c)))/((3*((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))**(1/3))) + (a**2/4 - (2*b)/3)))/2) - (sqrt(-(-8*c + (-a**3 + 4*(a*b)))/(4*sqrt((((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))/54)**(1/3) + ((2**(1/3)*(12*d + (b**2 - 3*a*c)))/((3*((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))**(1/3))) + (a**2/4 - 2*b/3)))) + (-(((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))/54)**(1/3) + (-2**(1/3)*(12*d + (b**2 - 3*a*c))/(3*((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))**(1/3)) + (a**2/2 - 4*b/3))))/2),
        (-a/4 - sqrt((((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))/54)**(1/3) + ((2**(1/3)*(12*d + (b**2 - 3*a*c)))/((3*((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))**(1/3))) + (a**2/4 + (2*b)/3)))/2) - (sqrt(-(-8*c + (-a**3 + 4*(a*b)))/(4*sqrt((((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))/54)**(1/3) + ((2**(1/3)*(12*d + (b**2 - 3*a*c)))/((3*((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))**(1/3))) + (a**2/4 - 2*b/3)))) + (-(((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))/54)**(1/3) + (-2**(1/3)*(12*d + (b**2 - 3*a*c))/(3*((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))**(1/3)) + (a**2/2 - 4*b/3))))/2),
        (-a/4 + sqrt((((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))/54)**(1/3) + ((2**(1/3)*(12*d + (b**2 - 3*a*c)))/((3*((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))**(1/3))) + (a**2/4 - (2*b)/3)))/2) - (sqrt(-(-8*c + (-a**3 + 4*(a*b)))/(4*sqrt((((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))/54)**(1/3) + ((2**(1/3)*(12*d + (b**2 - 3*a*c)))/((3*((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))**(1/3))) + (a**2/4 - 2*b/3)))) + (-(((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))/54)**(1/3) + (-2**(1/3)*(12*d + (b**2 - 3*a*c))/(3*((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))**(1/3)) + (a**2/2 - 4*b/3))))/2),
        (-a/4 + sqrt((((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))/54)**(1/3) + ((2**(1/3)*(12*d + (b**2 - 3*a*c)))/((3*((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))**(1/3))) + (a**2/4 + (2*b)/3)))/2) - (sqrt(-(-8*c + (-a**3 + 4*(a*b)))/(4*sqrt((((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))/54)**(1/3) + ((2**(1/3)*(12*d + (b**2 - 3*a*c)))/((3*((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))**(1/3))) + (a**2/4 - 2*b/3)))) + (-(((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))/54)**(1/3) + (-2**(1/3)*(12*d + (b**2 - 3*a*c))/(3*((-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c))))) + sqrt(-4*(12*d + (b**2 - 3*a*c))**3 + (-72*b*d + (27*(a**2*d) + (27*c**2 + (2*b**3 - 9*a*(b*c)))))**2))**(1/3)) + (a**2/2 - 4*b/3))))/2),
    ]

def quarticSolve3(a,b,c,d,e): #ax^4+bx^3+cx^2+dx+e=0
    x1=None
    x2=None
    x3=None
    x4=None

    if e/a - b*d/(4*a**2) + c**2/(12*a**2) == NumericalComponent():
        x1=(-sqrt(-2*(-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**(1/3) - 2*c/(3*a) + b**2/(4*a**2))/2 - sqrt((2*d/a - b*c/a**2 + b**3/(4*a**3))/sqrt(-2*(-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**(1/3) - 2*c/(3*a) + b**2/(4*a**2)) + 2*(-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**(1/3) - 4*c/(3*a) + b**2/(2*a**2))/2 - b/(4*a))
        x2=(-sqrt(-2*(-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**(1/3) - 2*c/(3*a) + b**2/(4*a**2))/2 + sqrt((2*d/a - b*c/a**2 + b**3/(4*a**3))/sqrt(-2*(-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**(1/3) - 2*c/(3*a) + b**2/(4*a**2)) + 2*(-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**(1/3) - 4*c/(3*a) + b**2/(2*a**2))/2 - b/(4*a))
        x3=(sqrt(-2*(-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**(1/3) - 2*c/(3*a) + b**2/(4*a**2))/2 - sqrt(-(2*d/a - b*c/a**2 + b**3/(4*a**3))/sqrt(-2*(-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**(1/3) - 2*c/(3*a) + b**2/(4*a**2)) + 2*(-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**(1/3) - 4*c/(3*a) + b**2/(2*a**2))/2 - b/(4*a))
        x4=(sqrt(-2*(-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**(1/3) - 2*c/(3*a) + b**2/(4*a**2))/2 + sqrt(-(2*d/a - b*c/a**2 + b**3/(4*a**3))/sqrt(-2*(-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**(1/3) - 2*c/(3*a) + b**2/(4*a**2)) + 2*(-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**(1/3) - 4*c/(3*a) + b**2/(2*a**2))/2 - b/(4*a))
    else:
        x1=(-sqrt(-2*(-e/a + b*d/(4*a**2) - c**2/(12*a**2))/(3*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3)) + 2*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3) - 2*c/(3*a) + b**2/(4*a**2))/2 - 
            sqrt((2*d/a - b*c/a**2 + b**3/(4*a**3))/sqrt(-2*(-e/a + b*d/(4*a**2) - c**2/(12*a**2))/(3*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3)) + 2*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3) - 2*c/(3*a) + b**2/(4*a**2)) + 2*(-e/a + b*d/(4*a**2) - c**2/(12*a**2))/(3*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3)) - 2*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3) - 4*c/(3*a) + b**2/(2*a**2))/2 - b/(4*a))
        x2=(-sqrt(-2*(-e/a + b*d/(4*a**2) - c**2/(12*a**2))/(3*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3)) + 2*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3) - 2*c/(3*a) + b**2/(4*a**2))/2 + 
            sqrt((2*d/a - b*c/a**2 + b**3/(4*a**3))/sqrt(-2*(-e/a + b*d/(4*a**2) - c**2/(12*a**2))/(3*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3)) + 2*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3) - 2*c/(3*a) + b**2/(4*a**2)) + 2*(-e/a + b*d/(4*a**2) - c**2/(12*a**2))/(3*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3)) - 2*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3) - 4*c/(3*a) + b**2/(2*a**2))/2 - b/(4*a))
        x3=(sqrt(-2*(-e/a + b*d/(4*a**2) - c**2/(12*a**2))/(3*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3)) + 2*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3) - 2*c/(3*a) + b**2/(4*a**2))/2 - 
            sqrt(-(2*d/a - b*c/a**2 + b**3/(4*a**3))/sqrt(-2*(-e/a + b*d/(4*a**2) - c**2/(12*a**2))/(3*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3)) + 2*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3) - 2*c/(3*a) + b**2/(4*a**2)) + 2*(-e/a + b*d/(4*a**2) - c**2/(12*a**2))/(3*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3)) - 2*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3) - 4*c/(3*a) + b**2/(2*a**2))/2 - b/(4*a))
        x4=(sqrt(-2*(-e/a + b*d/(4*a**2) - c**2/(12*a**2))/(3*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3)) + 2*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3) - 2*c/(3*a) + b**2/(4*a**2))/2 + 
            sqrt(-(2*d/a - b*c/a**2 + b**3/(4*a**3))/sqrt(-2*(-e/a + b*d/(4*a**2) - c**2/(12*a**2))/(3*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3)) + 2*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3) - 2*c/(3*a) + b**2/(4*a**2)) + 2*(-e/a + b*d/(4*a**2) - c**2/(12*a**2))/(3*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3)) - 2*((c/a - 3*b**2/(8*a**2))**3/216 - (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/6 + sqrt((-e/a + b*d/(4*a**2) - c**2/(12*a**2))**3/27 + (-(c/a - 3*b**2/(8*a**2))**3/108 + (c/a - 3*b**2/(8*a**2))*(e/a - b*d/(4*a**2) + b**2*c/(16*a**3) - 3*b**4/(256*a**4))/3 - (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/8)**2/4) + (d/a - b*c/(2*a**2) + b**3/(8*a**3))**2/16)**(1/3) - 4*c/(3*a) + b**2/(2*a**2))/2 - b/(4*a))

    return unique([x1,x2,x3,x4] )     

# numerically find roots

def findRoot(f,a,b,iterations=4700): # range is [a,b]
    stoppingThreshold = Fraction("1e-12")
    checkThreshold = Fraction("1e-8")
    median = (a+b)/frac(2)

    x_nM2 = median #x_(n-2)
    x_nM1 = median #x_(n-1)
    x_n = frac(0)
    n = frac(2)

    for i in range(iterations):
        if f(x_n) < stoppingThreshold and f(x_n) > -stoppingThreshold:
            break
        n+=frac(1)
        x_nM2 = x_nM1
        x_nM1 = x_n
        x_n = x_nM1 -f(x_nM1) * ( (x_nM1 - x_nM2) / ( f(x_nM1) - f(x_nM2) ) )

    if not ( ( f(x_n) < checkThreshold and f(x_n) > -checkThreshold ) and ( f(x_nM1) < checkThreshold and f(x_nM1) > -checkThreshold ) ):
        return None
    return NumericalComponent(Fraction(float(x_n)))

# regression

def generateRSquared(expectedValue,pointsX,pointsY,avgY):
    ssr = ncSum([(pointsY[ind]-expectedValue(x))**2 for ind,x in enumerate(pointsX)])
    sst = ncSum([(pointsY[ind]-avgY)**2 for ind,_ in enumerate(pointsX)])
    return NumericalComponent(frac(1)) - ssr/sst

def linearRegression(points):
    pointsX,pointsY=[x for x,y in points],[y for x,y in points]

    n = NumericalComponent(len(points))
    sumx,sumy = ncSum(pointsX),ncSum(pointsY)
    b = (ncSum([x*y for x,y in zip(pointsX,pointsY)]) - (sumx*sumy)/n) / (ncSum([x**2 for x in pointsX]) - (sumx**2)/n)
    a = sumy/n - (sumx/n * b)

    def expectedValue(x):
        return a+b*x
    rSquared = generateRSquared(expectedValue,pointsX,pointsY,sumy/n)

    return [b,a,rSquared] # f(x) = bx+a

# calculus

def evaluateDerivative(f,at):
    def limitFunction(h):
        return (f(at+h)-f(at))/h
    
    small = NumericalComponent(Fraction("0.0000000000001"))
    return ( limitFunction(small)+limitFunction(-small) )/2

def evaluateDefiniteIntegral(f,a,b):
    if a>b: return -evaluateDefiniteIntegral(f,b,a)
    if a == b: return NumericalComponent()

    n = 100000 #1e5
    dx = (b-a)/n

    sumLeft = NumericalComponent()
    sumRight = NumericalComponent()

    #x_i = x_0 + i*dx
    for i in range(1,n+1):
        sumRight += f(a + i*dx)*dx

    for i in range(n):
        sumLeft += f(a + i*dx)*dx

    return (sumLeft+sumRight)/2

def summation(f,a,b): #capital sigma
    _sum = NumericalComponent()
    for n in range(a,b+1):
        _sum+=f(n)
    return _sum

def product(f,a,b): #capital sigma
    _prod = NumericalComponent()
    for n in range(a,b+1):
        _prod*=f(n)
    return _prod

# misc

def erf(z):
    const = 2/sqrt(NumericalComponent(pi_multiple=1))
    f = lambda x: ((-1)**x) * (z**(2*x+1))/(factorial(x)*(2*x+1))
    _sum = summation(f,0,1000)
    return const*_sum