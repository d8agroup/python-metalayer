#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="python-metalayer",
    version="0.0.1",
    description="Simple client for the MetaLayer data and image API.",
    author="Rich Schumacher",
    author_email="rich.schu@gmail.com",
    url="https://github.com/richid/python-metalayer",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "requests==0.13.6",
    ],
    keywords=["metalayer"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
