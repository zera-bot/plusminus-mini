import decimal
import fractions
import math
import cmath

pi = fractions.Fraction(decimal.Decimal("3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628"))
e = fractions.Fraction(decimal.Decimal("2.718281828459045235360287471352662497757247093699959574966967627724076630353547594571"))
inf = cmath.inf
infj = cmath.infj

def sqrt(x):
    return fractions.Fraction(decimal.Decimal(math.sqrt(x)))



