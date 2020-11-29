from sql_alchemy import banco
from flask import request, url_for
from requests import post


#constantes
MAILGUN_DOMAIN = 'sandboxd58facbadd8946beb55098295ecef31a.mailgun.org'
MAIL_GUN_API_KEY = '9566b74fd20b415ad2d62d09e57053e3-d5e69b0b-4c42c18e'
FROM_TITLE = 'NO-REPLY'
FROM_EMAIL = 'no-reply@restapi.com'

class UserModel(banco.Model): #tabela no banco
    __tablename__ = 'usuarios' #nome da tabela

    #mapeamento para o SQLAlchemy
    user_id =  banco.Column(banco.Integer, primary_key=True) #tipo e primary key
    login =  banco.Column(banco.String(40), nullable=False, unique=True)
    senha =  banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(80), nullable=False, unique=True) 
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, senha, email, ativado): #Construtor
        self.login = login
        self.senha = senha 
        self.email = email
        self.ativado = ativado

    def send_confirmation_email(self):
        link = request.url_root[:-1] + url_for('userconfirm', user_id=self.user_id)

        return post(f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages', 
                auth = ('api', MAIL_GUN_API_KEY),
                data = {'from' : f'{FROM_TITLE} <{FROM_EMAIL}>',
                        'to' : self.email,
                        'subject' : 'Confimação de cadastro',
                        'text' : f'Confirme seu cadastro clicando no link a seguir: {link}',
                        'html' : f"""<html><p>
                            Confirme seu cadastro clicando no link a seguir: <a href="{link}">CONFIRMAR</a></p></html>"""
                        }
                    )

    def json(self):
        return {
        'user_id' : self.user_id,
        'login' : self.login,
        'email' : self.email,
        'ativado' : self.ativado
        }

    #CRUD
    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id = user_id).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login = login).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email = email).first()
        if user:
            return user
        return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()


    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()

