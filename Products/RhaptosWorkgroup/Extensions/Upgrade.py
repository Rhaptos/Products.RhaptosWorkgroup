from StringIO import StringIO

def resetPortalTypes(self):
    """Upgrade to the new LatestReference object"""
    out = StringIO()
    for wg in self.GroupWorkspaces.objectValues():
        wg._setPortalTypeName('Workgroup')

    out.write("Updated portal types\n")

    return out.getvalue()
