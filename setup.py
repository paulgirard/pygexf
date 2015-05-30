#!/usr/bin/python
from setuptools import setup


setup(
    name='pygexf',
    version='0.2.2',
    packages=['gexf'],
    url='http://github.com/paulgirard/pygexf',
    author='Paul Girard',
    author_email='paul.girard@sciences-po.fr',
    license='',
    install_requires=[
        'lxml',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
)
