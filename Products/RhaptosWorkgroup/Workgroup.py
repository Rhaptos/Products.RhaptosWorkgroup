"""
Rhaptos Workgroup - Shared, collaborative workspace

Author: Brent Hendricks
(C) 2002 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

from OFS.Folder import Folder
from Globals import InitializeClass
from AccessControl import getSecurityManager, ClassSecurityInfo
from AccessControl.Permissions import view
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from ComputedAttribute import ComputedAttribute

from Products.CMFDefault.DublinCore import DefaultDublinCoreImpl
from Products.CMFPlone.PloneFolder import PloneFolder
from Products.CMFDefault.SkinnedFolder import SkinnedFolder

# Import permission names
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.CMFCorePermissions import View, ManageProperties, ListFolderContents
from Products.CMFCore.utils import getToolByName

try:
    from Products.CMFBoardTab.config import forumname
except ImportError:
    forumname = None
    
def manage_addWorkgroup(self, id, title='', desc='', REQUEST=None):
    """Add a new Workgroup object to the context"""

    id = str(id)
    desc = str(desc)

    self = self.this()
    self._setObject(id, Workgroup(id, desc))
    
    # If this was a TTW request, jump back to the management page
    if REQUEST is not None:
        REQUEST.RESPONSE.redirect(self.absolute_url()+'/manage_main')


factory_type_information = (
    {'id': 'Workgroup',
     'content_icon': 'group.gif',
     'meta_type': 'Workgroup',
     'description': ('A Workgroup Folder'),
     'product': 'RhaptosWorkgroup',
     'factory': 'manage_addWorkgroup',
     'filter_content_types' : 0,
     'immediate_view': 'workspace_contents',
     'actions': ({'id': 'view',
                  'name': 'Contents',
                  'action': 'workspace_contents',
                  'permissions': (CMFCorePermissions.View,)},
                 {'id': 'properties',
                  'name': 'Properties',
                  'action': 'workgroup_properties',
                  'permissions': (CMFCorePermissions.View,)},
                 {'id': 'members',
                  'name': 'Members',
                  'action': 'workgroup_members',
                  'permissions': (CMFCorePermissions.View,)},
                 ),
     },
    )

class Workgroup(PloneFolder, DefaultDublinCoreImpl):
    """ Workgroup class

        This defines a workspace for collaborative content authoring"""

    __implements__ = PloneFolder.__implements__

    title = ComputedAttribute(lambda self: self._getWorkgroupProperty('title'), 1)
    email = ComputedAttribute(lambda self: self._getWorkgroupProperty('email'), 1)
    description = ComputedAttribute(lambda self: self._getWorkgroupProperty('description'), 1)

    meta_type = "Workgroup"

    security = ClassSecurityInfo()


    def __init__(self, id, desc):
        """Workgroup constructor"""
        DefaultDublinCoreImpl.__init__(self)
        self.id = id

    def manage_afterAdd(self, item, container):
        """Set permissions for the community"""
        PloneFolder.manage_afterAdd(self, item, container)
        
        #forum installation
        if forumname and not hasattr(item, forumname):
            item.manage_addProduct['CMFBoardTab'].addTabForum(forumname, title="Forum")

    def _getWorkgroupProperty(self, name):
        """ Get a property from the actual group object """
        g_tool = getToolByName(self, 'portal_groups')
        group = g_tool.getGroupById(self.getId())
        if group:
            return group.getProperty(name)
        #import pdb; pdb.set_trace()
        #print "old: no group found for %s" % self.getId()
        return None

    def setTitle(self, title):
        """ Bogus setTitle method since we don't really want to use it """
        pass


    def setDescription(self, title):
        """ Bogus setDescription method since we don't really want to use it """
        pass

        
    def emailMember(self, toAddresses, fromAddress, subject, body):
        """Send an email to group members"""

        toAddresses = ",".join(toAddresses)
        self.accounts.sendEmail(body, toAddresses, fromAddress, subject)
        self.REQUEST.RESPONSE.redirect('.')

    def getWorkgroupId(self):
	"""Return Id of workgroup, for aquisition use"""
        return self.getId()

    # Set default roles for these permissions
    security.setPermissionDefault('Edit Workgroup', ('Manager', 'Owner',))


InitializeClass(Workgroup)

