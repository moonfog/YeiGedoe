# -*- coding: utf-8 -*-
import datetime

session._language='nl'
T.force(session._language)
#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)


## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True


##redirect after login

def redirect_after_login(form):
  redirect(URL(r=request,c='guest',f='overview'))

auth.settings.login_onaccept.append(redirect_after_login)

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

#########################################################################
#defining some sets i need
years = []
guest_errors = None
guest_errors = []

talk_errors = None
talk_errors = []

competence_errors = None
competence_errors = []
#########################################################################

#####some methods i use#################################################
def makeYears():
	i = 0
	year = datetime.date.today().year
	while i < 100:
		i = i + 1
		years.append(year)
		year = year - 1
######################################################################
## validator voor rijksregisternummer ################################
def checkNationalNumber(national_number):
   isRijksRegisterNummer = False
   rr = national_number

   if(len(rr) == 11) :
      if(int(rr[0][0]) == 0):
       rr = ''.join(('2',rr))
      else :
       rr = rr

      checkDigit = int(rr[-2:])
      rr = rr[:-2]
      rr_rest97 = int(float(rr) / 97.0)

      rr_maal97 = rr_rest97 * 97

      testcijfer = int(rr) - rr_maal97

      if ((97 - testcijfer) == checkDigit):
            isRijksRegisterNummer = True
            return isRijksRegisterNummer
      else :
            return isRijksRegisterNummer

   else:
      return isRijksRegisterNummer

class IS_NATIONALNUMBER():
    def __init__(self, error_message="Foutief nummer"):
        self.error_message = error_message

    def __call__(self, nummer):
        error = None
        value = checkNationalNumber(nummer)
        if not value == True :
            error = self.error_message
        return (nummer, error)
#####################################################################



makeYears()

db.define_table('guest',
	Field('first_name',notnull=True,label=T('Firstname')),
	Field('family_name',notnull=True,label=T('Familyname')),
	Field('birth_year','integer',notnull=True,label=T('Birth year')),
	Field('sex',notnull=True,label=T('Sex')),
	Field('national_number',notnull=True,label=T('National number')),
    Field('gsmnummer',label=T('GSM')),
    Field('email',notnull=False,label=T('Email')),
	Field('registration_date','date',default=request.now,label=T('Registration date')),
	Field('registrator','reference auth_user',default=auth.user_id,label=T('Registered by')),
	Field('age',compute=lambda r: (datetime.datetime.now().year) - int(r['birth_year']),label=T('Age')),
	format = '%(first_name)s %(family_name)s')
db.guest.birth_year.requires=IS_IN_SET(years,zero=T('Choose One'),error_message = T('Choose a year from the list'))
db.guest.sex.requires=IS_IN_SET(["man","vrouw"],zero=T('Choose One'))
db.guest.national_number.requires=IS_NATIONALNUMBER()
#als je require gebruikt kan niet leeg zijn
#db.guest.email.requires=IS_EMAIL(error_message='invalid email')

db.define_table('difficultie',
    Field('registrator','reference auth_user',default=auth.user_id,label=T('Registred by')),
    Field('guest',db.guest,notnull=True,label=T('Guest')),
    Field('subject',notnull=True,label=T('Difficultie')), #vaste waarden van maken
    Field('story','text',label=T('Story')),
    format='%(difficultie)s')
db.difficultie.subject.requires=IS_IN_SET(["administratie","financieel","middelengebruik","familiaal","huisvesting","juridisch","ander"])

db.define_table('talk',
    Field('registrator','reference auth_user',default=auth.user_id,label=T('Registered by')),
    Field('guest',db.guest,notnull=True,label=T('Guest')),
    Field('date_talk','date',default=request.now,label=T('Date Talk')),
    Field('type_of_talk',notnull=True,label=T('Type of talk')),
    Field('story','text',label=T('Story')),
    format ='%(type_of_talk)s'
)

db.talk.type_of_talk.requires=IS_IN_SET(["intake","trajectbegeleiding","evaluatie"])

db.define_table('competence',
   Field('name',label=T('Name')),
   format= '%(name)s')

db.define_table('guest_competence',
    Field('guest',db.guest,notnull=True,label=T('Guest')),
    Field('state_of_competence',label=T('State')),
    Field('competence',db.competence,label=T('Competence')),
    Field('type_of_competence',label=T('Type of competence')),
    Field('level_of_competence',label=T('Level of competence')),
    format = '%(guestcompetence)s')

db.guest_competence.state_of_competence.requires=IS_IN_SET(["kan","wil"])
db.guest_competence.type_of_competence.requires=IS_IN_SET(["generiek","technisch"])

db.define_table('things_to_do',
    Field('registrator','reference auth_user',default=auth.user_id,label=T('Registered by')),
    Field('guest',db.guest,notnull=True,label=T('Guest')),
    Field ('guidance',label=T('Guidance')),
    Field('startdate','date',default=request.now,notnull=True,label=T('startdate')),
    Field('date_to_aim', 'date', label=('Aimdate')),
    Field('competence',db.competence, label=('Competence')),
    Field('story','text',label=T('Story')),
    Field('success','boolean',label=T('Success')))
