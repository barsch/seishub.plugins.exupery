# -*- coding: utf-8 -*-
"""
Exupery package for seishub.core.
"""

from seishub.core.core import Component, implements
from seishub.core.packages.interfaces import IPackage


class ExuperyPackage(Component):
    """
    Exupery package for seishub.core.
    """
    implements(IPackage)
    
    package_id = 'exupery'
    version = '0.1'
