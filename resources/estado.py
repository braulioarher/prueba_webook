from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app import db
from models import EstadoModel
from schemas import EstadoSchema, PlainEstadoSchema

blp = Blueprint("estados", __name__, description="Opereaciones en estados")

@blp.route("/estado/<string:estado_name>")
class Estado(MethodView):
    @blp.response(200, EstadoSchema)
    def get(self, estado_name):
        estado = db.session.query(EstadoModel).filter(EstadoModel.name == estado_name).first_or_404()
        return estado

@blp.route("/estados")
class EstadoList(MethodView):
    @blp.response(200, PlainEstadoSchema(many=True))
    def get(self):
        estados = EstadoModel.query.all()
        return estados