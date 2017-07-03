#!/usr/bin/env python
# -*- coding:utf-8 -*-

#   Copyright 2016 Takashi Ando - http://blog.rinka-blossom.com/
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import glob
import os
from setuptools import setup, find_packages


def readme():
    try:
        readme_ = os.path.join(os.path.dirname(__file__), 'README.rst')
        with open(readme_, 'r') as f:
            return f.read()
    except:
        return ''


def requires():
    try:
        packages = []

        for text in glob.glob(os.path.join(os.path.dirname(__file__), "requirements*.txt")):
            with open(text, 'r') as f:
                lines.extend(f.readlines())

        return packages
    except:
        return []


setup(
    name='necco_passbook',
    version='0.1.0',
    description='necco passbook web server application',
    long_description=readme(),
    license="Apache Software License",
    author='Takashi Ando',
    url='https://github.com/dodo5522/necco.git',
    install_requires=requires(),
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'necco = necco.__main__:main'
        ]
    },
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: Japanese',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)

