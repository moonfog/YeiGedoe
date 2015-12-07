@auth.requires_login()
def new():
	session.guestID = request.args[0]
	guest = session.guestID
	fields = ['date_talk','type_of_talk','story']
	form = SQLFORM(db.talk,fields=fields)
	form.vars.guest = guest
	form.add_button('Cancel', URL('talk','overview',args=[guest]),_class="btn btn-primary")

	if form.process().accepted:
		response.flash = 'form accepted' #guest id meegeven uit form halen
		guest = form.vars.guest
		redirect(URL(r=request,f='overview',args=[guest]))

	elif form.errors :
		response.flash = 'form has errors'
	else:
		response.flash = 'please fill out the form'

	return dict(form=form)

@auth.requires_login()
def overview():
	if len(request.args)!= 0:
		session.guestID = request.args[0]
		
	record = db(db.guest.id==session.guestID).select().first()   
	talks = db.talk.guest == session.guestID
	fields = [db.talk.date_talk, db.talk.type_of_talk]

	form = SQLFORM.grid(talks,fields=fields,searchable=False,deletable=False,editable=False,details=False,paginate=10,create=False,csv=False,
		links = [lambda row:A(T('Details'),_href=URL("talk","details",args=[row.id]))], user_signature=False)
	form[1].append(TAG.INPUT(_value=T('Add Talk'),_type="button",_class="btn btn-primary",_onclick="window.location='%s';"%URL(r=request,f='new',args = session.guestID)))
	form[1].append(TAG.INPUT(_value=T('Back'),_type="button",_class="btn btn-primary",_onclick="window.location='%s';"%URL('guest', 'overview')))


	return dict(form=form,record=record)

@auth.requires_login()
def details():
	session.talkID = request.args[0]

	record = db(db.talk.id==session.talkID).select().first()
	guestId = record.guest


	form = SQLFORM(db.talk,record,deletable=True,showid = False,submit_button = T('Update'))
	form.add_button('Back', URL('talk','overview',args=[record.guest]), _class="btn btn-primary")

	if form.process().accepted:

		response.flash = T('form accepted')
		redirect(URL(r=request,f='overview',args=[record.guest]))

	elif form.errors:
		response.flash = T('form has errors')
	else:
		response.flash = T('Update Talk')

	return dict(form=form)
