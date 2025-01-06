import os
import sys

from setuptools import setup, Extension, find_packages

install_requires=[
]

#and PyQt5


s = setup(
    name='ThorlabsControl',
    version='0.0.1',
    #scripts=[],
    packages=find_packages(),
    author='Alienor Lahlou',
    author_email='alienor.lahlou@espci.org',
    description='Thorlab instrument control via Python',
    long_description='',
    url = 'TODO',
    install_requires=install_requires,
    include_package_data=True,
)
