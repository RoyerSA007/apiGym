from models.user import User as UserModel
from schemas.user import User, LoginRequest, LoginResponse
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService():
    def __init__(self, db) -> None:
            self.db = db

    def get_Usuarios(self):
        result = self.db.query(UserModel).all()
        return result
    
    def get_user(self, id: int):
        result =  self.db.query(UserModel).filter(UserModel.id == id).first()
        return result
    
    def create_usuario(self, usuario : User):
        new_Usuario =  UserModel(**usuario.model_dump())
        self.db.add(new_Usuario)
        self.db.commit()
        return 
    
    def delete_user(self, id: int):
        result = self.db.query(UserModel).filter(UserModel.id == id).first()
        if not result:
            return {"message":"No existe el usuario"}
        self.db.delete(result)              
        self.db.commit()
        return {"message":"Usuario eliminado"}

    # def authenticate_user(self,email:str, password:str):
    #     result = self.db.query(UserModel).filter(UserModel.email == email).first()
    #     if not result:
    #         return {"message":"No existe el usuario"}, False
        
    #     if pwd_context.verify(password, result.password):
    #         return {"message": "Usuario autenticado"}, True
    #     else:
    #         return {"message": "Contraseña incorrecta"}, False

    # def authenticate_user(self,email:str, password:str):
    #     result = self.db.query(UserModel).filter(UserModel.email == email).first()
    #     if not result:
    #         return {"message":"No existe el usuario"}, False
        
    #     if result.password == password:
    #         return {"message": "Usuario autenticado"}, True
    #     else:
    #         return {"message": "Contraseña incorrecta"}, False
        
    def authenticate_user(self,login_request: LoginRequest) -> LoginResponse:
    # Buscar al usuario por email en la base de datos
        user = self.db.query(UserModel).filter(UserModel.email == login_request.email).first()
        
        if not user or user.password != login_request.password:
            return LoginResponse(
                userId=0,
                isLogged=False,
                message="Usuario o contraseña incorrectos"
            )
    
        
        # Retornar la respuesta de login
        return LoginResponse(
            userId=user.id,
            isLogged=True,
            message="Bienvenido"
        )