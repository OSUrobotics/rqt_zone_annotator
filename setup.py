#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['rqt_zone_annotator'],
    scripts=['scripts/rqt_zone_annotator'],
    package_dir={'': 'src'},
    install_requires=['rospkg'],
    )

setup(**d)
