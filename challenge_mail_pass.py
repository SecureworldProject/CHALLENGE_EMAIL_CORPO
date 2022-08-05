import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import random, re, time
import easygui
import os
from pathlib import Path


#VARIABLES GLOBALES
easy_mode = False #Testing only: Si lo pones a true no te manda el mail y te escribe la clave correcta automaticamente
props_dict={}
abece = "abcdefghijklmnopqrstuvwxyz" #Para generar de forma sencilla claves nuevas

#VARIABLES DE GESTION DEL EMAIL
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "secureworld.validator@gmail.com"  # Enter your address
password_sender = "" #Due to last gmail security update, the app password is used instead the regular password


# FUNCIONES AUXILIARES
def generate_mail_key(clave_real,distancia):
    mail_key = ""
    factor = random.choice(range(1,9))
    for letter in clave_real:
        #print(f"La letra orig es: {letter}")
        new_letter_index = (abece.find(letter)+(distancia*factor))%26
        mail_key += abece[new_letter_index]
    mail_key+=str(factor)
    #print("Por mail se envia: " + mail_key)
    return mail_key

def retrieve_key(mail_key, distancia):
    orig_key = ""
    #Cogemos el factor de la cadena, si no hay numeros el factor es cero
    match = re.search(r"[0-9]+",mail_key)
    if match:
        factor = int(match.group())
    else:
        factor = 0
    for letter in mail_key[:len(mail_key)-1]:
        #print(f"La letra orig es: {letter}")
        new_letter_index = (abece.find(letter)-(distancia*factor))%26
        orig_key += abece[new_letter_index]
    #print("La clave original era: "+ orig_key)
    return orig_key

def send_message(key_message, receiver_email):

    if receiver_email == "":
        print("ERROR: No hay destinatario del mail, te recuerdo que el destinatario esta en el param3 del challenge")
        return

    message = MIMEMultipart("alternative")
    message["Subject"] = "SecureWorld Auth"
    message["From"] = sender_email
    message["To"] = receiver_email


    #with open("secureworld.png", 'rb') as f:
    #    img_data = f.read()

    # Create the plain-text and HTML version of your message
    text = """\
    Version en texto plano:
    Tu clave es {key}, copiala con cuidado
    """.format(key = key_message)
    html = """\
    <html>
      <body>
        <p>Buenos dias,<br>
           Bienvenido al challenge de email corporativo
           Tu clave es: {key}
        </p>
      </body>
    </html>
    """.format(key=key_message)
    
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password_sender)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

# FUNCIONES DEL CHALLENGE
def init(props):
    global props_dict
    print("Python: Enter in init")
    
    #props es un diccionario
    props_dict= props

    return 0
    """
    res=executeChallenge()
    #check len retornada 
    if (res[1]>0):
        return 0
    else:
        #no se ha podido ejecutar
        return -1
    """

def executeChallenge():
    print("Starting execute")
    
    clave_real = props_dict["param1"] #La cojo de parametro pero seria mas seguro cogerla de otro lado
    distancia = props_dict["param2"]
    receiver_email = props_dict["param3"]
    

    #mecanismo de lock BEGIN, para garantizar una sola interaccion con user a la vez
    #-----------------------
    folder=os.environ['SECUREMIRROR_CAPTURES']
    while os.path.exists(folder+"/"+"lock"):
        time.sleep(1)
    Path(folder+"/"+"lock").touch()



    #Pulsa si, para que enviarte un correo con la clave
    send_mail=easygui.ynbox(msg='Pulsa Yes para recibir un email con la clave secreta',
                         choices=("Yes","Not"))
    if (send_mail==False):
        os.remove(folder+"/"+"lock")
        result = (0,0)
        print ("result:",result)
        return result

    clave_para_enviar = generate_mail_key(clave_real,distancia)
    if easy_mode:
        clave_enviada = easygui.enterbox("Enter password for corporative mail challenge", "Email Key", clave_para_enviar)
    else:
        send_message(clave_para_enviar, receiver_email)
        #pedimos password
        clave_enviada = easygui.enterbox("Enter password for corporative mail challenge", "Email Key", "")
    
    #ahora comparamos con la correcta
    
    clave_calculada = retrieve_key(clave_enviada, distancia)

    #construccion de la respuesta
    mode= props_dict["mode"]

    if (mode=="parental"):
        for i in range (0,2): # 3 intentos        
            if (clave_calculada==clave_real):
                cad="\0" #bytearray(0) #"%d"%(0)
                break
            else:
                clave_enviada = easygui.enterbox(f"Enter password for corporative mail challenge (Intento {i+2})", "chpass", "")
                clave_calculada = retrieve_key(clave_enviada, distancia)
                
        if (clave_calculada!=clave_real):
            cad="\1" #"%d"%(1)
        else :
            cad="\0" #"%d"%(0)
            
    else:#modo no parental
        cad=clave_calculada
    
    #mecanismo lock
    if os.path.exists(folder+"/"+"lock"):
        os.remove(folder+"/"+"lock")

    key = bytes(cad,'utf-8')
    key_size = len(key)

    result =(key, key_size)
    print ("result:",result)
    return result


if __name__ == "__main__":

    with open("password.txt","r") as f:
        password_sender=f.readline()

    #mode "parental" o "normal"
    midict={"param1": "secureworld",
            "param2": 43,
            "param3": "",
            "mode": "normal"}

    init(midict)
    executeChallenge()

