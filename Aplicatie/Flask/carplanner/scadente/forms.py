from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from carplanner import db
from carplanner.models import Marca, Scadent


'''class DefaultScadentForm(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later
    #title = StringField('Title', validators=[DataRequired()])
    #text = TextAreaField('Text', validators=[DataRequired()])
    #submit = SubmitField('BlogPost')
    pass'''


'''class DefaultScadentForm(FlaskForm):

    def __init__(self):
        FlaskForm.__init__(self)

    def init2(self, fruit):
      self.name = StringField('Do you like' + fruit)'''

def update_form(request):
    #table = query()

    class MyForm(Form):
        pass

    #for row in table:
    setattr(MyForm, "ceva", SomeField())

    form = MyForm(request.form)
