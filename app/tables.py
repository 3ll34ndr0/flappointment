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
    quota       = db.Column(db.Integer)
    description = db.Column(db.Text)
    vCalendar   = db.Column(db.Text)
    dayly       = db.Column(db.Boolean)
    weekly      = db.Column(db.Boolean)
    monthly     = db.Column(db.Boolean)
    wdays       = db.Column(db.Boolean) # If True, which days must be defined elsewhere (working days)
    prePay      = db.Column(db.Boolean)
    """
    if enabled, user needs to buy some credit before booking an appointment. It
    is disabled by default.
    """

    manager     = db.relationship('User', foreign_keys=id_manager)

    def __init__(self, name, manager, quota=None, description=None,
                 vCalendar=None,dayly=False, weekly=None, monthly=None,
                 wdays=False, prePay=False):
        self.name        = name or self.name
        self.manager     = manager
        self.quota       = quota
        self.description = description
        self.vCalendar   = vCalendar
        self.dayly       = dayly
        self.weekly      = weekly
        self.monthly     = monthly
        self.wdays       = wdays
        self.prePay      = prePay

    def __repr__(self):
        return self.name


class Credit(db.Model):
    __tablename__ = "credits"
    id          = db.Column(db.Integer, primary_key=True)
    id_user     = db.Column(db.Integer, db.ForeignKey('users.id'))
    id_activity = db.Column(db.Integer, db.ForeignKey('activities.id'))
    credits     = db.Column(db.Integer)
    expireDate  = db.Column(db.DateTime)

    user        = db.relationship('User', foreign_keys=id_user)
    activity    = db.relationship('Activity', foreign_keys=id_activity)

    def __init__(self, user, activity, credits, expireDate=None):
        self.user     = user
        self.activity = activity
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
    enrolled    = db.relationship("MakeAppointment", cascade="all, delete-orphan", backref='appointment')

    def __init__(self, activity, initHour, endHour=None):
        self.activity = activity
        self.initHour    = initHour
        self.endHour     = endHour
    def __repr__(self):
        return "*{}*: {}".format(self.activity.name, self.initHour.strftime("%d %h %H:%M"))
    #TODO: Lear how to show the name of the id_activity..."




class Participant(db.Model):
    __tablename__ = "participants"
    id              = db.Column(db.Integer, primary_key=True)
    id_activity = db.Column(db.Integer, db.ForeignKey('activities.id'))
    id_user     = db.Column(db.Integer, db.ForeignKey('users.id'))

    activity    = db.relationship('Activity', foreign_keys=id_activity)
    user        = db.relationship('User', foreign_keys=id_user)


class MakeAppointment(db.Model):
    __tablename__  = 'makeappointment'
    id_appointment = db.Column(db.Integer, db.ForeignKey('appointments.id'), primary_key=True)
    id_user        = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    def __init__(self, user):
        self.user    = user

    user = db.relationship(User, lazy='joined')

