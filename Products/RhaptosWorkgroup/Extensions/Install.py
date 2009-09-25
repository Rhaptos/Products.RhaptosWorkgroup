
from Products.CMFCore.utils import getToolByName

def install(portal):
    portal_setup = getToolByName(portal, 'portal_setup')
    import_context = portal_setup.getImportContextID()
    portal_setup.setImportContext('profile-RhaptosSite:rhaptos-default')
    portal_setup.setImportContext(
            'profile-Products.RhaptosWorkgroup:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(import_context)

