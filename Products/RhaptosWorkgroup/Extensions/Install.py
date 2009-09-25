__version__ = "0.1"

from Products.CMFCore.TypesTool import ContentFactoryMetadata
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.Expression import Expression

from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.Archetypes.public import listTypes

from Products.RhaptosWorkgroup.config import PROJECTNAME, GLOBALS

from cStringIO import StringIO
import string

import logging
logger = logging.getLogger('RhaptosWorkgroup.Install')
def log(msg, out=None):
    logger.info(msg)
    if out: print >> out, msg

redirectscriptcontents="return context.manageworkgroups()"

def isOldInUse(self):
    """Query if old CMF type is disabled
    """
    ttool = getToolByName(self, 'portal_types')
    if 'Workgroup' in ttool.objectIds():
        meta_type = getattr(ttool, 'Workgroup').Metatype()
        if meta_type == 'Workgroup':
            return True
    return False


def install(self):
    """Register RhaptosWorkgroup with the necessary tools"""
    out = StringIO()
    portal = self.portal_url.getPortalObject()
    groups_tool = getToolByName(portal, 'portal_groups')

    # setup tool prep (see also RhaptosSite install)
    setup_tool = getToolByName(portal, 'portal_setup')
    prevcontext = setup_tool.getImportContextID()
    setup_tool.setImportContext('profile-CMFPlone:plone')  # get Plone steps registered
    setup_tool.setImportContext('profile-RhaptosSite:rhaptos-default')  # Rhaptos steps registered (FormController)
    setup_tool.setImportContext('profile-RhaptosWorkgroup:rhaptos-default')  # use profile from this product
    
    # skins
    log('Installing skin layers', out)
    install_subskin(self, out, GLOBALS)

    # turn on workspace creation
    groups_tool.groupWorkspacesCreationFlag = True
    wgfolder = groups_tool.getGroupWorkspacesFolder()
    # Create Group Workspaces folder if it doesn't exist
    if wgfolder is None:
        pt = getToolByName(portal, 'portal_types')
        pt.constructContent(
            type_name = 'Large Plone Folder',
            container = portal,
            id = groups_tool.getGroupWorkspacesFolderId(),
            )
        wgfolder = groups_tool.getGroupWorkspacesFolder()
        wgfolder.setTitle(groups_tool.getGroupWorkspacesFolderTitle())
        wgfolder.setDescription("Container for " + groups_tool.getGroupWorkspacesFolderId())

        portal_catalog = getToolByName(portal, 'portal_catalog')
        portal_catalog.unindexObject(wgfolder)



    # create default vew for GroupWorkspaces: 'manageworkgroups'
    log('Set workgroups management page as workspaces folder default view', out)
    # following is better, but won't work as CMF BTree Folder isn't a TypeInfo with dynamic views
    #wgfolder.layout = 'manageworkgroups'
    if not 'index_html' in wgfolder.objectIds():
        wgfolder.manage_addProduct['PythonScripts'].manage_addPythonScript('index_html')
        redirectscript = getattr(wgfolder, 'index_html', None)
        redirectscript.manage_role('Anonymous', ['View'])
    else:
        redirectscript = wgfolder['index_html']
    if redirectscript.meta_type == 'Script (Python)':
        redirectscript.ZPythonScript_edit(params='', 
                body=redirectscriptcontents)
    
    # Configure the groups tool
    groups_tool.setGroupWorkspaceType('Workgroup')
    log('Set groups tool to create Workgroup objects', out)

    # make workflow go away
    log("Making workflow empty", out)
    wf_tool=getToolByName(portal,'portal_workflow')
    wf_tool.setChainForPortalTypes(['Workgroup'],'')

    # move aside old type to 'Old Workgroup'
    needMigrate = isOldInUse(portal)
    if needMigrate:
        log("Moving aside old Workgroup type", out)
        atct = portal.portal_atct
        atct._changePortalTypeName('Workgroup', 'Old Workgroup')

    # install new types
    log("Installing current type(s)", out)
    installTypes(portal, out,
                 listTypes(PROJECTNAME),
                 PROJECTNAME,
                 refresh_references=0
                 )

    # Setting up FormController customizations
    # modify and add by way of Generic Setup XML profile
    log("...setting up form controller actions", out)
    log(" - applying profile", out)
    status = setup_tool.runImportStep('rhaptos_cmfformcontroller')
    log(status['messages']['rhaptos_cmfformcontroller'], out)
    
    # migrate if needed
    if needMigrate:
        log("Migrating workgroup objects", out)
        from Products.RhaptosWorkgroup.ATWorkgroup import migrateWGs
        migrateWGs(portal)
        
    # setup tool "teardown"
    setup_tool.setImportContext(prevcontext)

    log("Done.", out)
    return out.getvalue()

