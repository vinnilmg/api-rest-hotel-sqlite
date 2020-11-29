from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hoteis, Hotel #Importando um recurso
from resources.usuario import User, UserRegister, UserLogin, UserLogout, UserConfirm
from resources.site import Site, Sites
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db' #caminho e nome do banco -- pode usar outros tipos de bancos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #rastreio de modificações
app.config['JWT_SECRET_KEY'] = 'buibui10' #garantir criptografia
app.config['JWT_BLACKLIST_ENABLED'] = True

api = Api(app)
jwt = JWTManager(app)

@app.before_first_request #antes da primeiro requisição
def cria_banco():
	banco.create_all()

@jwt.token_in_blacklist_loader
def verifica_blacklist(token):
	return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado():
	return jsonify({'message': 'Você foi deslogado!'}), 401 #unauthorized #converter dict para json

api.add_resource(Hoteis, '/hoteis') #recurso importado
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<string:url>')
api.add_resource(UserConfirm, '/confirmacao/<int:user_id>')

if __name__ == '__main__': #se o nome for o principal, rode
    from sql_alchemy import banco
    banco.init_app(app) #só executa se chamar o app.py
    app.run(debug=True)
