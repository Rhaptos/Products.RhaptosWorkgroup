## Script (Python) "workgroup_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##bind state=state
##parameters=title="",email="",description=""
##title=
##

REQUEST=context.REQUEST
groupstool = context.portal_groups
portal = context.portal_url

id = REQUEST.get('groupname', None)
newGroup = ''

# If there wasn't a group specified, we must be creating one
if id is None:
    f = portal.workgroups
    id = newGroup = 'wg' + str(f.nextID)
    f.manage_changeProperties(nextID = f.nextID + 1)
    f.invokeFactory(type_name='Workgroup',id=id)
    groupstool.addGroup(newGroup, "", (), ())

group = groupstool.getGroupById(id)
group.setGroupProperties(REQUEST.form)
msg = context.translate("message_workgroup_properties_changed", domain="rhaptos", default="Properties changed.")

# If this is a new group, we'll add the current user as a member
if newGroup:
    member = context.portal_membership.getAuthenticatedMember()
    group.addMember(member.getId())
    msg = context.translate("message_workgroup_created", domain="rhaptos", default="Workgroup created.")
    
new_context = portal.workgroups.get(id)

return state.set(status='success', portal_status_message=msg, context=new_context)


