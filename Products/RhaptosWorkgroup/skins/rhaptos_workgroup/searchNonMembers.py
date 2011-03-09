## Script (Python) "searchNonMembers"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=search, exclude
##title= Search for members not in the workgroup

# We assume these are all catalog brains so getUserName is an
# attribute not a method
exclude_names = [u.getId() for u in exclude]
members = context.portal_membership.searchForMembers(name=search)
# Need a status property for members!
# return [m for m in members if m.status != "Pending" and m.getId not in exclude_names]
return [m for m in members if m.getId not in exclude_names]

