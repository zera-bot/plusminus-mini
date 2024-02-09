from comp import *
from methods import erf

lambdas = {
    "Frac": lambda p,q: p / q,
    "Power": lambda x,y: x**y,
    "Mod": lambda x,y: x % y,
    "Sqrt": lambda x: c_sqrt(x),
    "NthRoot": lambda x,y: x**(NumericalComponent(frac(1))/y), #yth root of x
    "LogBase": lambda x,base: c_log(x,base),
    "Ln": lambda x: c_ln(x),
    "Factorial": lambda x: c_factorial(x),
    "Abs": lambda x: abs(x),
    "Choose": lambda n,k: c_choose(n,k),
    "W": lambda x: c_W(x),
    "Erf": lambda x: erf(x),
    "Floor": lambda x: c_floor(x),
    "Ceil": lambda x: c_ceil(x),
    "Paren":lambda x: x, #parentheses

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

string_lambdas = {
    "Frac": lambda p,q: f"({p}/{q})",
    "Power": lambda x,y: f"({x}/{y})",
    "Mod": lambda x,y: f"({x}%{y})",
    "Sqrt": lambda x: f"(c_sqrt({x}))",
    "NthRoot": lambda x,y: f"({x}**(NumericalComponent(frac(1))/{y}))", #yth root of x
    "LogBase": lambda x,base: f"(c_sqrt({x},{base}))",
    "Ln": lambda x: f"(c_ln({x}))",
    "Factorial": lambda x: f"(c_factorial({x}))",
    "Abs": lambda x: f"(abs({x}))",
    "Choose": lambda n,k: f"(c_choose({n},{k}))",
    "W": lambda x: f"(c_W({x}))",
    "Erf": lambda x: f"(erf({x}))",
    "Floor": lambda x: f"(c_floor({x}))",
    "Ceil": lambda x: f"(c_ceil({x}))",
    "Paren":lambda x: f"({x})", #parentheses

    "acos": lambda x: f"(c_acos({x}))",
    "asin": lambda x: f"(c_asin({x}))",
    "atan": lambda x: f"(c_atan({x}))",
    "cos": lambda x: f"(c_cos({x}))",
    "sin": lambda x: f"(c_sin({x}))",
    "tan": lambda x: f"(c_tan({x}))",

    "acosh": lambda x: f"(c_acosh({x}))",
    "asinh": lambda x: f"(c_asinh({x}))",
    "atanh": lambda x: f"(c_atanh({x}))",
    "cosh": lambda x: f"(c_cosh({x}))",
    "sinh": lambda x: f"(c_sinh({x}))",
    "tanh": lambda x: f"(c_tanh({x}))",
}

numbersOfParameters = {
    "Frac": 2,
    "Power": 2,
    "Mod": 2,
    "Sqrt": 1,
    "NthRoot": 2,
    "LogBase": 2,
    "Ln": 1,
    "Factorial": 1,
    "Abs": 1,
    "Choose": 2,
    "W": 1,
    "Erf": 1,
    "Floor": 1,
    "Ceil": 1,
    "Paren": 1,

    "acos": 1,
    "asin": 1,
    "atan": 1,
    "cos": 1,
    "sin": 1,
    "tan": 1,

    "acosh": 1,
    "asinh": 1,
    "atanh": 1,
    "cosh": 1,
    "sinh": 1,
    "tanh": 1,

    "X": 1,
    "Y": 1,
    "Z": 1,
}

functionDelimiters = ["Ln","W","acos","asin","atan",
                      "cos","sin","tan","acosh","asinh","atanh",
                      "cosh","sinh","tanh","Erf"]
