from flask import Flask, render_template, request, redirect, Blueprint, url_for
from utils import db
from models import Produto
from flask_migrate import Migrate
from routes.principal import home_route
from routes.produto import produto_route


app = Flask(__name__)

app.secret_key = 'minha_chave_secreta'

conexao = "sqlite:///meubanco.sqlite"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)


migrate = Migrate(app, db)

app.register_blueprint(home_route)
app.register_blueprint(produto_route, url_prefix='/produto')




if __name__ == '__main__':
    app.run()