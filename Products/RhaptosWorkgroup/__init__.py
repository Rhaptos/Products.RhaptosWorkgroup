"""
Initialize RhaptosWorkgroup Product

Author: Brent Hendricks and J. Cameron Cooper
(C) 2005 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

from Products.CMFDefault import Portal
from Products.CMFCore import utils, CMFCorePermissions
from Products.CMFCore.DirectoryView import registerDirectory

from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils

from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

from config import PROJECTNAME, ADD_CONTENT_PERMISSION

import Workgroup
import ATWorkgroup

import monkeypatch

import sys
this_module = sys.modules[ __name__ ]

contentConstructors = (Workgroup.manage_addWorkgroup,)
contentClasses = (Workgroup.Workgroup,)

product_globals = globals()

z_bases = utils.initializeBasesPhase1(contentClasses, this_module)

# Make the skins available as DirectoryViews
registerDirectory('skins', globals())

def initialize(context):
    """Register"""

    utils.initializeBasesPhase2( z_bases, context )
    utils.ContentInit(Workgroup.Workgroup.meta_type,
                      content_types = contentClasses,
                      permission = CMFCorePermissions.AddPortalContent,
                      extra_constructors = contentConstructors,
                      fti = Workgroup.factory_type_information).initialize(context)
    
    # AT types
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

