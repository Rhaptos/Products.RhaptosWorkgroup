## Script (Python) "workgroup_members_remove_dispatch"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=groupname, delete
##title=Determine destination of member removal request
##

# used to be in 'prefs_group_members_edit'

group = context.portal_groups.getGroupById(groupname)

# Verify if deleting the workgroup
if len(delete) == len(group.getGroupMembers()):
    return state.set(status='delete')

# special confirm if just self leaving
if len(delete) == 1:
    me = context.portal_membership.getAuthenticatedMember().getId()
    if me in delete:
        return state.set(status='leave')

return state