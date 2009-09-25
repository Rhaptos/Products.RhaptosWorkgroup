## Script (Python) "validate_registration"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=validates the membership of a workgroup

# CNX note: now for FormController

REQUEST=context.REQUEST
errors = {}

add = REQUEST.get('ids',[])
delete = REQUEST.get('delete', [])
groupname = REQUEST.get('groupname', None)

group = context.portal_groups.getGroupById(groupname)

if not add and not delete:
    psm = context.translate("message_no_one_selected", domain="rhaptos", default="No one selected.")
    return state.set(status='failure', portal_status_message=psm)
else:
    return state
