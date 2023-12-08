import xmath
import math

from decimal import Decimal as dm
from copy import deepcopy as dc

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
    def __init__(self, real=dm(0), imaginary=dm(0), pi_multiple=dm(0), sqrt_components=[]):
        self.real = real
        
        self.pi_multiple = pi_multiple
        #remove duplicates first
        #simplify each sqrt component
        #remove duplicate square root components again which is important

        sqrt_components = removeDuplicatesInSqrtComponents(sqrt_components)

        #simplify fully
        for r in sqrt_components:
            if r[1] < 0:
                imaginary += r[0] * xmath.sqrt(abs(r[1]))
            elif xmath.sqrt(r[1]) % 1 == dm(0):
                sqrt_components.remove(r)
                self.real+=xmath.sqrt(r[1])*r[0]
            else:
                for factor_root in range(int(math.sqrt(r[1])), 1, -1):
                    factor = factor_root ** 2
                    if r[1] % factor == 0:
                        reduced = r[1] // factor
                        sqrt_components.remove(r)
                        sqrt_components.append([dm(factor_root)*r[0],dm(reduced)])

        self.imaginary = imaginary
        sqrt_components = removeDuplicatesInSqrtComponents(sqrt_components)

        self.sqrt_components = removeDuplicatesInSqrtComponents(sqrt_components)
        #each sqrt component is laid out as [multiple,value]


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
        rowThreeSum = dm(0)
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
        return "Not done Yet!"
    
    def __pow__(self,other):
        val = self.getDecimalValue() ** other.getDecimalValue()
        return NumericalComponent(val.real,val.imag)
    
    def getDecimalValue(self):
        v = complex(self.real+(xmath.pi*self.pi_multiple),self.imaginary)
        for w in self.sqrt_components:
            v += complex(w[0]*xmath.sqrt(w[1]),0)
        return v

    def __str__(self):
        s = []
        if self.real != dm(0): s.append(str(self.real))
        if self.imaginary != dm(0): s.append(str(self.imaginary)+"i")
        if self.pi_multiple != dm(0): s.append(str(self.pi_multiple)+"pi")
        for r in self.sqrt_components:
            s.append(f"{r[0]}sqrt({r[1]})")

        return " + ".join(s)

a = NumericalComponent(dm(3),dm(4),dm(4),[[dm(2),dm(3)]])
b = NumericalComponent(dm(-1),dm(3),dm(-4),[[dm(2),dm(3)],[dm(4),dm(5)]])

#print(a*b)
#print((a*b).getDecimalValue())
print(a**b)