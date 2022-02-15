from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from carplanner import db
from carplanner.models import Marca, Scadent

def RepresentsInt(s):
  try:
    int(s)
    return True
  except ValueError:
    return False

class DefaultScadentForm(FlaskForm):
  default1 = BooleanField("Ulei + Filtre")
  default2 = BooleanField("Distributie")
  default3 = BooleanField("Elemente franare")
  default4 = BooleanField("Baterie")

  submit = SubmitField("Salveaza scadente")


class AddScadentForm(FlaskForm):


  numeScadent = StringField(validators=[DataRequired(message = "Introduceti Numele Scadentului")], render_kw={"placeholder": "Nume Scadent*"})
  viataZile = StringField(validators=[DataRequired(message = "Introduceti Viata in Zile a Scadentului")], render_kw={"placeholder": "Viata Zile*"})
  viataKm = StringField(render_kw={"placeholder": "Viata Km (0 daca nu este cazul)"})


  submit = SubmitField('Adauga Scadent!')

  def validate_viataZile(form, field):
    if RepresentsInt(field.data) is False:
      raise ValidationError('Viata zile trebuie sa fie un numar')
    if (len(str(field.data))) > 4:
      raise ValidationError('Viata zile introdusa este prea mare')

  def validate_viataKm(form, field):
    if field.data != "" and RepresentsInt(field.data) is False:
      raise ValidationError('Viata kilometri trebuie sa fie un numar')
    if (len(str(field.data))) > 7:
      raise ValidationError('Viata kilometri introdusa este prea mare')

  def validate_numeScadent(form, field):
    if (len(str(field.data))) > 19:
      raise ValidationError('Nume scadent introdus este prea lung')

class EditScadentForm(FlaskForm):


  numeScadent = StringField(validators=[DataRequired(message = "Introduceti Numele Scadentului")], render_kw={"placeholder": "Nume Scadent*"})
  viataZile = StringField(validators=[DataRequired(message = "Introduceti Viata in Zile a Scadentului")], render_kw={"placeholder": "Viata Zile*"})
  viataKm = StringField(render_kw={"placeholder": "Viata Km (0 daca nu este cazul)"})


  submit = SubmitField('Actualizeaza Scadent!')


  def validate_viataZile(form, field):
    if RepresentsInt(field.data) is False:
      raise ValidationError('Viata zile trebuie sa fie un numar')
    if (len(str(field.data))) > 4:
      raise ValidationError('Viata zile introdusa este prea mare')

  def validate_viataKm(form, field):
    if field.data != "" and RepresentsInt(field.data) is False:
      raise ValidationError('Viata kilometri trebuie sa fie un numar')
    if (len(str(field.data))) > 7:
      raise ValidationError('Viata kilometri introdusa este prea mare')

  def validate_numeScadent(form, field):
    if (len(str(field.data))) > 19:
      raise ValidationError('Nume scadent introdus este prea lung')
