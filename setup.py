#!/usr/bin/env python
import os
# import glob

from setuptools import setup, find_packages

import Sources

#import ProfileManager

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''
   

   
pkg_scripts = []

setup(
    name=Sources.__name__,
        long_description=long_description,

   
    platforms=['Any'],
    scripts=pkg_scripts,
    provides=[],
    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,
    package_data={'Sources' : []},

#     entry_points={
#         'console_scripts': [
#             'profilemanager = ProfileManager.Apps.ProfileManagerApp:main'
#         ],
#         'ProfileManager.commands': [
#             'restserver = ProfileManager.Commands.RestServer:RestServer',
#             'daemon = ProfileManager.Commands.TestGroupGenerator:TestGroupGenerator'
#         ],
#     },

    zip_safe=False,
)