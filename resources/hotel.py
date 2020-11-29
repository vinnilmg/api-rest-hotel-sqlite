from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel
from resources.filtros import normalize_path_params, consulta_com_cidade, consulta_sem_cidade
from flask_jwt_extended import jwt_required
import sqlite3

#path /hoteis?cidade=Rio de Janeiro&estrelas_min=4&diaria_max=400
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)

class Hoteis(Resource):
    def get(self):
        #conexao com o bd
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        if not parametros.get('cidade'):
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_sem_cidade, tupla)
        else:
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_com_cidade, tupla)

        hoteis = []
        for linha in resultado:
            hoteis.append({
                'hotel_id' :    linha[0],
                'nome' :        linha[1],
                'estrelas' :    linha[2],
                'diaria' :      linha[3],
                'cidade' :      linha[4],
                'site_id' :     linha[5]
            })

        return {'hoteis': hoteis}
        #return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]} #SELECT * FROM hotel

class Hotel(Resource):
    argumentos = reqparse.RequestParser() #chamado biblioteca para pegar elementos
    argumentos.add_argument('nome', type=str, required=True, help="O campo 'nome' não pode ser nulo.") #elementos por nome
    argumentos.add_argument('estrelas', type=float, required=True, help="O campo 'estrelas' não pode ser nulo.")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    argumentos.add_argument('site_id', type=int, required=True, help="O campo 'site_id' não pode ser nulo.")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message' : 'Hotel not found.'}, 404 #not found

    @jwt_required #obrigado estar logado (tem q ter token)
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400 #bad request

        dados = Hotel.argumentos.parse_args() #transforma em chave e valor dos argumentos
        hotel = HotelModel(hotel_id, **dados) #criando objeto do tipo hotel

        if not SiteModel.find_by_id(dados['site_id']):
            return {'message' : 'The Hotel must be associated to a valid site_id.'}, 400

        try:
            hotel.save_hotel()
        except:
            return {'message' : 'Erro interno ao tentar salvar o hotel.'}, 500 #internal server error
        return hotel.json()

    @jwt_required
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args() #transforma em chave e valor dos argumentos
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            try:
                hotel_encontrado.save_hotel()
            except:
                return {'message' : 'Erro interno ao tentar salvar o hotel.'}, 500
            return hotel_encontrado.json(), 200 #OK

        #se nao for encontrado, criar
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message' : 'Erro interno ao tentar salvar o hotel.'}, 500
        return hotel.json(), 201 #created (criado)

    @jwt_required
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message' : 'Erro interno ao tentar deletar o hotel.'}, 500
            return {'message' : 'Hotel deleted.'}
        return {'message' : 'Hotel not found.'}, 404
