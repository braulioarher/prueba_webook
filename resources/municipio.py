from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app import db
from models import MunicipioModel
from schemas import PlainMunicipioSchema

blp = Blueprint("municipios", __name__, description="Opereaciones en municipios")

@blp.route("/municipio/<string:municipio_name>")
class Municipio(MethodView):
    @blp.response(200, PlainMunicipioSchema)
    def get(self, municipio_name):
        municipio = db.session.query(MunicipioModel).filter(MunicipioModel.name == municipio_name).first_or_404()
        return municipio

