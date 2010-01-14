## Script (Python) "getWorkGroupMembers"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title= Return a list of members in the workgroup

group_name = context.getId()
group = context.portal_groups.getGroupById(group_name)
members = group.getGroupMembers()

return members
