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
   
def load_pkg_dependencies():
    pkgDeps = list()
   
    if os.path.exists('requirements.txt'):
        reqsList = None
        with open('requirements.txt') as fp:
            reqsList = fp.readlines()
           
        if reqsList:
            for req in reqsList:
                reqSpec = req.strip()
                if reqSpec:
                    pkgDeps.append(reqSpec)
                   
    return pkgDeps  
   
pkg_dependencies = load_pkg_dependencies()
pkg_scripts = []
pkg_datalist = ['Conf/*.conf', 'version.txt']

setup(
    name=Sources.__name__,
        long_description=long_description,

   
    platforms=['Any'],
    scripts=pkg_scripts,
    provides=[],
    install_requires=pkg_dependencies,
    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,
    package_data={'Sources' : pkg_datalist},

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