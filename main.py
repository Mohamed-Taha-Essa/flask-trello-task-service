from flask import Flask 
from flask_migrate import Migrate
from app.core.config import settings
 

def creat_app()->Flask :
    app = Flask(__name__)


    return app 



app = creat_app()


if __name__ == "__main__":
    app.run(
        host = settings.HOST,
        port = settings.PORT,
        debug = settings.DEBUG 
    )