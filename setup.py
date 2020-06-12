
from setuptools import setup, find_packages


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="rwmem",
    version="0.0.7",
    description="A Simple Read/Write Memory module for Windows python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Oseid Aldary",
    author_email="oseid.eng@gmail.com",
    url='https://github.com/Oseid/rwmem',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
    ],
)
