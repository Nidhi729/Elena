import os

from setuptools import setup, find_packages

import Sources


pkg_scripts = []

setup(
    name=Sources.__name__,
        long_description='ELena',

   
    platforms=['Any'],
    scripts=pkg_scripts,
    provides=[],
    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,
    package_data={'Sources' : []},



    zip_safe=False,
)