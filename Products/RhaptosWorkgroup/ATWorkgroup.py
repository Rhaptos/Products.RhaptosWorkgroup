"""
Rhaptos Workgroup - Shared, collaborative workspace

Author: J Cameron Cooper, Brent Hendricks
(C) 2007 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""
# based on Workgroup.py, but an Archetypes version

#TODO: tab actions

from AccessControl import ClassSecurityInfo

from Products.RhaptosWorkgroup.config import PROJECTNAME

from Products.CMFCore.permissions import View

from Products.Archetypes.public import ComputedField, StringWidget
from Products.Archetypes.public import Schema

from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.base import ATCTOrderedFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.ATContentTypes.lib.autosort import AutoOrderSupport
from Products.ATContentTypes.interfaces import IATFolder
from Products.RhaptosWorkgroup.interfaces import IWorkgroup
from zope.interface import implements

try:
    from Products.CMFBoardTab.config import forumname
except ImportError:
    forumname = None

ATWGSchema = ATFolderSchema.copy() + Schema((
    ComputedField('title',
              expression="context._getWorkgroupProperty('title')",
              searchable=True,
              accessor='Title',
              widget = StringWidget(
                        label= "Title",
                        label_msgid = "label_title",
                        i18n_domain = "plone")),
    ComputedField('email',
              expression="context._getWorkgroupProperty('email')",
              searchable=True,
              languageIndependent=True,
              widget = StringWidget(
                        description_msgid = "help_description",
                        description = "Email address for the group.",
                        label= "Email",
                        label_msgid = "label_email",
                        i18n_domain = "rhaptos")),
    ComputedField('description',
              expression="context._getWorkgroupProperty('description')",
              searchable=True,
              accessor="Description",
              widget = StringWidget(
                        description = "A short summary of the content",
                        label= "Description",
                        label_msgid = "label_description",
                        description_msgid="help_description",
                        i18n_domain = "plone")),
    ))
finalizeATCTSchema(ATWGSchema)

class ATWorkgroup(AutoOrderSupport, ATCTOrderedFolder):
    """A folder which can contain other items."""
    implements(IWorkgroup)

    schema         =  ATWGSchema

    content_icon   = 'group.gif'
    meta_type      = 'WorkgroupAT'
    portal_type    = 'Workgroup'
    archetype_name = 'Workgroup'
    immediate_view = 'workspace_contents'
    default_view   = 'workspace_contents'
    use_folder_tabs = 0
    #suppl_views    = ('folder_summary_view', 'folder_tabular_view', 'atct_album_view')
    _atct_newTypeFor = {'portal_type' : 'Old Workgroup', 'meta_type' : 'Workgroup'}
    typeDescription= 'A folder which can contain other items, with some group management features.'
    typeDescMsgId  = 'description_edit_workgroup'
    
    __implements__ = (ATCTOrderedFolder.__implements__, IATFolder,
                     AutoOrderSupport.__implements__)

    include_default_actions = False
    actions = (
               {'id': 'view',
                'name': 'Contents',
                'action': 'workspace_contents',
                'permissions': (View,)},
               {'id': 'properties',
                'name': 'Properties',
                'action': 'workgroup_properties',
                'permissions': (View,)},
               {'id': 'members',
                'name': 'Members',
                'action': 'workgroup_members',
                'permissions': (View,)},
              )
    filter_content_types = 1
    allowed_content_types = ('Module','UnifiedFile','Collection')
    
    aliases = {
        '(Default)'  : '(dynamic view)',
        'contents'   : 'workspace_contents',
        'properties' : 'workgroup_properties',
        'view'       : '(selected layout)',
        'index.html' : '(dynamic view)',
        'edit'       : 'workspace_contents',
        }
    
    # Enable marshalling via WebDAV/FTP/ExternalEditor.
    __dav_marshall__ = True

    security       = ClassSecurityInfo()

    def manage_afterAdd(self, item, container):
        ATCTOrderedFolder.manage_afterAdd(self, item, container)
        AutoOrderSupport.manage_afterAdd(self, item, container)
        
        #forum installation
        if forumname and not hasattr(item, forumname):
            item.manage_addProduct['CMFBoardTab'].addTabForum(forumname, title="Forum")

    def _getWorkgroupProperty(self, name):
        """ Get a property from the actual group object """
        try:
            g_tool = getToolByName(self, 'portal_groups')
            group = g_tool.getGroupById(self.getId())
            if group:
                return group.getProperty(name)
            #print "AT: no group found for %s" % self.getId()
        except AttributeError:
            pass
            #print 'AT: No portal_groups found on %s' % self
        return None

registerATCT(ATWorkgroup, PROJECTNAME)


# migration....

import logging
from cStringIO import StringIO

from Products.CMFCore.utils import getToolByName

from Products.ATContentTypes.migration.common import registerATCTMigrator
from Products.ATContentTypes.migration.common import migratePortalType
from Products.ATContentTypes.migration.migrator import CMFFolderMigrator
from Products.ATContentTypes.migration.walker import CatalogWalkerWithLevel

LOG = logging.getLogger('Workgroup.migration')

class WorkgroupMigrator(CMFFolderMigrator):
    walkerClass = CatalogWalkerWithLevel
    map = {}

registerATCTMigrator(WorkgroupMigrator, ATWorkgroup)

def migrateWGs(portal):
    """Migrate Workgroup to ATWorkgroup; largely stolen from ATCT.migration.atctmigrator"""
    LOG.debug('Starting ATWorkspace type migration')
    kwargs = {}

    atct = getToolByName(portal, 'portal_atct')
    kwargs['use_catalog_patch'] = bool(atct.migration_catalog_patch)
    kwargs['transaction_size'] = int(atct.migration_transaction_size)
    transaction = atct.migration_transaction_style
    if transaction == "full transaction":
        kwargs['full_transaction'] = True
        kwargs['use_savepoint'] = False
    elif transaction == "savepoint":
        kwargs['full_transaction'] = False
        kwargs['use_savepoint'] = True
    else:
        kwargs['full_transaction'] = False
        kwargs['use_savepoint'] = False

    out = StringIO()
    migrator = WorkgroupMigrator
    ## a loop in original...
    src_portal_type = migrator.src_portal_type
    dst_portal_type = migrator.dst_portal_type
    ttool = getToolByName(portal, 'portal_types')
    if (ttool.getTypeInfo(src_portal_type) is None or
        ttool.getTypeInfo(dst_portal_type) is None):

        LOG.debug('Missing FTI for %s or %s'%(src_portal_type, dst_portal_type))
        print >>out, ("Couldn't migrate src_portal_type due to missing FTI")
        #continue
    else:
        migratePortalType(portal, src_portal_type, dst_portal_type, out=out,
                          migrator=migrator, **kwargs)
    ##
    
    LOG.debug('Finished ATWorkgroup type migration')
    
    return out.getvalue()
