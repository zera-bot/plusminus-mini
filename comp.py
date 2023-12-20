import xmath
import math
import cmath

from fractions import Fraction
import decimal
from copy import deepcopy as dc

def frac(x):
    return Fraction(x,1)

def removeDuplicatesInSqrtComponents(components):
    distinct = []
    for c in components:
        has = False
        for ind,d in enumerate(distinct):
            if d[1] == c[1]:
                has = True
                distinct[ind][0] += c[0]
                break
        if not has:
            distinct.append(c)
    return dc(distinct)

class NumericalComponent:
    def __init__(self, real=frac(0), imaginary=frac(0), pi_multiple=frac(0), sqrt_components=[]):
        self.real = real
        
        self.pi_multiple = pi_multiple

        #remove duplicate square root components again which is important

        sqrt_components = removeDuplicatesInSqrtComponents(sqrt_components)

        #remove non-whole number sqrts
        for r in sqrt_components:
            if r[1] % 1 != frac(0):
                self.real+=r[0]*xmath.sqrt(r[1])
                sqrt_components.remove(r)

        #simplify fully
        for r in sqrt_components:
            if r[1] < 0:
                #convert negative perfect squares to terms of i
                #and convert negative non-perfect squares to approximate terms of i
                imaginary += r[0] * xmath.sqrt(abs(r[1]))
                sqrt_components.remove(r)
            elif xmath.sqrt(r[1]) % 1 == frac(0):
                self.real+=xmath.sqrt(r[1])*r[0]
                sqrt_components.remove(r)
            else:
                for factor_root in range(int(math.sqrt(r[1])), 1, -1):
                    factor = factor_root ** 2
                    if r[1] % factor == 0:
                        reduced = r[1] // factor
                        sqrt_components.remove(r)
                        sqrt_components.append([frac(factor_root)*r[0],frac(reduced)])

        self.imaginary = imaginary

        self.sqrt_components = removeDuplicatesInSqrtComponents(sqrt_components)
        #each sqrt component is laid out as [multiple,value]

    # operators

    def __add__(self,other):
        sum = NumericalComponent(self.real+other.real,
                                  self.imaginary+other.imaginary,
                                  self.pi_multiple+other.pi_multiple)
        selfRoots = self.sqrt_components

        for root in other.sqrt_components:
            hasRoot = False
            for selfRoot in selfRoots:
                if selfRoot[1] == root[1]:
                    selfRoot[0]+=root[0]
                    hasRoot = True
            if not hasRoot:
                selfRoots.append(root)

        sum.sqrt_components=selfRoots
        return sum

    def __sub__(self,other):
        sum = NumericalComponent(self.real+other.real,
                                  self.imaginary+other.imaginary,
                                  self.pi_multiple+other.pi_multiple)
        selfRoots = self.sqrt_components

        for root in other.sqrt_components:
            hasRoot = False
            for selfRoot in selfRoots:
                if selfRoot[1] == root[1]:
                    selfRoot[0]-=root[0]
                    hasRoot = True
            if not hasRoot:
                selfRoots.append(root)

        sum.sqrt_components=selfRoots
        return sum
    
    def __mul__(self,other):
        mainSum = NumericalComponent(sqrt_components=[])
        approximateSum = NumericalComponent(sqrt_components=[])

        # row 1
        rootListOne = []
        for r in other.sqrt_components:
            rootListOne.append([self.real*r[0],r[1]])
        mainSum += NumericalComponent(self.real*other.real, self.real*other.imaginary, self.real*other.pi_multiple, rootListOne)
        # row 2
        for r in other.sqrt_components:
            approximateSum += NumericalComponent(imaginary=self.imaginary * r[0] * xmath.sqrt(r[1]) )
        mainSum += NumericalComponent(-self.imaginary*other.imaginary,self.imaginary*other.real)
        approximateSum += NumericalComponent(imaginary=self.imaginary*other.pi_multiple*xmath.pi)
        # row 3
        rowThreeSum = frac(0)
        for r in other.sqrt_components:
            rowThreeSum += xmath.pi * self.pi_multiple * (r[0] * xmath.sqrt(r[1]))
        approximateSum += NumericalComponent(rowThreeSum)

        mainSum += NumericalComponent(pi_multiple=self.pi_multiple*other.real)
        approximateSum += NumericalComponent(self.pi_multiple*other.pi_multiple*(xmath.pi**2) , self.pi_multiple*other.imaginary*xmath.pi)
        # row(s) 4+
        for r in self.sqrt_components:
            mainSum += NumericalComponent(sqrt_components=[[r[0]*other.real,r[1]]])
            approximateSum += NumericalComponent(imaginary= other.imaginary * ( r[0] * xmath.sqrt(r[1]) ),
                                                 pi_multiple= other.pi_multiple * ( r[0] * xmath.sqrt(r[1]) ))
            
            for s in other.sqrt_components:
                mainSum += NumericalComponent(sqrt_components=[[r[0]*s[0],r[1]*s[1]]])


        return mainSum+approximateSum

    def __truediv__(self,other):
        componentsThatAreZero = 0

        mainSum = NumericalComponent(sqrt_components=[])

        if other.real == frac(0): componentsThatAreZero+=1
        if other.imaginary == frac(0): componentsThatAreZero+=1
        if other.pi_multiple == frac(0): componentsThatAreZero+=1

        #if only one component is the divisor
        if (len(other.sqrt_components) == 1 and componentsThatAreZero == 3) or (len(other.sqrt_components) == 0 and componentsThatAreZero == 2):
            if len(other.sqrt_components) == 0:
                if other.imaginary != frac(0): #if we are dividing by only imaginary value
                    sqrtAndPiSumSelf = frac(0)
                    for r in self.sqrt_components:
                        sqrtAndPiSumSelf += r[0]*xmath.sqrt(r[1])
                    sqrtAndPiSumSelf+=xmath.pi*self.pi_multiple

                    mainSum+=NumericalComponent(self.imaginary/other.imaginary,-(self.real/other.imaginary + sqrtAndPiSumSelf/other.imaginary))
                else: #if we are dividing by only a real value
                    sqrtSumOther = frac(0)
                    for r in other.sqrt_components:
                        sqrtSumOther+=r[0]*xmath.sqrt(r[1])

                    divisionValue = other.real+(other.pi_multiple*xmath.pi)+sqrtSumOther

                    mainSum+=NumericalComponent(self.real/divisionValue, self.imaginary/divisionValue,
                    self.pi_multiple/divisionValue, [[k[0]/divisionValue,k[1]] for k in self.sqrt_components])
        else: #just approximate at this point
            mainSum = self * (other**-1)

        return mainSum
    
    def __pow__(self,other):
        val = complex(self) ** complex(other)
        return NumericalComponent(Fraction(val.real),Fraction(val.imag))

    #display

    def __str__(self):
        s = []
        if self.real != frac(0): s.append(str(self.real))
        if self.imaginary != frac(0): s.append(str(self.imaginary)+"i")
        if self.pi_multiple != frac(0): s.append(str(self.pi_multiple)+"pi")
        for r in self.sqrt_components:
            s.append(f"{r[0]}sqrt({r[1]})")
        
        r = " + ".join(s)
        return r.replace("+ -","- ")

    #other

    def __abs__(self):
        k = complex(self)
        return xmath.sqrt(k.real**2 + k.imag**2)
    
    def __complex__(self):
        v = complex(self.real+(xmath.pi*self.pi_multiple),self.imaginary)
        for w in self.sqrt_components:
            v += complex(w[0]*xmath.sqrt(w[1]),0)
        return v

    def isOnlyReal(self):
        return self.imaginary == frac(0)

    def isOnlyRationalReal(self):
        return self.imaginary == frac(0) and self.pi_multiple == frac(0) and len(self.sqrt_components) == frac(0)

    #def __nonzero__(self):
    #    return not self.real == 0 and self.imaginary == 0 and self.pi_multiple == 0 and len(self.sqrt_components) == 0

