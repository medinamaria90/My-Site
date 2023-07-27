from werkzeug.security import check_password_hash
from flask_login import UserMixin
from config import db, now


class Connection(db.Model, UserMixin):
    __tablename__ = 'conexiones'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    time_connection = db.Column(db.DateTime, default=now)
    time_disconnection = db.Column(db.DateTime)
    session_token = db.Column(db.String(100))
    valid_until = db.Column(db.DateTime)


class User(db.Model, UserMixin,):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20))
    apellidos = db.Column(db.String(30))
    email = db.Column(db.String(50), unique=True)
    fecha_registro = db.Column(db.Date)
    caducidad_suscripcion = db.Column(db.Date)
    password = db.Column(db.String(300))
    cuenta_activada = db.Column(db.Boolean)
    change_password_token =  db.Column(db.String(255))
    suscripcion_activa = ""
    password_check = ""
    access_token = db.Column(db.String(255))
    access_token_used = db.Column(db.Boolean)
    licenses = db.Column(db.Integer)
    connections = db.Column(db.Integer)

    def get_id(self):
        return self.id

    @staticmethod
    def check_password(hashed_password, password):
        return check_password_hash(hashed_password, password)

