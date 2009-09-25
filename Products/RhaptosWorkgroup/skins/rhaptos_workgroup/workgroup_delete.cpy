## Script (Python) "workgroup_delete.cpy"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Delete the workgroup
##
from Products.CMFCore.utils import getToolByName

id = context.getId()
g_tool = getToolByName(context, 'portal_groups')
g_tool.removeGroups([id])

psm = context.translate("message_workgroup_deleted", domain="rhaptos", default="Workgroup Deleted")
return state.set(portal_status_message=psm)

