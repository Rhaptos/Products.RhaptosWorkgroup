import logging

logger = logging.getLogger('RhaptosWorkgroup')

## Monkeypatch GroupDataTool to allow group members to add members to the group
## (any more than this, and we'd want to make a new tool)

from Products.PlonePAS.tools.groupdata import GroupData

    
if not hasattr(GroupData, 'RhaptosWorkgroup_adminGroup_patch'):
    logger.debug("Monkey patch: RhaptosWorkgroup on PlonePAS.tools.groupdata.GroupData.canAdministrateGroup")
   
    GroupData.RhaptosWorkgroup_adminGroup_patch = 1

    from Products.PlonePAS.tools.groupdata import *     # get all the original's imports and definitions
    from AccessControl import getSecurityManager
   
    def canAdministrateGroup(self):
        """
        Return true if the #current# user can administrate this group
        """
        #import pdb; pdb.set_trace()
        user = getSecurityManager().getUser()
        userid = user.getId()
        members = self.getGroupMembers()
        memberids = [m.getId() for m in members]
        
        if userid in memberids:         # member of group: OK
            return True
        elif not memberids:             # first member of group: OK
            return True
        else:                           # then check normal mechanisms
            return self._orig_canAdministrateGroup()

    
    GroupData._orig_canAdministrateGroup= GroupData.canAdministrateGroup
    GroupData.canAdministrateGroup= canAdministrateGroup
