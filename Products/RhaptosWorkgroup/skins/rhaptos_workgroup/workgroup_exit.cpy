## Script (Python) "workgroup_exit.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Workgroup exit
##

# Remove ourself from the workgroup
id = context.getId()
group = context.portal_groups.getGroupById(id)

me = context.portal_membership.getAuthenticatedMember().getId()
group.removeMember(me)

psm = context.translate("message_workgroup_exited", domain="rhaptos", default="Workgroup Exited")
return state.set(portal_status_message=psm)
