import os.path
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

token = "/home/medinamaria90/mysite/token.json"

class EmailSender:
    def __init__(self, email, link=None):
        self.email = email
        self.subject = None
        self.body = None
        self.token = None
        self.link = link
        self.toadmin = False

    def send_message(self):
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        else:
            try:
                creds = Credentials.from_authorized_user_file(token, SCOPES)
            except Exception as e:
                print(e)

        try:
            service = build("gmail", "v1", credentials=creds)
            message = EmailMessage()
            message.set_content(self.body)
            if self.toadmin == True:
                message["To"] = "mmcprogramacion@gmail.com"
                self.toadmin = False
            else:
                message["To"] = self.email
            message["From"] = "mmcprogramacion@gmail.com"
            message["Subject"] = self.subject
            encoded_message = base64.urlsafe_b64encode(
                message.as_bytes()).decode()
            create_message = {"raw": encoded_message}
            print("trying to send")
            send_message = (
                service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )
            print(f'Message Id: {send_message["id"]}')
        except HttpError as error:
            print(f"An error occurred: {error}")
            send_message = None
        return send_message

    def send_sucess_email(self):
        self.body = '''ENGLISH
Your registration has been completed. You have 30 days of trial to use the software. These are the instructions:

Download the program and the sample Excel file that you will find in your user account.
Install the program. Windows may indicate that the program is not trusted as it is very new. You can click on "More Info" and then "Run Anyway." I guarantee it is safe.
Enter your email and the serial number that you will find in your user account.
Now you can start using it! You can use the downloaded Excel file as a template.
Oh! Super important! There will be a black window that opens while you use the program. This window is a subprocess. Never close it or you'll lose the information!

If you close the browser, you can retrieve the data obtained at any time.

If you have any questions, please write to us!


ESPAÑOL
Tu registro ha sido completado. Tienes 30 días de prueba para utilizar el software. Estas son las instrucciones:\n

- Descarga el programa y el excel de prueba que encontrarás en tu usuario  \n
- Instala el programa. Windows te puede indicar que el programa no es de confianza dado que es muy nuevo. Puedes darle a más información y despúes a ejecutar programa. ¡Te garantizo que es seguro \n
- Introduce tu email y el serial que verás en tu usuario\n
- ¡Ya puedes usarlo! Puedes utilizar el excel descargado como modelo.\n

¡Ah! ¡Super importante! hay una ventana negra que se abrirá mientras utilizas el programa. Esta ventana es un subproceso. ¡Nunca la cierres o perderás la información! \n

Si cierras el explorador, podrás recuperar los datos conseguidos en cualquier momento.\n

Cualquier duda, ¡Escribenos!'''
        self.subject = "¡Ya estás registrado!"
        self.send_message()
        self.send_admin_mail()

    def send_admin_mail(self):
        self.body = f"El usuario {self.email} se ha registrado en SEO TRACKER"
        self.subject = "Nuevo Registro de usuario"
        self.toadmin = True
        self.send_message()

    def send_reset_password_email(self):
        self.body = "Puedes cambiar tu contraseña haciendo click en el siguiente link. Si no has solicitado el cambio, no te preocupes, no sucederá nada. // You can change your password by clicking on the following link. If you haven't requested the change, don't worry, nothing will happen. {}".format(
            self.link)
        self.subject = "¡Cambia tu contraseña!"
        self.send_message()

    def send_confirmation_email(self):
        self.body = f'¡Gracias por registrarte! Entra en el siguiente link de registro para confirmar tu cuenta: {self.link}'
        self.subject = "Confirma tu cuenta para usar SEO Tracker"
        self.send_message()
