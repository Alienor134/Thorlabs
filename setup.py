import os
import sys

from setuptools import setup, find_packages

install_requires=[
]

setup(
    name='ThorlabsControl',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A package to control Thorlabs hardware',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/ThorlabsControl',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True,
)
