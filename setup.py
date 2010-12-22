#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
seishub.plugins.exupery installer

:copyright:
    Robert Barsch (barsch@lmu.de)
:license:
    GNU Lesser General Public License, Version 3
    (http://www.gnu.org/copyleft/lesser.html)
"""

from setuptools import setup
import os


VERSION = open(os.path.join("seishub", "plugins", "exupery",
                            "VERSION.txt")).read()


setup(
    name='seishub.plugins.exupery',
    version=VERSION,
    description="Exupery package for SeisHub.",
    long_description="""
    seishub.plugins.exupery - Exupery package for SeisHub.

    For more information visit http://www.seishub.org.
    """,
    url='http://www.seishub.org',
    author='Robert Barsch',
    author_email='barsch@lmu.de',
    license='GNU Lesser General Public License, Version 3 (LGPLv3)',
    platforms='OS Independent',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ' + \
        'GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    keywords=['SeisHub', 'seismology'],
    packages=['seishub.plugins.exupery'],
    namespace_packages=['seishub', 'seishub.plugins'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'seishub.core',
        'obspy.core',
        'obspy.mseed',
        'obspy.gse2',
        'obspy.seishub',
        'obspy.imaging',
        'obspy.xseed',
        'obspy.arclink',
        'obspy.db',
    ],
    dependency_links=[
        "https://svn.obspy.org/obspy.db/trunk#egg=obspy.db-dev"
    ],
    download_url="https://svn.geophysik.uni-muenchen.de/svn/seishub/trunk/seishub.plugins.exupery#egg=seishub.plugins.exupery-dev",
    entry_points={'seishub.plugins': [
        'seishub.plugins.exupery = seishub.plugins.exupery', ]
    },
)
