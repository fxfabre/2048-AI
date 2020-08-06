#!/usr/bin/python3
# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext


setup(
    ext_modules = cythonize("AI_cython/ai_MC.pyx"),
    requires=['numpy', 'pandas']
)
