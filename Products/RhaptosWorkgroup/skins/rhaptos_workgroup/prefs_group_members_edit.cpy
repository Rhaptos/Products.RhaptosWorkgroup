## Script (Python) "prefs_group_members_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=groupname, ids
##title=Add group members
##

# CNX note: moved to FormController
# used to also delete, now only adds

add = ids
group = context.portal_groups.getGroupById(groupname)
map(group.addMember, add)

psm = context.translate("message_workgroup_membership_updated", domain="rhaptos", default="Membership updated.")
return state.set(status='success', portal_status_message=psm, context=context)
