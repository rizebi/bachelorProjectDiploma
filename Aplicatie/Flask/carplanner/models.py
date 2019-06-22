from carplanner import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user
# and grab their id.

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

class User(db.Model, UserMixin):

  # Create a table in the db
  __tablename__ = 'useri'

  IDUser = db.Column(db.Integer, primary_key = True)
  imagineProfil = db.Column(db.String(50), nullable=False, default='default_profile.png')
  numeUser = db.Column(db.String(30), nullable=False)
  prenumeUser = db.Column(db.String(30), nullable=False)
  email = db.Column(db.String(30), nullable=False)
  parola = db.Column(db.String(128))
  numeCompanie = db.Column(db.String(30))

  masini = db.relationship('Masina', backref='proprietar', lazy='dynamic')

  def __init__(self, numeUser, prenumeUser, email, parola, numeCompanie):
    self.numeUser = numeUser
    self.prenumeUser = prenumeUser
    self.email = email
    self.numeCompanie = numeCompanie
    self.parola = generate_password_hash(parola)

  def check_password(self, parola):
    # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
    return check_password_hash(self.parola, parola)

  def __repr__(self):
    return f"Nume: {self.numeUser}, Prenume: {self.prenumeUser}"

  def get_id(self):
    return (self.IDUser)

class Masina(db.Model):

  # Create a table in the db
  __tablename__ = 'masini'

  IDMasina = db.Column(db.Integer, primary_key = True)
  IDUser = db.Column(db.Integer, db.ForeignKey('useri.IDUser'), nullable=False)
  IDAuto = db.Column(db.Integer, db.ForeignKey('marci.IDAuto'), nullable=False)
  detaliiMasina = db.Column(db.String(100))
  VIN = db.Column(db.String(20))
  combustibil = db.Column(db.String(20))
  capacitateCilindrica = db.Column(db.String(20))
  anFabricatie = db.Column(db.Integer)
  codMotor = db.Column(db.String(20))
  numarInmatriculare = db.Column(db.String(20), nullable=False)
  kilometraj = db.Column(db.Integer, nullable=False)
  crestereZilnica = db.Column(db.Integer)
  lastUpdate = db.Column(db.Date)

  scadente = db.relationship('Scadent', backref='masina', lazy='dynamic')

  def __init__(self, IDUser, IDAuto, detaliiMasina, VIN, combustibil, capacitateCilindrica, anFabricatie, codMotor, numarInmatriculare, kilometraj, crestereZilnica, lastUpdate):
    self.IDUser = IDUser
    self.IDAuto = IDAuto
    self.detaliiMasina = detaliiMasina
    self.VIN = VIN
    self.combustibil = combustibil
    self.capacitateCilindrica = capacitateCilindrica
    self.anFabricatie = anFabricatie
    self.codMotor = codMotor
    self.numarInmatriculare = numarInmatriculare
    self.kilometraj = kilometraj
    self.crestereZilnica = crestereZilnica
    self.lastUpdate = lastUpdate

  def __repr__(self):
    return f"IDMasina: {self.IDMasina}, IDAuto: {self.IDAuto}"


class Scadent(db.Model):

  # Create a table in the db
  __tablename__ = 'scadente'

  IDScadent = db.Column(db.Integer, primary_key = True)
  IDRevizie = db.Column(db.Integer, db.ForeignKey('reviziiDefault.IDRevizie'), nullable=False)
  numeScadent = db.Column(db.String(20), nullable=False)
  IDMasina = db.Column(db.Integer, db.ForeignKey('masini.IDMasina'), nullable=False)
  dataExp = db.Column(db.Date)
  areKM = db.Column(db.Boolean)
  kmExp = db.Column(db.Integer)
  viataZile = db.Column(db.Integer)
  viataKm = db.Column(db.Integer)

  def __init__(self, IDRevizie, numeScadent, IDMasina, dataExp, areKM, kmExp, viataZile, viataKm):
    self.numeScadent = numeScadent
    self.dataExp = dataExp
    self.areKM = areKM
    self.IDRevizie = IDRevizie
    self.IDMasina = IDMasina
    self.kmExp = kmExp
    self.viataZile = viataZile
    self.viataKm = viataKm

  def __repr__(self):
    return f"IDScadent: {self.IDScadent}, IDRevizie: {self.IDRevizie}"


class RevizieDefault(db.Model):

  # Create a table in the db
  __tablename__ = 'reviziiDefault'

  IDRevizie = db.Column(db.Integer, primary_key = True)
  IDAuto = db.Column(db.Integer, db.ForeignKey('marci.IDAuto'), nullable=False)
  numeSchimb = db.Column(db.String(20), nullable=False)
  viataZile = db.Column(db.Integer)
  viataKm = db.Column(db.Integer)

  def __init__(self, IDAuto, numeSchimb, viataZile, viataKm):
    self.IDAuto = IDAuto
    self.numeSchimb = numeSchimb
    self.viataZile = viataZile
    self.viataKm = viataKm

  def __repr__(self):
    return f"IDRevizie: {self.IDRevizie}, IDAuto: {self.IDAuto}"

class Marca(db.Model):

  # Create a table in the db
  __tablename__ = 'marci'

  IDAuto = db.Column(db.Integer, primary_key = True)
  marcaMasina = db.Column(db.String(20))
  modelMasina = db.Column(db.String(20))

  def __init__(self, marcaMasina, modelMasina):
    self.marcaMasina = marcaMasina
    self.modelMasina = modelMasina

  def __repr__(self):
    return f"IDAuto: {self.IDAuto}, marcaMasina: {self.marcaMasina}"
