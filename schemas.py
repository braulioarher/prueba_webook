from marshmallow import Schema, fields

class PlainMunicipioSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PlainEstadoSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PlainLocalidadSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    cp = fields.Int(required=True)
    id_muni = fields.Int(required=True)

class LocalidadSchema(Schema):
    id_muni = fields.Int(required=True, load_only=True)

class MunicipioSchema(Schema):
    id_estado = fields.Int(required=True, load_only=True)
    estado = fields.Nested(PlainMunicipioSchema(), dump_only=True)

class EstadoSchema(PlainEstadoSchema):
    municipios = fields.List(fields.Nested(PlainMunicipioSchema()), dump_only=True)