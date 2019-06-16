from carplanner import app
import logging
from logging.handlers import RotatingFileHandler

if __name__ == '__main__':
    #formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    #handler = RotatingFileHandler('main.log', maxBytes=10000, backupCount=1)
    #handler.setLevel(logging.DEBUG)
    #handler.setFormatter(formatter)
    #app.logger.addHandler(handler)
    #app.logger.setLevel(logging.DEBUG)
    #app.logger.info("Starting app")
    app.run(debug=True, host='0.0.0.0')
