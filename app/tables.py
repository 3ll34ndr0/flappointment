from app import db

class User(db.Model):
    __tablename__ = "cuentaUsuarios"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    wsaddress = db.Column(db.String, unique=True)
    tgaddress = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)

    def __init__(self, name, wsaddress=None, tgaddress=None, email=None, vCard=None): 
      self.name =name
      self.wsaddress = wsaddress
      self.tgaddress = tgaddress
      self.email = email
      self.vCard = vCard

   def __repr_(self):
	   return "<User %r>" % self.name

class Activity(db.Model):
	__tablename__ = "activities"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text)
	manager = db.Column(db.Integer, db.ForeignKey('cuentaUsuarios.id'))
	quota = db.Column(db.Integer)
	description  = db.Column(db.Text)
	vCalendar = db.Column(db.Text)

