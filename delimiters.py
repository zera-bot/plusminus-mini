from comp import *

lambdas = {
    "Frac": lambda p,q: p / q,
    "Power": lambda x,y: x**y,
    "Mod": lambda x,y: x % y,
    "Sqrt": lambda x: c_sqrt(x),
    "NthRoot": lambda x,y: x**(NumericalComponent(frac(1))/y), #yth root of x
    "LogBase": lambda x,base: c_log(x,base),
    "Ln": lambda x: c_ln(x),
    "Factorial": lambda x: c_factorial(x),
    "Choose": lambda n,k: c_choose(n,k),
    "W": lambda x: c_W(x),
    "Floor": lambda x: c_floor(x),
    "Ceil": lambda x: c_ceil(x),

    "acos": lambda x: c_acos(x),
    "asin": lambda x: c_asin(x),
    "atan": lambda x: c_atan(x),
    "cos": lambda x: c_cos(x),
    "sin": lambda x: c_sin(x),
    "tan": lambda x: c_tan(x),

    "acosh": lambda x: c_acosh(x),
    "asinh": lambda x: c_asinh(x),
    "atanh": lambda x: c_atanh(x),
    "cosh": lambda x: c_cosh(x),
    "sinh": lambda x: c_sinh(x),
    "tanh": lambda x: c_tanh(x),

    "X": lambda x: Variable("x"),
    "Y": lambda x: Variable("y"),
    "Z": lambda x: Variable("z"),
}