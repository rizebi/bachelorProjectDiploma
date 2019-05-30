import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)

#############################################################################
############ CONFIGURATIONS (CAN BE SEPARATE CONFIG.PY FILE) ###############
###########################################################################

# Remember you need to set your environment variables at the command line
# when you deploy this to a real website.
# export SECRET_KEY=mysecret
# set SECRET_KEY=mysecret
app.config['SECRET_KEY'] = 'mysecret'

#################################
### DATABASE SETUPS ############
###############################

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:mypassword@mysql/car-planner'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


###########################
#### LOGIN CONFIGS #######
#########################

login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "useri.login"


##############################
#### BLUEPRINT CONFIGS #######
##############################


from carplanner.core.views import core
from carplanner.useri.views import useri
#from carplanner.masini.views import masini
#from carplanner.scadente.views import scadente
#from carplanner.error_pages.handlers import error_pages

# Register the apps
app.register_blueprint(core)
app.register_blueprint(useri)
#app.register_blueprint(masini)
#app.register_blueprint(scadente)
#app.register_blueprint(error_pages)
