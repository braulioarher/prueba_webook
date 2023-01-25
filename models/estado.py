from db import db

class EstadoModel(db.Model):
    __tablename__ = "estados"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    municipios = db.relationship("MunicipioModel", back_populates="estado", lazy="dynamic", cascade="all")