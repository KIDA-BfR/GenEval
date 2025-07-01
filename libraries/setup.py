from setuptools import setup, find_packages

setup(
    name="libraries",
    version="0.1",
    packages=find_packages(),
    description= "a library helping you checking if your data extraction is valid, by comparing it to a ground truth file.",
    long_description= open('README.md').read(),
    long_description_content_type= "text/markdown",
    author= "",
    author_email="",
    url="https://github.com/KIDA-BfR/GenEval.git",
    #don't know if it's the right access path
    classifiers= [
        "Programming Language:: ...",
        "License:: ...",
        "Operating System :: ...",
    ],
    python_requires= ">= ...",
)
