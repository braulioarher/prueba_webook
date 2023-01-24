from db import db

class EstadoModel(db.Model):
    __tablename__ = "estado"

    id = db.Column(db.Integer(2), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    municipios = db.relationship("MunicipioModel", back_populates="event", lazy="dynamic", cascade="all")