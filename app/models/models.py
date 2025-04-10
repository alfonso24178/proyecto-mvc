from app import db

class Nivel(db.Model):
    __tablename__ = 'niveles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class Municipio(db.Model):
    __tablename__ = 'municipios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class Asunto(db.Model):
    __tablename__ = 'asuntos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class SolicitudTurno(db.Model):
    __tablename__ = 'solicitud_turno'
    id = db.Column(db.Integer, primary_key=True)
    curp = db.Column(db.String(18), nullable=False)
    nombre_tramite = db.Column(db.String(100))
    nombre = db.Column(db.String(100))
    paterno = db.Column(db.String(100))
    materno = db.Column(db.String(100))
    telefono = db.Column(db.String(15))
    celular = db.Column(db.String(15))
    correo = db.Column(db.String(100))
    id_nivel = db.Column(db.Integer, db.ForeignKey('niveles.id'))
    id_municipio = db.Column(db.Integer, db.ForeignKey('municipios.id'))
    id_asunto = db.Column(db.Integer, db.ForeignKey('asuntos.id'))
    turno = db.Column(db.Integer)
    estatus = db.Column(db.Enum('Pendiente', 'Resuelto'), default='Pendiente')
    fecha_registro = db.Column(db.DateTime, server_default=db.func.now())

    nivel = db.relationship('Nivel')
    municipio = db.relationship('Municipio')
    asunto = db.relationship('Asunto')
