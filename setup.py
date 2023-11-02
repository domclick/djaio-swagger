#!/usr/bin/env python
import os
from setuptools import setup, find_packages

base = os.path.dirname(os.path.abspath(__file__))

install_requires = [
    'transmute-core==1.13.5',
    'PyYAML<=4',
    'swagger-schema==0.2.0',
]

tests_require = []

setup(name='djaio-swagger',
      version='0.0.10',
      description='The battery to generate additional swagger-spec json routes for '
                  'your ClassBasedView methods (get,post,put,delete). Based on aiothh-transmute app by Yusuke Tsutsumi.',
      author='Alexander Sivov',
      author_email='aasivov@sberned.ru',
      url='',
      packages=find_packages(),
      install_requires=install_requires,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Operating System :: MacOS',
          'Operating System :: POSIX :: Linux',
          'Topic :: System :: Software Distribution',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
      ],
      tests_require=tests_require
)
