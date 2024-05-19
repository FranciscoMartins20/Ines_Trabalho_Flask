from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__, template_folder='./app/templates', static_folder='./app/static')
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'  # Defina uma chave secreta para proteger suas sessões
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from routes import *

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('site.db'):
            db.create_all()
    app.run(debug=True)