# library

def c_log(x,base=xmath.e):
    y = complex(x)
    result = cmath.log(y,base)
    return NumericalComponent(Fraction(decimal.Decimal(result.real)),Fraction(decimal.Decimal(result.imag)))

def c_ln(x):
    return c_log(x)

def c_sqrt(x):
    if x.imaginary == frac(0) and x.pi_multiple == frac(0) and len(x.sqrt_components) == 0:
        return NumericalComponent(sqrt_components=[[frac(1),frac(x.real)]])

    return x**.5

def c_factorial(x:NumericalComponent):
    if x.imaginary != 0 or x.pi_multiple != 0 or len(x.sqrt_components) > 0: raise TypeError
    if x.real % 1 == frac(0):
        return NumericalComponent(frac(math.factorial(int(x.real))))
    else:
        raise TypeError
    
def c_choose(n:NumericalComponent,k:NumericalComponent):
    return c_factorial(n) / ( c_factorial(k) * c_factorial(n-k))

# trig functions

def c_acos(x):
    result = cmath.acos(complex(x))
    return NumericalComponent(Fraction(decimal.Decimal(result.real)),
                              Fraction(decimal.Decimal(result.imag)))

def c_asin(x):
    result = cmath.asin(complex(x))
    return NumericalComponent(Fraction(decimal.Decimal(result.real)),
                              Fraction(decimal.Decimal(result.imag)))

