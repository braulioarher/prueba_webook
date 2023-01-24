from db import db

class MunicipioModel(db.Model):
    __tablename__ = "municipios"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    id_estado = db.Column(db.Integer, db.ForeignKey("estados.id"), unique=False, nullable=False)
    estado = db.relationship("EstadoModel", back_populates="municipios")
    localidad = db.relationship("LocalidadModel")