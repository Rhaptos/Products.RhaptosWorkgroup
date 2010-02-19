## Script (Python) "workgroup_postop.cpy"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Workgroup post-operation destination controller
##

# Where to go once we leave or destroy a workgroup
from Products.CMFCore.utils import getToolByName

wgs = context.getWorkspaces()
if len(wgs) > 1:
    m_tool = getToolByName(context, 'portal_membership')
    home = m_tool.getHomeFolder()
    state.set(status='manage', context=home)   # enough WGs, go to "Manage Workgroups"
else:
    u_tool = getToolByName(context, 'portal_url')
    portal = u_tool.getPortalObject()
    state.set(status='home', context=portal)     # otherwise, go to "mydashboard Home"

return state