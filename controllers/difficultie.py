@auth.requires_login()
def new():
  session.guestID = request.args[0]
  guest = session.guestID
  fields = ['subject','story']
  form = SQLFORM(db.difficultie,fields=fields)
  form.vars.guest=guest
  form.vars.registrator=auth.user.id
  form.add_button('Cancel', URL('difficultie','overview',args=[guest]),_class="btn btn-primary")
  if form.process().accepted:
      response.flash = 'form accepted'
      guest = form.vars.guest
      redirect(URL(r=request,f='overview',args=[guest]))


  elif form.errors :
      response.flash = 'form has errors'
  else:
      response.flash = 'please fill out the form'

  return dict(form=form)

@auth.requires_login()
def overview():
  session.guestID = request.args[0]
  record = db(db.guest.id==session.guestID).select().first()

  difficulties =((db.difficultie.registrator == auth.user.id) & (db.difficultie.guest == session.guestID))
  fields = [db.difficultie.subject]
  form = SQLFORM.grid(difficulties, fields=fields ,searchable=False,deletable=False,editable=False,details=False,paginate=10,create=False,csv=False,links = [lambda row:A(T('Details'),_href=URL("difficultie","details",args=[row.id]))],user_signature=False)
  form[1].append(TAG.INPUT(_value=T('Add Difficultie'),_type="button",_class="btn btn-primary",_onclick="window.location='%s';"%URL(r=request,f='new',args = [session.guestID])))
  form[1].append(TAG.INPUT(_value=T('Back'),_type="button",_class="btn btn-primary",_onclick="window.location='%s';"%URL('guest','overview')))
  return dict(form=form,record=record)

@auth.requires_login()
def details():
      session.difficultieID = request.args[0]

      record = db(db.difficultie.id==session.difficultieID).select().first()

      form = SQLFORM(db.difficultie,record,showid = False,deletable=True,submit_button = T('Update'))
      form.add_button('Back', URL('difficultie','overview',args=[record.guest]), _class="btn btn-primary")

      if form.process().accepted:

          response.flash = T('form accepted')
          redirect(URL(r=request,f='overview',args=[record.guest]))

      elif form.errors:
           response.flash = T('form has errors')
      else:
           response.flash = T('Update Talk')

      return dict(form=form)
