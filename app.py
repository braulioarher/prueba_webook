import os
import pandas as pd

from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import EstadoModel, MunicipioModel, LocalidadModel


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

    # Cargar informacion
    @app.cli.command()
    def loaddata():
        cp = pd.read_excel("CPdescarga.xls", sheet_name=None)
        estados = list(cp.keys())

        for estado in estados:
            id = cp[estado]["c_estado"][0]
            estado = estado.replace("_", " ")
            to_add = EstadoModel(id=int(id), name=estado)
            
            try:
                db.session.add(to_add)
                db.session.commit()
                print(f"Estado {estado} agregado")
            except SQLAlchemyError:
                print("Error al agregar estado")
        
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
                    print(f"Municipio {name} agregado")
                except SQLAlchemyError:
                    db.session.rollback()
                    print(f"Error al agregar {name} municipio")

                

    
    @app.cli.command()
    def erasedata():
        db.drop_all()
        db.session.commit()
        db.create_all()


    return app