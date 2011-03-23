from AccessControl.SecurityInfo import ClassSecurityInfo
from Acquisition import aq_inner
from Acquisition import aq_parent
from App.class_init import InitializeClass
from App.special_dtml import DTMLFile
from OFS.Folder import Folder
from zope.interface import implements

from Products.CMFCore.utils import _dtmldir
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.permissions import ManagePortal

from Products.RhaptosWorkgroup.interfaces import IWorkgroupTool
from Products.RhaptosWorkgroup.permissions import AddWorkgroupFolder

class WorkgroupTool(UniqueObject, Folder):
    """ Tool to manage Rhaptos Workgroups
    """

    implements(IWorkgroupTool)

    id = 'portal_workgroups'
    meta_type = 'Rhaptos Workgroup Tool'

    security = ClassSecurityInfo()

    manage_options=(
        {'label' : 'Configuration', 'action' : 'manage_config'},
        ) + Folder.manage_options

    security.declareProtected(ManagePortal, 'manage_config')
    manage_mapRoles = DTMLFile('workgroupconfig', _dtmldir )

    def __init__(self, id=None):
        super(Folder, self).__init__(id)
        self._nextId = 0

    security.declarePublic('getWorkgroupsFolder')
    def getWorkgroupsFolder(self):
        """ Get the workgroups folder object.
        """
        parent = aq_parent( aq_inner(self) )
        workgroups = getattr(parent, 'workgroups', None)
        return workgroups

    security.declareProtected(AddWorkgroupFolder, 'createWorkgroupFolder')
    def createWorkgroupFolder(self):
        """ Create a workgroup folder
        """
        workgroups = self.getWorkgroupsFolder()
        nextId = self._getNextId()
        workgroups.invokeFactory(type_name='Workgroup', id=nextId)
        return nextId

    def _getNextId(self):
        """ return the next id for a workgroup
        """
        self._nextId += 1
        return 'wg%d' % self._nextId


InitializeClass(WorkgroupTool)
