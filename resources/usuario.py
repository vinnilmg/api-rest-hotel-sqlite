from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST
import traceback
from flask import make_response, render_template

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="O campo 'login' não pode ser null.")
atributos.add_argument('senha', type=str, required=True, help="O campo 'senha' não pode ser null.")
atributos.add_argument('email', type=str)
atributos.add_argument('ativado', type=bool)

class User(Resource):
    # /usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message' : 'User not found.'}, 404 #not found

    @jwt_required
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message' : 'Erro interno ao tentar deletar o usuario.'}, 500
            return {'message' : 'User deleted.'}
        return {'message' : 'User not found.'}, 404

class UserRegister(Resource):
    # /cadastro
    def post(self):
        dados = atributos.parse_args()
        if not dados.get('email') or dados.get('email') is None: #verifica se ela nulo ou se foi informado
            return {'message' : "The field 'email' cannot be left blank."}, 400

        if UserModel.find_by_email(dados['email']): #verificar se o email existe
            return {'message' : f"The email '{dados['email']}' already exists. "}, 400

        if UserModel.find_by_login(dados['login']): #verificar se já existe o login na tabela
            return{"message": "The login '{}' already exists.".format(dados['login'])}

        user = UserModel(**dados) #ou dados['login'], dados['senha']
        user.ativado = False #garantir que seja falso
        
        try:
            user.save_user()
            user.send_confirmation_email()
        except:
            user.delete_user()
            traceback.print_exc()
            return {'message' : 'An internal server error has ocurred.'}, 500
        return {'message': 'User created successfully!'}, 201 #created

class UserLogin(Resource):
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']): #comparar strings
            if user.ativado:
                token_de_acesso = create_access_token(identity=user.user_id) #criar token de acesso
                return {'access_token' : token_de_acesso}, 200
            return {'message' : 'User not confirmed.'}, 400
        return {'message': 'The username or password is incorrect.'}, 401 # Unauthorized


class UserLogout(Resource):

    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti'] #JWT TOKEN IDENTIFIER
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out succesfully!'}, 200

class UserConfirm(Resource): #URI para ativar user
    #raiz_do_site/confirmacao/{user_id}

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_user(user_id)

        if not user:
            return {'message': f"User id {user_id} not found."}, 404
        user.ativado = True
        user.save_user()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('user_confirm.html', email=user.email, usuario=user.login), 200, headers)
        # return {'message' : f'User id {user_id} confirmed successfully.'}, 200
