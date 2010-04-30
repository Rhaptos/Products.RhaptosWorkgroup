## Script (Python) "getWorkspaces"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=returnonly=None
##title= Returns a list of the current member's workspaces
# Return list of dicts with keys 'id', 'title', 'members', 'contents', 'email', 'description', 'link',
#  'folder', but see below. Sorted by title.
# Pass 'returnonly' a dict with any or all keys specified to return to get only those data points back
#  (and not do the calculations). Values don't matter. Set returnonly=false value to get all (the default).
#  The 'title' will always be returned, as it is required for sorting.

## Rhaptos note: no difference in conversion. no plone counterpart.

g_tool = context.portal_groups
m_tool = context.portal_membership

member = m_tool.getAuthenticatedMember()
glist = g_tool.getGroupsForPrincipal(member);
groups = [g_tool.getGroupById(g) for g in glist]
groups = [g for g in groups if g is not None]  # filter bad groups

returnonly = returnonly or {'id': None, 'members':None, 'contents':None,
                            'email':None, 'description':None, 'link':None, 'folder':None}
returnonly['title'] = None  # title is required for sorting

workspaces = []
for g in groups:
    gfolder = g_tool.getGroupareaFolder(g.getGroupName())
    groupname = g.getGroupName()
    gdict = {}
    if returnonly.has_key('id'):          gdict['id'] = groupname
    if returnonly.has_key('title'):       gdict['title'] = g.getGroupTitleOrName()
    if returnonly.has_key('link'):        gdict['link'] = gfolder and gfolder.absolute_url(1) or None
    if returnonly.has_key('contents'):    gdict['contents'] = gfolder and len(gfolder.contentIds()) or 0
    if returnonly.has_key('folder'):      gdict['folder'] = gfolder
    if returnonly.has_key('email'):       gdict['email'] = g.getProperty('email')
    if returnonly.has_key('description'): gdict['description'] = g.getProperty('description')
    if returnonly.has_key('members'):     gdict['members'] = [{'fullname':m.getProperty('fullname'),
                                                               'id':m.getMemberId()} for m in g.getGroupMembers()]
    workspaces.append(gdict)

workspaces.sort(cmp=lambda x,y:cmp(x['title'].lower(), y['title'].lower()))

return workspaces
