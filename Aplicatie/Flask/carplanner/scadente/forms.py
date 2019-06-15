from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired
from carplanner import db
from carplanner.models import Marca, Scadent


class DefaultScadentForm(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later
    #title = StringField('Title', validators=[DataRequired()])
    #text = TextAreaField('Text', validators=[DataRequired()])
    #submit = SubmitField('BlogPost')
    default1 = BooleanField("Ulei + Filtre")
    default2 = BooleanField("Distributie")
    default3 = BooleanField("Elemente franare")
    default4 = BooleanField("Baterie")

    submit = SubmitField("Salveaza scadente")
