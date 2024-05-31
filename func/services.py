from database.database import Session, engine, Base
from database.nutriApp import Nutricionista, Paciente, Turno, Dieta, FichaMedica
from models.modelos import NutricionistaModel, DietaModel, TurnoModel, PacienteModel, FichaMedicaModel, Credentials
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status



class servicesNutri():
    def __init__(self, db):
        self.db = db
    #agregar proceso de hasheo de password para login
    def add_nutricionista(self,nutrcionista: NutricionistaModel):
        new_nutricionista = Nutricionista(**nutrcionista.dict() )
        new_nutricionista.hash_password = login.get_hashed_password(new_nutricionista.hash_password)

        self.db.add(new_nutricionista)
        self.db.commit()

        return{"message": "nutricionista added"}

    def add_paciente(self,paciente: PacienteModel):
        new_paciente = Paciente(**paciente.dict())

        self.db.add(new_paciente)
        self.db.commit()

        return {"message": "paciente added"}

    def add_turno(self,turno: TurnoModel):
        new_turno = Turno(**turno.model_dump())

        self.db.add(new_turno)
        self.db.commit()

        return {"message": "turno added"}

    def add_dieta(self,dieta: DietaModel):
        new_dieta = Dieta(**dieta.model_dump())

        self.db.add(new_dieta)
        self.db.commit()

        return {"message": "dieta added"}

    def get_nutricionista(self,id : int):
        result = self.db.query(Nutricionista).filter(Nutricionista.id == id).first()
        if not result:
            JSONResponse(status_code=404,content={"message": "no encontrado"})
        return JSONResponse(status_code=200,content=jsonable_encoder(result))

    def get_pacientes(self,idNutricionista: int):
        result = self.db.query(Paciente).filter(Paciente.nutricionista_id == idNutricionista).all()
        return JSONResponse(status_code=200,content=jsonable_encoder(result))

    def update_Onepaciente(self,id : int, paciente: PacienteModel):
        paciente2 = self.db.query(Paciente).filter(Paciente.id == id).first()
        if not paciente2:
            raise HTTPException(status_code=404, content={"message": "paciente not exist"})

        paciente2.nombre = paciente.nombre
        paciente2.apellido = paciente.apellido
        paciente2.edad = paciente.edad
        paciente2.sexo = paciente.sexo
        paciente2.email = paciente.email
        paciente2.peso = paciente.peso
        paciente2.altura = paciente.altura
        paciente2.actividad_ficica = paciente.actividad_fisica
        paciente2.is_active = paciente.is_active
        paciente2.dieta_id = paciente.dieta_id
        paciente2.fecha_ult_actualizacion = paciente.fecha_utl_actualizacion
        paciente2.fecha_inicio = paciente.fecha_inicio

        self.db.commit()
        self.db.refresh(paciente2)
        return jsonable_encoder(paciente2)

    def sum_paciente(self,id : int):
        cant = self.db.query(Paciente).filter(Paciente.nutricionista_id == id, Paciente.is_active == True).count()
        return cant

    def sum_dietas(self,id : int):
        cant=self.db.query(Dieta).filter(Dieta.nutricionista_id == id).count()
        return cant

    def get_dietas(self,id : int):
        result = self.db.query(Dieta).filter(Dieta.nutricionista_id == id).first()
        if not result:
            {"message":"no hay dietas registradas"}
        return JSONResponse(status_code=200, content=jsonable_encoder(result))

    def get_turnos(self,id : int):
        result = self.db.query(Turno).filter(Turno.nutricionista_id == id).first()
        if not result:
            result = {"message":"no hay turnos registradas"}
        return result

    def update_nutricionista(self,id : int, nutricionista : NutricionistaModel):
        nutri =self.db.query(Nutricionista).filter(Nutricionista.id == id).first()
        if not nutri:
            raise HTTPExecption(status_code=404, content={"message":"no hay nutricionista registradas"})

        nutri.nombre = nutricionista.nombre
        nutri.apellido = nutricionista.apellido

        self.db.commit()
        return {"message": "nutricionista editado"}

    def update_turno(self,id : int, turno : TurnoModel):
        turno2 = self.db.query(Turno).filter(Turno.id == id).first()
        if not turno2:
            raise HTTPExecption(status_code=404, content={"message":"no hay turno"})

        turno2.paciente = turno.paciente
        turno2.fecha_hora = turno.fehca_hora
        turno2.estado = turno.estado

        self.db.commit()
        self.db.refresh(turno2)
        return turno2

    def update_dieta(self,id : int, dieta : DietaModel):
        dieta2 = self.db.query(Dieta).filter(Dieta.id == id).first()
        if  not dieta2:
            raise HTTPExecption(status_code=404,content={"message":"no hay dieta"})

        dieta2.detalles = dieta.detalles
        dieta2.nutricionista_id = dieta.nutricionista_id

        self.db.commit()
        self.db.refresh(dieta2)
        return jsonable_encoder(dieta2)

    def update_ficha(self,id : int, ficha : FichaMedicaModel):
        ficha2 = self.db.query(FichaMedica).filter(FichaMedica.id == id).first()
        if not ficha2:
            raise HTTPExecption(status_code=404,content={"message":"no ficha"})

        ficha2.paciente_id = ficha.paciente_id
        ficha2.detalles = ficha.detalles
        ficha2.dato_medico = ficha.dato_medico
        ficha2.fecha = ficha.fecha

        self.db.commit()
        self.db.refresh(ficha2)
        return jsonable_encoder(ficha2)

    def add_ficha(self,ficha :FichaMedicaModel):
        nuew_ficha = FichaMedica(**ficha.dict())

        self.db.add(nuew_ficha)
        self.db.commit()

        return jsonable_encoder(nuew_ficha)

    def get_ficha(self, id: int):
        new_ficha = self.db.query(FichaMedica).filter(FichaMedica.paciente_id == id).first()
        if not new_ficha:
            {"message": "no se encontro"}
        return jsonable_encoder(new_ficha)