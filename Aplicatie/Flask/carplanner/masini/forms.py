from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class AddVehicleForm(FlaskForm):
  detaliiMasina = TextAreaField(render_kw={"placeholder": "Detalii Masina"})
  VIN = StringField(render_kw={"placeholder": "VIN"})
  submit = SubmitField('Adauga Vehicul')
