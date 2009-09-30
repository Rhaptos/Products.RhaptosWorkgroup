
from Products.CMFCore.utils import getToolByName

redirectscriptcontents="return context.manageworkgroups()"

def setupWorkgroups(context):
    logger = context.getLogger('rhaptosworkgroup')
    if context.readDataFile('rhaptosworkgroup.txt') is None:
        logger.info('Nothing to import')
        return

    portal = context.getSite()
    portal_groups = getToolByName(portal, 'portal_groups')
    # turn on workspace creation
    portal_groups.groupWorkspacesCreationFlag = True
    # Create Group Workspaces folder if it doesn't exist
    wgfolder = portal_groups.getGroupWorkspacesFolder()
    if wgfolder is None:
        portal_groups.setGroupWorkspacesFolder('GroupWorkspaces', 'Workgroups')
        pt = getToolByName(portal, 'portal_types')
        pt.constructContent(
            type_name = 'Large Plone Folder',
            container = portal,
            id = portal_groups.getGroupWorkspacesFolderId(),
            )
        wgfolder = portal_groups.getGroupWorkspacesFolder()
        wgfolder.setTitle(portal_groups.getGroupWorkspacesFolderTitle())
        wgfolder.setDescription("Container for " + portal_groups.getGroupWorkspacesFolderId())

        portal_catalog = getToolByName(portal, 'portal_catalog')
        portal_catalog.unindexObject(wgfolder)



    # create default vew for GroupWorkspaces: 'manageworkgroups'
    logger.info('Set workgroups management page as workspaces folder default view')
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
    portal_groups.setGroupWorkspaceType('Workgroup')
    logger.info('Set groups tool to create Workgroup objects')

