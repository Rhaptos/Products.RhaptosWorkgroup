## Script (Python) "workgroup_members_remove.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=groupname, delete
##title=Workgroup members remove
##

group = context.portal_groups.getGroupById(groupname)
delete_self = 0

me = context.portal_membership.getAuthenticatedMember().getId()
if me in delete:
    state.set(status='left')

map(group.removeMember, delete)

psm = context.translate("message_workgroup_members_removed", domain="rhaptos", default="Members removed.")
return state.set(portal_status_message=psm)
