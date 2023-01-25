from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app import db
from models import LocalidadModel
from schemas import LocalidadSchema, PlainLocalidadSchema

blp = Blueprint("localidades", __name__, description="Opereaciones en localidades")

@blp.route("/localidad/<string:localidad_name>")
class Localidad(MethodView):
    @blp.response(200, PlainLocalidadSchema(many=True))
    def get(self, localidad_name):
        localidad = db.session.query(LocalidadModel).filter(LocalidadModel.name == localidad_name).all()
        return localidad

@blp.route("/localidad/cp/<string:codigo_postal>")
class Localidadescp(MethodView):
    @blp.response(200, PlainLocalidadSchema(many=True))
    def get(self, codigo_postal):
        localidades = db.session.query(LocalidadModel).filter(LocalidadModel.cp == codigo_postal).all()
        return localidades