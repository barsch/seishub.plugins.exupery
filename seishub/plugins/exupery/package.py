# -*- coding: utf-8 -*-
"""
Exupery package for SeisHub.
"""

from seishub.core import Component, implements
from seishub.packages.interfaces import IPackage


class ExuperyPackage(Component):
    """
    Exupery package for SeisHub.
    """
    implements(IPackage)
    
    package_id = 'exupery'
    version = '0.1'
