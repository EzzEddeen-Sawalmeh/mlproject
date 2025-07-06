from setuptools import setup, find_packages
from typing import List

def get_requierments(file_path:str)->List[str]:
    '''
    this function will return a list of requierments
    '''
    requierments = []
    with open(file_path) as file_obj:
        requierments = file_obj.readlines()
        requierments = [req.replace("\n", "") for req in requierments]

        if '-e .' in requierments:
            requierments.remove('-e .')

setup(
    name='mlproject',
    version='0.1',
    author='EzzEdddeen',
    packages=find_packages(),
    install_requires=get_requierments('requierments.txt')
)
