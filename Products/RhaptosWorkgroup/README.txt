RhaptosWorkgroup

  This Zope Product is part of the Rhaptos system
  (http://software.cnx.rice.edu)

  RhaptosWorkgroup is a folderish content type that provides a shared
  workspace for groups of portal members.  It is designed to be used
  as the group work-area created by GRUF's portal_groups tool used in
  Plone 2.X.

  Workgroups have no member hierarchy: they are jointly owned by every
  member of the group.  Each member can add and remove other members
  as well as add, edit, and delete content.  When the last member of a
  workgroup leaves (or is removed), the workgroup is deleted.

Notes:

 - The primary view for RhaptosWorkgroup is the workspace_contents
   template defined in RhaptosSite for its Workspace type

 - The properties tab of RhaptosWorkgroup gets and sets properties on the
   underlying group object rather than on itself

 - Be sure that RhaptosWorkgroup's skin layer is above all the Plone layers.
   If it is not, the user addition can be expected to not work.
   