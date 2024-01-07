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

def convertToNumericalComponent(number):
    if isinstance(number,int) or isinstance(number,float):
        return NumericalComponent(Fraction(number))
    elif isinstance(number,Fraction):
        return NumericalComponent(number)
    elif isinstance(number,complex):
        return NumericalComponent(Fraction(number.real),Fraction(number.imag))
    elif isinstance(number,NumericalComponent):
        return number
        

class Variable:
    def __init__(self,symbol:str):
        self.symbol = symbol

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return str(self)

class NumericalComponent:
    def __init__(self, real=frac(0), imaginary=frac(0), pi_multiple=frac(0), sqrt_components=[]):
        if not isinstance(real,Fraction):
            real = Fraction(real)
        if not isinstance(imaginary,Fraction):
            imaginary = Fraction(imaginary)
        if not isinstance(pi_multiple,Fraction):
            pi_multiple = Fraction(pi_multiple)
        for i in sqrt_components:
            if not isinstance(i[0],Fraction):
                i[0]=Fraction(i[0])
            if not isinstance(i[1],Fraction):
                i[1]=Fraction(i[1])
        
        self.real = real
        self.pi_multiple = pi_multiple

        #remove duplicate square root components again which is important

        sqrt_components = removeDuplicatesInSqrtComponents(sqrt_components)

        #remove non-whole number sqrts
        for r in sqrt_components:
            if r[1] % 1 != frac(0):
                if r[1]>=0: #if negative
                    self.real+=r[0]*xmath.sqrt(r[1])
                    sqrt_components.remove(r)
                elif r[1]<0:
                    imaginary += r[0] * xmath.sqrt(abs(r[1]))
                    sqrt_components.remove(r)

        #simplify fully
        for r in sqrt_components:
            if r[1] == 0:
                sqrt_components.remove(r)
            elif r[1] < 0:
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

    def __pos__(self):
        return self

    def __neg__ (self):
        return NumericalComponent(frac(-1))*self

    def __add__(self,other):
        self,other = convertToNumericalComponent(self),convertToNumericalComponent(other)
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
        self,other = convertToNumericalComponent(self),convertToNumericalComponent(other)
        sum = NumericalComponent(self.real-other.real,
                                  self.imaginary-other.imaginary,
                                  self.pi_multiple-other.pi_multiple)
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
        self,other = convertToNumericalComponent(self),convertToNumericalComponent(other)
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
        self,other = convertToNumericalComponent(self),convertToNumericalComponent(other)
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
            selfRealComponent = self.real
            otherRealComponent = other.real

            if self.pi_multiple != 0 or len(self.sqrt_components)>0:
                selfRealComponent = complex(self).real
            if other.pi_multiple != 0 or len(other.sqrt_components)>0:
                otherRealComponent = complex(other).real

            a = selfRealComponent
            b = self.imaginary
            c = otherRealComponent
            d = other.imaginary

            mainSum = NumericalComponent(
                (a*c + b*d)/(c**2 + d**2),
                (b*c - a*d)/(c**2 + d**2)
            )
            
            #mainSum = self * (other**-1)

        return mainSum

    def __pow__(self,other):
        self,other = convertToNumericalComponent(self),convertToNumericalComponent(other)
        val = complex(self) ** complex(other)
        return NumericalComponent(Fraction(val.real),Fraction(val.imag))

    def __mod__(self,other):
        self,other = convertToNumericalComponent(self),convertToNumericalComponent(other)
        return self-other*(c_floor(self/other))

    #binary operator

    def __eq__(self,other):
        self,other = convertToNumericalComponent(self),convertToNumericalComponent(other)
        v0 = self.real == other.real
        v1 = self.imaginary == other.imaginary
        v2 = self.pi_multiple == other.pi_multiple

        self.sqrt_components.sort()
        other.sqrt_components.sort()
        v3 = self.sqrt_components==other.sqrt_components

        return v0 and v1 and v2 and v3

    #with incompatible types

    def __radd__(self,other):
        return convertToNumericalComponent(self)+convertToNumericalComponent(other)
    
    def __rsub__(self,other):
        return convertToNumericalComponent(other)-convertToNumericalComponent(self)
    
    def __rmul__(self,other):
        return convertToNumericalComponent(self)*convertToNumericalComponent(other)
    
    def __rtruediv__(self,other):
        return convertToNumericalComponent(other)/convertToNumericalComponent(self)
    
    def __rpow__(self,other):
        return convertToNumericalComponent(other)**convertToNumericalComponent(self)
    
    def __rmod__(self,other):
        return convertToNumericalComponent(other)%convertToNumericalComponent(self)

    def __req__(self,other):
        return convertToNumericalComponent(self) == convertToNumericalComponent(other)

    #display

    def __str__(self):
        s = []
        if self.real != frac(0): s.append(str(self.real))
        if self.imaginary != frac(0): s.append(str(self.imaginary)+"i")
        if self.pi_multiple != frac(0): s.append(str(self.pi_multiple)+"pi")
        for r in self.sqrt_components:
            s.append(f"{r[0]}sqrt({r[1]})")

        r = " + ".join(s)
        if r == "": r = "0"
        return r.replace("+ -","- ")

    def __repr__(self):
        return str(self)

    #other

    def __abs__(self):
        k = complex(self)
        return NumericalComponent(xmath.sqrt(k.real**2 + k.imag**2))

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

def c_floor(x):
    x = complex(x)
    x = complex(math.floor(x.real),math.floor(x.imag))
    return NumericalComponent(Fraction(x.real),Fraction(x.imag))

def c_ceil(x):
    x = complex(x)
    x = complex(math.ceil(x.real),math.ceil(x.imag))
    return NumericalComponent(Fraction(x.real),Fraction(x.imag))

def c_log(x,base=xmath.e):
    base = complex(base)
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
    if not x.isOnlyRationalReal(): raise TypeError
    if x.real % 1 == frac(0) and x.real >= 0:
        return NumericalComponent(frac(math.factorial(int(x.real))))
    else:
        raise TypeError

def c_choose(n:NumericalComponent,k:NumericalComponent):
    try:
        return c_factorial(n) / ( c_factorial(k) * c_factorial(n-k))
    except TypeError:
        return NumericalComponent()

def c_W(n:NumericalComponent):
    c = ( n / ( NumericalComponent(frac(1)) + n) )
    ans = c * ( ( NumericalComponent(frac(1)) + NumericalComponent(frac(2))*n ) / ( n + NumericalComponent(xmath.e)**(c) ) )
    approxAns = complex(ans)
    return NumericalComponent(Fraction(approxAns.real),Fraction(approxAns.imag))

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

def tortureTest():
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

tortureTest()