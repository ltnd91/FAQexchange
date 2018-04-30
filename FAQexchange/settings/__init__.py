from .base import *

# from .production import *

# try:
#    from .local import *
# except:
#    pass

"""
what is __init__.py?
https://stackoverflow.com/questions/448271/what-is-init-py-for

 Python searches a list of directories to resolve names in, e.g., import statements. Because these can be any directory, and arbitrary ones can be added by the end user, the developers have to worry about directories that happen to share a name with a valid Python module, such as 'string' in the docs example. To alleviate this, it ignores directories which do not contain a file named _ _ init _ _.py (no spaces), even if it is blank

 what is __pycache__ ?
https://stackoverflow.com/questions/16869024/what-is-pycache

When you run a program in python, the interpreter compiles it to bytecode first (this is an oversimplification) and stores it in the __pycache__ folder. If you look in there you will find a bunch of files sharing the names of the .py files in your project's folder, only their extensions will be either .pyc or .pyo. These are bytecode-compiled and optimized bytecode-compiled versions of your program's files, respectively.

As a programmer, you can largely just ignore it... All it does is make your program start a little faster. When your scripts change, they will be recompiled, and if you delete the files or the whole folder and run your program again, they will reappear (unless you specifically suppress that behavior)
"""