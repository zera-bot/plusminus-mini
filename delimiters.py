from comp import *

delims = {
    "Frac": lambda p,q: p / q,
    "Power": lambda x,y: x**y,
    "Mod": lambda x,y: x % y,
    "Sqrt": lambda x: c_sqrt(x),
    #continue this later
}