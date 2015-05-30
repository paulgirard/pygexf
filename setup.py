#!/usr/bin/python
from setuptools import setup


setup(
    name='pygexf',
    version='0.2.2',
    py_modules=['gexf'],
    url='http://github.com/paulgirard/pygexf',
    author='Paul Girard',
    author_email='paul.girard@sciences-po.fr',
    license='GPL v3',
    install_requires=[
        'lxml',
    ],
    test_suite="tests",
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
)
