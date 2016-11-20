from app import db
from datetime import datetime, timedelta
class User(db.Model):
    __tablename__ = "users"

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

    def __repr__(self):
        return "<User %r>" % self.name

class Activity(db.Model):
    __tablename__ = "activities"
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.Text)
    id_manager  = db.Column(db.Integer, db.ForeignKey('users.id'))
    inscriptos  = db.relationship("Appointment", cascade="all, delete-orphan",backref='order')
    quota       = db.Column(db.Integer)
    description = db.Column(db.Text)
    vCalendar   = db.Column(db.Text)
    dayly       = db.Column(db.Text)
    weekly      = db.Column(db.Text)
    monthly     = db.Column(db.Text)
    wdays       = db.Column(db.Text) #Yes or not, that must be defined elsewhere (working days)

    manager     = db.relationship('User', foreign_keys=id_manager)

    def __init__(self, name, manager, quota=None, description=None,
                 vCalendar=None,dayly=None, weekly=None, monthly=None,
                 wdays=None):
        self.name        = name
        self.manager     = manager
        self.quota       = quota
        self.description = description
        self.vCalendar   = vCalendar
        self.dayly       = dayly
        self.weekly      = weekly
        self.monthly     = monthly
        self.wdays       = wdays

    def __repr__(self):
        return "<Activity %r>" % self.name


class Credit(db.Model):
    __tablename__ = "credits"
    id          = db.Column(db.Integer, primary_key=True)
    id_user     = db.Column(db.Integer, db.ForeignKey('users.id'))
    id_activity = db.Column(db.Integer, db.ForeignKey('activities.id'))
    credits     = db.Column(db.Integer)
    expireDate  = db.Column(db.DateTime)

    user        = db.relationship('User', foreign_keys=id_user)
    activity    = db.relationship('Activity', foreign_keys=id_activity)

    def __init__(self, id, id_user, id_activity, credits, expireDate=None):
        self.id_user     = id_user
        self.id_activity = id_activity
        self.credits     = credits
        if expireDate is None:
            expireDate = datetime.utcnow() + timedelta(days=30)
        self.expireDate = expireDate
    def __repr__(self):
        return "<Credits: {} which expire on {}>".format(self.credits,self.expireDate) 
    #TODO: Format date as wished



class Appointment(db.Model):
    __tablename__ = "appointments"
    id          = db.Column(db.Integer, primary_key=True)
    id_activity = db.Column(db.Integer, db.ForeignKey('activities.id'))
    initHour    = db.Column(db.DateTime)
    endHour     = db.Column(db.DateTime)

    activity    = db.relationship('Activity', foreign_keys=id_activity)

    def __init__(self, id, id_activity, initHour, endHour=None):
        self.id_activity = id_activity
        self.initHour    = initHour
        self.endHour     = endHour
    def __repr__(self):
        return "<Appointment: {} at {}>".format(self.id_activity, self.initHour)
    #TODO: Lear how to show the name of the id_activity..."

class Participant(db.Model):
    __tablename__ = "participants"
    id              = db.Column(db.Integer, primary_key=True)
    id_activity = db.Column(db.Integer, db.ForeignKey('activities.id'))
    id_user     = db.Column(db.Integer, db.ForeignKey('users.id'))

    activity    = db.relationship('Activity', foreign_keys=id_activity)
    user        = db.relationship('User', foreign_keys=id_user)


class MakeAppointment(db.Model):
    __tablename__ = 'makeappointment'
    id_activity = db.Column(Integer, ForeignKey('activities.id'), primary_key=True)
    id_user     = db.Column(Integer, ForeignKey('users.id'), primary_key=True)

    def __init__(self, user):
        self.user    = user

    user = relationship(User, lazy='joined')
