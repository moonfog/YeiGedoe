@auth.requires_login()
def index():
	session.guestID = request.args[0]
	record = db(db.guest.id==session.guestID).select().first()
	talks = db(db.talk.guest == session.guestID).select()
	actions = db(db.things_to_do.guest == session.guestID).select()
	competences = db(db.guest_competence.guest == session.guestID).select()

	return dict(record=record,talks=talks,actions=actions,competences=competences) 


