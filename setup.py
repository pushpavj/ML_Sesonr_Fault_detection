from setuptools import find_packages,setup
from typing import List
import os 
import pandas as pd

def get_requirments()->List[str]:
    """
    This module returns the list of requirments to be installed.
    """

    requirement_list:List[str]=[]
    file=pd.read_table("requirements.txt",'r',header=None)
    for i in file:
       for j in file[i]:
        requirement_list.append(j)
    

    return requirement_list

setup(
    name="sensor",
    version="0.0.1",
    author="Pushpa",
    author_email="pushpapraketh@gmail.com",
    packages=find_packages(),
    install_requires=get_requirments()#["pymango==4.2.0"],
)