from db import db

class LocalidadModel(db.Model):
    __tablename__ = "localidades"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    cp = db.Column(db.Integer, unique=False, nullable=False)
    id_muni = db.Column(db.Integer, db.ForeignKey("municipios.id"), unique=False, nullable=False)