from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from blueprints import register_blueprints
from config import config
from schemas import connect_db


app = Flask(__name__)

app.config.from_object(config)
toolbar = DebugToolbarExtension(app)
app = register_blueprints(app)

connect_db(app)


if __name__ == '__main__':
    app.run(debug=True)


