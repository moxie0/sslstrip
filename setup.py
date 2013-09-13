#!/usr/bin/env python
from setuptools import setup, find_packages

setup  (
    name        = 'sslstrip',
    version     = '0.9.2',
    description = 'A MITM tool that implements Moxie Marlinspike\'s HTTPS stripping attacks.',
    author = 'Moxie Marlinspike',
    author_email = 'moxie@thoughtcrime.org',
    url = 'https://github.com/graingert/sslstrip/',
    license = 'GPL',
    packages  =  find_packages('src'),
    package_dir = {'' : 'src'},
    entry_points = {
        'console_scripts': [
            'sslstrip = sslstrip.sslstrip:_main',
        ],
    },
    install_requires = [
        'Twisted==13.1.0',
        'pyOpenSSL==0.13.1',
    ]
)