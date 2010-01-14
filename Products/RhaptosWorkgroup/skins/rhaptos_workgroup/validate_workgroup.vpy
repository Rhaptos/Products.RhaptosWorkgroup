## Script (Python) "validate_registration"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##bind state=state
##parameters=title='', email=''
##title=Validates workgroup creation

def missing(field):
    errormsg = context.translate("message_this_field_required", domain="rhaptos", default="This field is required.")
    state.setError(field, errormsg)

if not title:
    missing('title')

if state.getErrors():
    psm = context.translate("message_please_correct_errors", domain="rhaptos", default="Please correct the indicated errors.")
    return state.set(status='failure', portal_status_message=psm)
else:
    psm = context.translate("message_workgroup_created", domain="rhaptos", default="Workgroup created.")
    return state.set(portal_status_message=psm)
