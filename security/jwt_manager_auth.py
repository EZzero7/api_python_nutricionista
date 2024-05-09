from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from database.database import Session, engine, Base
from database.nutriApp import Nutricionista, Paciente, Turno, Dieta, FichaMedica
from models.modelos import NutricionistaModel, DietaModel, TurnoModel, PacienteModel, FichaMedicaModel, Credentials
from fastapi.responses import JSONResponse


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 60
SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b"


oauth2 = OAuth2PasswordBearer(tokenUrl="login")

password_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

class login():
    def __init__(self,db):
        self.db = db

    def get_hashed_password(password: str):
        return password_context.hash(password)


    def verify_password(self, hashed_pass : str, user : str):
        respuesta = self.db.query(Nutricionista).filter(Nutricionista.email == user).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario o contraseña incorrectos")    
        if not  password_context.verify(hashed_pass,respuesta.hash_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Usuario o contraseña incorrectos")
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)

        acces_token_payload = {
            "sub": user,
            "exp": expire
        }
        acces_token = jwt.encode(acces_token_payload,SECRET,algorithm=ALGORITHM)
        
        return {"acces_token":acces_token , "token_type": "Bearer"}

    