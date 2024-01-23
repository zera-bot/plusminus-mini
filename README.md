# PlusMinus Mini
[<img src="https://i.ibb.co/fS61ZgD/untitled-1.png" width="250" align="middle"/>](image.png)

PlusMinus Mini is a numerical computation system. Its ultimate goal is to be written in pure Python without any libraries installed via pip.
A physical scientific calculator model may be possible in the near future.

## Features
PlusMinus Mini is equipped with the features required for a physical system- a computation engine, an expression tokenizer and parser, and a textbook display expression renderer. 
There are many implemented computation functions including methods involving calculus and regression:
### comp.py
- Precision only limited by Python's Fraction object
- Complex Numbers
- Standard Functions (Logarithmic functions, Trigonometric Functions, Absolute Value, Factorial, Choose Function, )
- Lambert W Function
- Error Function
### methods.py
- Solvers for Quadratic, Cubic, and Quartic functions
- Numerical Root Solving
- Linear Regression
- Derivatives at $x=n$
- Definite Integrals
- Summation and Product Evaluation

PlusMinus Mini has a tokenizer and parser system that will convert expressions from string form to a list of tokens or a parsed expression (warning: uses `eval()`). 
It also has a renderer that can render expressions of the same string format to an array of points similar to how expressions would be written by hand. 

![image 5](tortureTest/5.png) ![image 7](tortureTest/7.png) ![image 8](tortureTest/8.png) ![image 12](tortureTest/12.png) ![image 17](tortureTest/17.png) ![image 26](tortureTest/26.png) 

You can see more of this in [the renderer torture test folder.](/tortureTest)

PlusMinus Mini is also equipped with the file `system.py`, which is a calculation system that may be useful for operating the calculator's functions. Inputs can call a function and, 
from the current state of the data, the screen will be modified accordingly.
A "demo" can be seen in [the system torture test folder.](/systemTortureTest)
## What should I take?
- Want the whole system? Sure, go for it!
- You just need the main computational stuff? Try taking `comp.py`, `xmath.py`, and (optional) `methods.py`.
- Want to be able to write and parse expressions in the math string format? Also take `mathcode.py`, `tokenizer.py`, and `delimiters.py`.
- To start rendering, you'll need the computational stuff and `render.py`, `renderformats.py`, `tokenizer.py`, and `delimiters.py`.
