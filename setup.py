import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="maplapse",
    version="0.0.6b1",
    author="Sourav Bhadra",
    author_email='sbhadra019@gmail.com',
    description="A python library to create animated timelapse of maps",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url='https://github.com/souravbhadra/maplapse',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',    
    py_modules=["maplapse"],
    install_requires=read('requirements.txt').splitlines()
)