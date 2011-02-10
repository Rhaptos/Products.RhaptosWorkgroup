
from Products.CMFCore.utils import getToolByName

redirectscriptcontents="return context.manageworkgroups()"

def setupWorkgroups(context):
    logger = context.getLogger('rhaptosworkgroup')
    if context.readDataFile('rhaptosworkgroup.txt') is None:
        logger.info('Nothing to import')
        return

    portal = context.getSite()
    portal.invokeFactory(type_name='Folder', id='groups', title='Workgroups')
