from Cython.Build import cythonize
from distutils.core import setup

setup(ext_modules=cythonize("AI_cython/ai_MC.pyx"), requires=["numpy", "pandas"])
