from setuptools import setup, find_packages

setup(
    name='andante', 
    version='1.0', 
    packages=find_packages(),
    install_requires=[
        "parsimonious>=0.8.1",
        "dataclasses>=0.6",
        "ipywidgets>=7.6.5",
    ],
)
