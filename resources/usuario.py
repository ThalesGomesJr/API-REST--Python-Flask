from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST


argumentos = reqparse.RequestParser()
argumentos.add_argument('login', type=str, required=True, help="Este campo 'login' é obrigatório.")
argumentos.add_argument('senha', type=str, required=True, help="Este campo 'senha' é obrigatório.")

class User(Resource):
    #/usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        
        return {'Message': 'User not found.'}, 404  # not found

    @jwt_required   
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'Message':'Erro ao excluir do banco de dados.'}
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404

class UserRegister(Resource):
    #/cadastro
    def post(self):
       
        dados = argumentos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' already exists".format(dados['login'])}

        user = UserModel(**dados)
        user.save_user()
        return {'message':'Sucesso'},201 #create


class UserLogin(Resource):


    @classmethod
    def post(cls):
        
        dados = argumentos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'access_token':token_de_acesso},200 #sucesso

        return {'message':'Usuario ou senha estão incorretos'},401 #não encontrado
    

class UserLogout(Resource):

    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti'] #JWT TOKEN IDENTIFIER
        BLACKLIST.add(jwt_id)
        return {'message': 'Logout feito com sucesso.'},200