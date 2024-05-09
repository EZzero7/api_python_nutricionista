from fastapi import FastAPI
from database.database import Session, engine, Base, database_url
from database.nutriApp import Nutricionista, Paciente, Turno, Dieta, FichaMedica
from func.services import *
from security.jwt_manager_auth import *
from security.jwt_manager_auth import login

app = FastAPI()

Base.metadata.create_all(bind=engine)

oauth2_token = oauth2


def validate_token(token : str = Depends(oauth2_token)):
        respuesta = jwt.decode(token,SECRET,algorithms=[ALGORITHM])
        return respuesta

@app.get('/login')
def login_acces(nutricionista: NutricionistaModel):
    db = Session()
    contraseña = login.get_hashed_password(nutricionista.hash_password)
    token= login(db).verify_password(nutricionista.hash_password,nutricionista.email)
    return JSONResponse(status_code=200, content=token)

@app.get('/home/{id}', response_model=dict, status_code=200)
def home(id:int, token = Depends(validate_token)):
    db = Session()
    pacientes = servicesNutri(db).sum_paciente(id)
    dietas = servicesNutri(db).sum_dietas(id)
    turnos = servicesNutri(db).get_turnos(id)
    return {"suma pacientes": pacientes,
            "suma dietas": dietas,
            "turnos": jsonable_encoder(turnos)}

@app.post('/addNutricionista', response_model=dict , status_code=201)
def ag_nutri(nutricionista : NutricionistaModel):
    db = Session()
    respuestas = servicesNutri(db).add_nutricionista(nutricionista)
    return respuestas

@app.put('/editNutricionista/{id}', response_model=dict, status_code=200)
def edit_nutricionista(nutricionista : NutricionistaModel, id : int, token = Depends(validate_token)):
    db = Session()
    respuestas = servicesNutri(db).update_nutricionista(id, nutricionista)
    db.commit()
    return respuestas

@app.get('/nutricionista/{id}', response_model=dict, status_code=200)
def one_nutricionista(id, token = Depends(validate_token)):
    db = Session()
    respuesta = servicesNutri(db).get_nutricionista(id)
    return respuesta

@app.post('/Nutricionista/addPaciente', response_model=dict, status_code=200)
def ag_paciente(paciente : PacienteModel, token = Depends(validate_token)):
    db = Session()
    respuestas = servicesNutri(db).add_paciente(paciente)
    return respuestas

@app.get('/nutricionista/{idNutri}/pacientes',response_model=dict, status_code=200)
def all_pacientes(idNutri : int, token = Depends(validate_token)):
    db = Session()
    respuestas = servicesNutri(db).get_pacientes(idNutri)
    return respuestas

@app.put('/nutricionista/paciente/edit/{id}', response_model=dict,status_code=201)
def edit_paciente(id : int, paciente : PacienteModel, token = Depends(validate_token)):
    db=Session()
    respuestas = servicesNutri(db).update_Onepaciente(id,paciente)
    return respuestas

@app.post('/Nutricionista/addTurno', response_model=dict, status_code=201)
def ag_turno(turno : TurnoModel, token = Depends(validate_token)):
    db = Session()
    respuestas = servicesNutri(db).add_turno(turno)
    return respuestas

@app.post('/Nutricionista/Paciente/addDieta', response_model=dict, status_code=201)
def ag_dieta(dieta: DietaModel, token = Depends(validate_token)):
    db = Session()
    respuestas = servicesNutri(db).add_dieta(dieta)
    return respuestas

@app.get('/nutricionista/{id}/dietas', response_model=dict,status_code=200)
def all_dietas(id : int, token = Depends(validate_token)):
    db = Session()
    respuestas = servicesNutri(db).get_dietas(id)
    return respuestas

@app.put('/nutricioniista/editDieta/{id}', response_model=dict, status_code=201)
def edit_dieta(id: int, dieta : DietaModel, token = Depends(validate_token)):
    db = Session()
    respuestas = servicesNutri(db).update_dieta(id,dieta)
    return respuestas

@app.post('/nutricionista/paciente/addFicha',response_model=dict,status_code=201)
def ag_ficha(ficha : FichaMedicaModel, token = Depends(validate_token)):
    db = Session()
    respuestas = servicesNutri(db).add_ficha(ficha)
    return respuestas

@app.put('/nutricionista/paciente/editFicha/{id}',response_model=dict, status_code=201)
def edit_ficha(id: int, ficha : FichaMedicaModel, token = Depends(validate_token)):
    db = Session()
    respuestas = servicesNutri(db).update_ficha(id,ficha)
    return respuestas

@app.get('/nutricionista/paciente/{id}/ficha',response_model=dict, status_code=201)
def ag_ficha(id:int, token = Depends(validate_token)):
    db = Session()
    respuestas = servicesNutri(db).get_ficha(id)
    return respuestas