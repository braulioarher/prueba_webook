import os
import pandas as pd

from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import EstadoModel, MunicipioModel, LocalidadModel
from resources.estado import blp as EstadoBlueprint
from resources.municipio import blp as MunicipioBlueprint
from resources.localidad import blp as LocalidadBlueprint

def create_app(db_url=None):
    
    app = Flask(__name__)


    # Variables de entorno de nuestra app
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Events API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    app.json.sort_keys = False


    migrate = Migrate(app, db)

    # Creacion de api
    api = Api(app)

    #Registro de blueprints en nuestra API
    api.register_blueprint(EstadoBlueprint)
    api.register_blueprint(MunicipioBlueprint)
    api.register_blueprint(LocalidadBlueprint)

    # Cargar informacion
    @app.cli.command()
    def loaddata():
        cp = pd.read_excel("CPdescarga.xls", sheet_name=None)
        estados = list(cp.keys())

        for estado in estados:
            id = cp[estado]["c_estado"][0]
            estado_add = estado.replace("_", " ")
            to_add = EstadoModel(id=int(id), name=estado_add)
            
            try:
                db.session.add(to_add)
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                print("Error al agregar estado")
        print("Estados agregados")
        
        for estado in estados:
            municipios = cp[estado]["D_mnpio"]
            est_id = cp[estado]["c_estado"].astype(str)
            mun_id = cp[estado]["c_mnpio"].astype(str)
            id = "_" + est_id + mun_id
            name_id = municipios + id
            set_mun_ids = set(name_id)
            for item in set_mun_ids:
                mun_id = item.split("_", 1)
                name = str(mun_id[0])
                id = int(mun_id[1])
                estado_id = int(cp[estado]["c_estado"][0])
                to_add = MunicipioModel(id=id, name=name, id_estado=estado_id)

                try:
                    db.session.add(to_add)
                    db.session.commit()
                except SQLAlchemyError:
                    db.session.rollback()
                    print(f"Error al agregar municipio de {name} en {estado}")
            print(f"Municipios de {estado} cargados")

        estados = list(cp.keys())
        
        for estado in estados:
            localidades = cp[estado][["d_codigo", "d_asenta"]].copy()
            localidades["id_muni"] = cp[estado]["c_estado"].astype(str) + cp[estado]["c_mnpio"].astype(str)
            
            for idex, row in localidades.iterrows():
                name = row["d_asenta"]
                codigo_p = int(row["d_codigo"])
                id_muni = int(row["id_muni"])
                to_add = LocalidadModel(name=name, cp=codigo_p, id_muni=id_muni)

                try:
                    db.session.add(to_add)
                    db.session.commit()
                except SQLAlchemyError:
                    db.session.rollback()
                    print(f"Error al agregar {name} municipio")

            print(f"Localidades de {estado} cargadas")
    
    @app.cli.command()
    def erasedata():
        db.drop_all()
        db.session.commit()
        db.create_all()


    return app