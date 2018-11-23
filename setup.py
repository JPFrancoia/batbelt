#!/usr/bin/python
# coding: utf-8

"""
Tutorials on how to create a lib:
http://sametmax.com/creer-un-setup-py-et-mettre-sa-bibliotheque-python-en-ligne-sur-pypi/
http://peterdowns.com/posts/first-time-with-pypi.html
https://github.com/SolidCode/SolidPython/blob/master/setup.py
"""

from setuptools import setup, find_packages

setup(
    name="batbelt",
    version="1.0",
    description="Personal tools useful in Batman-tricky situations",
    author="Jean-Patrick Francoia",
    author_email="jeanpatrick.francoia@gmail.com",
    url="https://github.com/JPFrancoia/batbelt",
    include_package_data=True,
    py_modules=["batbelt"],
    packages=find_packages(),
    install_requires=["numpy", "xlrd", "xlwt"],
)
