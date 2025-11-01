from setuptools import setup, find_packages
from typing import List

def get_requirements()->List[str]:
    """Reads the requirements.txt file and returns a list of dependencies."""
    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r')as file:
            lines=file.readlines()
            for line in lines:
                requirements=line.strip()
                if requirements and requirements!='-e .':
                    requirement_lst.append(requirements)
    except FileNotFoundError:
        print("requirements.txt file not found. No dependencies will be installed.")
    return requirement_lst
setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Divyanshi Goel",
    author_email="divyanshigoel1117@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)

