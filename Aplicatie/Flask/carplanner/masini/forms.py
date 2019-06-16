from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError
from carplanner import db
from carplanner.models import Marca

def RepresentsInt(s):
  try:
    int(s)
    return True
  except ValueError:
    return False

class AddVehicleForm(FlaskForm):
  '''
  marci = db.session.query(Marca.marcaMasina).distinct(Marca.marcaMasina).all()
  marciModele = Marca.query.filter_by().all()

  marciForm = []
  for marca in marci:
    marciForm.append((marca[0], marca[0]))

  marciModeleForm = []
  for marca in marciModele:
    marciModeleForm.append((marca.IDAuto, marca.modelMasina))'''

  choicesCombustibil = [("Benzina", "Benzina"), ("Motorina","Motorina"), ("Electric","Electric"), ("Hibrid","Hibrid"), ("Benzina + GPL","Benzina + GPL"), ("Hidrogen","Hidrogen")]

  marcaMasina = SelectField('marca', choices=[], render_kw={"placeholder": "Marca Vehicul"})
  modelMasina = SelectField('model', coerce=str, choices=[], render_kw={"placeholder": "Model Vehicul"})
  numarInmatriculare = StringField(validators=[DataRequired(message = "Introduceti numarul de inmatriculare")], render_kw={"placeholder": "Numar Inmatriculare*"})
  kilometraj = StringField(validators=[DataRequired(message = "Introduceti kilometrajul")], render_kw={"placeholder": "Kilometraj*"})
  anFabricatie = StringField(render_kw={"placeholder": "An Fabricatie"})
  combustibil = SelectField('combustibil', choices=choicesCombustibil, render_kw={"placeholder": "Combustibil"})

  capacitateCilindrica = StringField(render_kw={"placeholder": "Capacitate Cilindrica"})
  codMotor = StringField(render_kw={"placeholder": "Cod Motor"})
  VIN = StringField(render_kw={"placeholder": "VIN"})
  detaliiMasina = StringField(render_kw={"placeholder": "Detalii Vehicul"})

  submit = SubmitField('Adauga Vehicul')


  def validate_kilometraj(form, field):
    if RepresentsInt(field.data) is False:
      raise ValidationError('Kilometrajul trebuie sa fie un numar')

  def validate_capacitateCilindrica(form, field):
    if field.data != "" and RepresentsInt(field.data) is False:
      raise ValidationError('Capacitatea cilindrica trebuie sa fie un numar')

  def validate_anFabricatie(form, field):
    if field.data != "" and RepresentsInt(field.data) is False:
      raise ValidationError('Anul de fabricatie trebuie sa fie un numar')

class EditVehicleForm(FlaskForm):

  choicesCombustibil = [("Benzina", "Benzina"), ("Motorina","Motorina"), ("Electric","Electric"), ("Hibrid","Hibrid"), ("Benzina + GPL","Benzina + GPL"), ("Hidrogen","Hidrogen")]


  numarInmatriculare = StringField(validators=[DataRequired(message = "Introduceti numarul de inmatriculare")], render_kw={"placeholder": "Numar Inmatriculare*"})
  kilometraj = StringField(validators=[DataRequired(message = "Introduceti kilometrajul")], render_kw={"placeholder": "Kilometraj*"})
  anFabricatie = StringField(render_kw={"placeholder": "An Fabricatie"})
  combustibil = SelectField('combustibil', choices=choicesCombustibil, render_kw={"placeholder": "Combustibil"})
  capacitateCilindrica = StringField(render_kw={"placeholder": "Capacitate Cilindrica"})
  codMotor = StringField(render_kw={"placeholder": "Cod Motor"})
  VIN = StringField(render_kw={"placeholder": "VIN"})
  detaliiMasina = StringField(render_kw={"placeholder": "Detalii Vehicul"})

  submit = SubmitField('Actualizeaza Vehicul')


  def validate_kilometraj(form, field):
    if RepresentsInt(field.data) is False:
      raise ValidationError('Kilometrajul trebuie sa fie un numar')

  def validate_capacitateCilindrica(form, field):
    if field.data != "" and RepresentsInt(field.data) is False:
      raise ValidationError('Capacitatea cilindrica trebuie sa fie un numar')

  def validate_anFabricatie(form, field):
    if field.data != "" and RepresentsInt(field.data) is False:
      raise ValidationError('Anul de fabricatie trebuie sa fie un numar')
