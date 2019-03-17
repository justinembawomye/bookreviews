import os

from application import create_app
from application.routes import *

config_name = 'production' # config_name = "development"
app = create_app(config_name)

if __name__ == '__main__':
    app.run()