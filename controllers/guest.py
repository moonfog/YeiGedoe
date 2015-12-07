@auth.requires_login()
def new():


	fields = ['first_name','family_name','birth_year','sex','national_number','gsmnummer','email']
	form = SQLFORM(db.guest,fields=fields)
	form.add_button('Cancel', URL('guest','overview'),_class="btn btn-primary")

	if form.process().accepted:
		response.flash = 'form accepted'
		redirect(URL(r=request,f='overview'))
	elif form.errors :
		response.flash = 'form has errors'
	else:
		response.flash = 'please fill out the form'

	return dict(form=form)

@auth.requires_login()
def overview():
	fields = [db.guest.first_name,db.guest.family_name,db.guest.age]
	grid = SQLFORM.grid(db.guest,fields=fields,deletable=False,editable=False,details=False,paginate=10,create=False,csv=False,orderby=[~db.guest.id],
		links = [lambda row:A(T('Details'),_href=URL("guest","details",args=[row.id])),
				 lambda row:A(T('Competences'),_href=URL("guest_competence","overview",args=[row.id])),
				 lambda row:A(T('Talks'),_href=URL("talk","overview",args=[row.id])),
				 lambda row:A(T('Things to do'),_href=URL("things_to_do","overview",args=[row.id])),
				 lambda row:A(T('Difficulties'),_href=URL("difficultie","overview",args=[row.id])),
				 lambda row:A(T('Fiche'),_href=URL("fiche","index",args=[row.id])),
				 ])
	return dict(form=grid)

@auth.requires_login()
def details():

	session.guestID = request.args[0]

	record = db(db.guest.id==session.guestID).select().first()

	form = SQLFORM(db.guest,record,showid = False,submit_button = T('Update'))

	form.add_button('Back', URL('guest','overview'), _class="btn btn-primary")
	return dict(form=form,record=record)

	if form.process().accepted:
		response.flash = T('form accepted')
		redirect(URL(r=request,f='overview'))

	elif form.errors:
		response.flash = T('form has errors')
	else:
		response.flash = T('Update Guest')

	return dict(form=form)
