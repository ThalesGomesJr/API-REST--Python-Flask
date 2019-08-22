from flask_restful import Resource, reqparse
from models.hotel import HotelModel
#lista de hoteis
hoteis = [
    {
        'hotel_id': 'Alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Rio de Janeiro'
    },

    {
        'hotel_id': 'Oscar',
        'nome': 'Oscar Hotel',
        'estrelas': 4.4,
        'diaria': 380.90,
        'cidade': 'São Paulo'
    },

    {
        'hotel_id': 'Floresta',
        'nome': 'Floresta Hotel',
        'estrelas': 4.5,
        'diaria': 510.34,
        'cidade': 'Porto Alegre'
    }
]

class Hoteis(Resource):

    def get(self):
        return {'hoteis': hoteis}

class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        
        return {'Message': 'Hotel not found.'}, 404  # not found

    def post(self, hotel_id):
        
        dados = Hotel.argumentos.parse_args()
       
        hotel_objeto = HotelModel(hotel_id, **dados) 
        novo_hotel = hotel_objeto.json()

        hoteis.append(novo_hotel)
        return novo_hotel, 200


    def put(self, hotel_id):
        
        dados = Hotel.argumentos.parse_args()

        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()

        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200 #se foi atualizado um hotel já existente 
        else:
            hoteis.append(novo_hotel)
            return novo_hotel, 201 #se foi criado um novo hotel

        
    def delete(self, hotel_id):
        global hoteis #referenciar lista de hoteis.
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel deleted.'}

