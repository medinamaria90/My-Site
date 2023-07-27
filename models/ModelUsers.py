from datetime import timedelta
from models.entities.User import User, Connection
from werkzeug.security import generate_password_hash
from config import db, current_date
import random
import string
import traceback
import datetime



class ModelUser():
    @classmethod
    def check_suscription(cls, user):
        if user.caducidad_suscripcion is not None and user.caducidad_suscripcion > current_date:
            user.suscripcion_activa = 1
        else:
            user.suscripcion_activa = 0
        return user

    @classmethod
    def login(cls, email, password):
        try:
            db_user = User.query.filter_by(email=email).first()
            if db_user:
                db_user.password_check=User.check_password(db_user.password, password)
                if db_user.password_check:
                    db_user = cls.check_suscription(db_user)
                    return db_user
            return None
        except Exception as ex:
            traceback.print_exc()
            print(ex)

    @classmethod
    def get_by_id(cls, id):
        try:
            id = User.query.get(id)

            return id
        except Exception as ex:
            print(ex)

    @classmethod
    def register(cls, email, nombre, apellidos, password):
        # Esta funcion retorna True si el usuario NO está registrado o su cuenta NO esta activada, y FALSE si ya existe
        try:
            db_user = User.query.filter_by(email=email).first()
            if db_user is None:
                # Si el usuario que se pretende registrar no existe, creamos uno nuevo y le asignamos cuenta activada = "N", porque en este punto aun no han confirmado el email
                encripted_password = generate_password_hash(
                    password,
                    method='pbkdf2:sha256',
                    salt_length=8
                )
                new_user = User(
                    email=email,
                    password=encripted_password,
                    nombre=nombre,
                    apellidos=apellidos,
                    cuenta_activada=0,
                    fecha_registro=current_date,
                    licenses = 2,
                )
                db.session.add(new_user)
                db.session.commit()
                return True
            else:
                #En el caso se que ya haya un usuario, checkeamos si la cuenta está activada
                if db_user.cuenta_activada == 0:
                # Si la cuenta no está activada, retornamos True
                    return True
                else:
                    return False
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def store_access_token(cls, user):
        user_to_store = db.session.query(User).filter_by(email=user.email).first()
        if user_to_store:
            token = (''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=23)))
            user_to_store.access_token = token
            user_to_store.access_token_used = 0
            db.session.commit()
    @classmethod
    def extend_suscription(cls, user):
        user_to_extend = db.session.query(User).filter_by(email=user.email).first()
        if user_to_extend:
            expiration_date =current_date.replace(month=current_date.month + 1)
            user_to_extend.caducidad_suscripcion = expiration_date
            db.session.commit()

    @classmethod
    def terminate_registration(cls, email):
        existing_user = db.session.query(User).filter_by(email=email).first()
        if existing_user is not None:
            existing_user.cuenta_activada = 1
            cls.store_access_token(existing_user)
            cls.extend_suscription(existing_user)
            db.session.commit()

    @classmethod
    def get_by_email(cls, email):
        try:
            existing_user = db.session.query(User).filter_by(email=email).first()
            if existing_user is not None:
                return True
            else:
                return False
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def reset_password(cls, email, password):
        try:
            existing_user = db.session.query(User).filter_by(email=email).first()
            if existing_user is not None:
                existing_user.password = generate_password_hash(
                    password,
                    method='pbkdf2:sha256',
                    salt_length=8)
                db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            print(e)

    @classmethod
    def store_change_password_token(cls, email, token):
        existing_user = db.session.query(User).filter_by(email=email).first()
        if existing_user is not None:
            existing_user.change_password_token = token
            db.session.commit()

    @classmethod
    def new_api_session(cls, user):
        session_token = (''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=23)))
        new_connection = Connection(
            email=user.email,
            time_connection= datetime.datetime.now(),
            session_token=session_token,
            valid_until = datetime.datetime.now() + timedelta(seconds=120)
        )
        db.session.add(new_connection)
        db.session.commit()
        user.connections += 1
        db.session.commit()
        return session_token

    @classmethod
    def api_report_status(cls, session_token):
        try:
            existing_connection = db.session.query(Connection).filter_by(session_token=session_token).first()
            if existing_connection:
                existing_connection.valid_until = datetime.datetime.now() + timedelta(seconds=120)
                existing_connection.time_disconnection = datetime.datetime.now()
                db.session.commit()
                return True
            else:
                return False
        except:
            return False

    @classmethod
    def disconnect_session_token(cls, session_token):
        try:
            existing_connection = db.session.query(Connection).filter_by(session_token=session_token).first()
            if existing_connection:
                print("this connection exists")
                existing_connection.valid_until = None
                existing_connection.session_token = None
                existing_connection.time_disconnection = datetime.datetime.now()
                db.session.commit()
                return True
            else:
                print("this connection doesnt exist")
                return False
        except:
            return False

    @classmethod
    def remove_user_connection(cls, access_token):
        try:
            existing_user = db.session.query(User).filter_by(access_token=access_token).first()
            if existing_user:
                existing_user.connections -= 1
                db.session.commit()
                return True
            else:
                return False
        except:
            traceback.print_exc()
            return False


    @classmethod
    def api_logout(cls, session_token, access_token):
        disconnected_session = False
        removed_user = False
        print(session_token, access_token)
        if session_token is not None:
            disconnected_session = cls.disconnect_session_token(session_token=session_token)
        if access_token is not None:
            removed_user = cls.remove_user_connection(access_token=access_token)
        print(disconnected_session, removed_user)
        return {
            "disconnected_session" : disconnected_session,
            "removed_user": removed_user
            }

    @classmethod
    def api_login(cls, token, email):
        try:
            # If they entered the email...
            if email:
                db_user = db.session.query(User).filter_by(access_token=token, email=email).first()
                if db_user:
                    db_user.access_token_used = 1
                    db.session.commit()
            # If they entered with the token....
            else:
                db_user = db.session.query(User).filter_by(access_token=token).first()
            # If there is a valid user
            if db_user:
                user = True
                if db_user.connections<150:
                    max_connections = False
                else:
                    max_connections = True
                # we update the user to check if there is an active suscription
                db_user =  cls.check_suscription(db_user)
                if db_user.suscripcion_activa == 1:
                    session_token = cls.new_api_session(db_user)
                    suscripcion_activa =True
                else:
                    suscripcion_activa = False
                    session_token = None
            else:
                user = False

            return {
                "user" : user,
                "session_token" : session_token,
                "suscripcion_activa" : suscripcion_activa,
                "max_connections" : max_connections,
            }

        except Exception as e:
            return {"error": str(e)}
            traceback.print_exc()


    @classmethod
    def token_exist(cls, email, token):
        existing_user = db.session.query(User).filter_by(email=email).first()
        if existing_user.change_password_token == token:
            return True
        else:
            return False

    @classmethod
    def delete_used_token(cls, email):
        existing_user = db.session.query(User).filter_by(email=email).first()
        existing_user.change_password_token = ''
        db.session.commit()