def c_atan(x):
    result = cmath.atan(complex(x))
    return NumericalComponent(Fraction(decimal.Decimal(result.real)),
                              Fraction(decimal.Decimal(result.imag)))

def c_cos(x):
    result = cmath.cos(complex(x))
    return NumericalComponent(Fraction(decimal.Decimal(result.real)),
                              Fraction(decimal.Decimal(result.imag)))

def c_sin(x):
    result = cmath.sin(complex(x))
    return NumericalComponent(Fraction(decimal.Decimal(result.real)),
                              Fraction(decimal.Decimal(result.imag)))

def c_tan(x):
    result = cmath.tan(complex(x))
    return NumericalComponent(Fraction(decimal.Decimal(result.real)),
                              Fraction(decimal.Decimal(result.imag)))

# hyperbolics

def c_acosh(x):
    result = cmath.acosh(complex(x))
    return NumericalComponent(Fraction(decimal.Decimal(result.real)),
                              Fraction(decimal.Decimal(result.imag)))

def c_asinh(x):
    result = cmath.asinh(complex(x))
    return NumericalComponent(Fraction(decimal.Decimal(result.real)),
                              Fraction(decimal.Decimal(result.imag)))

def c_atanh(x):
    result = cmath.atanh(complex(x))
    return NumericalComponent(Fraction(decimal.Decimal(result.real)),
                              Fraction(decimal.Decimal(result.imag)))

def c_cosh(x):
    result = cmath.cosh(complex(x))
    return NumericalComponent(Fraction(decimal.Decimal(result.real)),
                              Fraction(decimal.Decimal(result.imag)))

def c_sinh(x):
    result = cmath.sinh(complex(x))
    return NumericalComponent(Fraction(decimal.Decimal(result.real)),
                              Fraction(decimal.Decimal(result.imag)))

def c_tanh(x):
    result = cmath.tanh(complex(x))
    return NumericalComponent(Fraction(decimal.Decimal(result.real)),
                              Fraction(decimal.Decimal(result.imag)))

# equation tools

def substitute(f,x):
    return f(x)

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



a = NumericalComponent(frac(3),frac(4),frac(4),[[frac(2),frac(3)]])
b = NumericalComponent(frac(-1),frac(3),frac(-4),[[frac(2),frac(3)],[frac(4),frac(5)]])

c = NumericalComponent(Fraction(3,2),Fraction(6,7))

f = lambda x: x**frac(2) - frac(4)*x
g = lambda x: (x-frac(3))*(x+frac(5))*(x+frac(7))

print("Printing Number:")
print(c)

print("Choose function:")
print(c_choose(NumericalComponent(3),NumericalComponent(4)))

print("Division by imaginary value:")
v = NumericalComponent(frac(5),frac(5),frac(5),[[frac(5),frac(2)]])/NumericalComponent(imaginary=frac(4))
print(v,complex(v))

print("Approximate Zero:")
print(findRoot(g,Fraction(3.5),Fraction(4.5)))

print("Square root:")
print(c_sqrt(NumericalComponent(Fraction(3,5))))
print(c_sqrt(NumericalComponent(-6)))