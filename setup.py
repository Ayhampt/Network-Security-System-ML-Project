from setuptools import setup, find_packages
from typing import List

REQUIREMENT_FILE_NAME = "requirements.txt"
HYPHEN_E_DOT = "-e ."


def get_requirements(file_path: str) -> List[str]:
    """This function will return the list of requirements"""
    requirements = []
    with open(file_path) as obj_file:
        requirements = obj_file.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements


setup(
    name="Network Security Project",
    version="0.0.1",
    author="Ayham",
    packages=find_packages(),
    install_requires=get_requirements(REQUIREMENT_FILE_NAME),
)
