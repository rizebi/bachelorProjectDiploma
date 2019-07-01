import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from carplanner import db
from carplanner.models import Marca, RevizieDefault, User, Masina, Scadent


gmail_user = 'carplannerroot@gmail.com'
gmail_password = 'samsungS3'

def sendMail(email, subject, body):

  msg = MIMEMultipart('alternative')
  msg['Subject'] = subject
  msg['From'] = gmail_user
  msg['To'] = email

  HTMLpart = MIMEText(body, 'html')
  msg.attach(HTMLpart)

  try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(gmail_user, email, msg.as_string())
    server.close()

    print('Email sent to ' + email)
  except:
    print('Something went wrong when sending email to ' + email)


def sortDate(obj):
  return obj["dataExp"]

def getBody(user):

  now = datetime.datetime.now().date()

  scadenteLista = []

  for masina, marca in db.session.query(Masina, Marca).filter(Masina.IDAuto == Marca.IDAuto, Masina.proprietar == user).all():
    scadente = db.session.query(Scadent).filter(Scadent.IDMasina == masina.IDMasina).all()

    for scadent in scadente:
      if (scadent.dataExp - now).days <= 3:
        if scadent.areKM is False:
          scadenteLista.append({"areKm":False, "numeScadent":scadent.numeScadent, "marcaMasina":marca.marcaMasina, "modelMasina":marca.modelMasina, "numarInmatriculare":masina.numarInmatriculare, "dataExp":scadent.dataExp, "kmExp":"NA"})
        else:
          scadenteLista.append({"areKm":True, "numeScadent":scadent.numeScadent, "marcaMasina":marca.marcaMasina, "modelMasina":marca.modelMasina, "numarInmatriculare":masina.numarInmatriculare, "dataExp":scadent.dataExp, "kmExp":scadent.kmExp})

  if user.prenumeUser is None or user.prenumeUser == "" or user.prenumeUser == " ":
    nume = user.email.split("@")[0]
  else:
    nume = user.prenumeUser

  body = ""
  nevoie = False

  if len(scadenteLista) == 0:
    body += "<b>Salut " + nume + "!</b><br>"
    body += "<br>"
    body += "Din pacate nu ai nici un scadent in baza noastra de date."
    body += "<br>"
    body += "Pentru mai multe detalii si pentru a adauga scadente, intra in <a href='https://carplanner.ro/" + user.email + "'>contul tau</a></b>"
  else:
    scadenteLista.sort(key=sortDate)
    nevoie = True

    body += "<style> \ntable, th, td { \nborder: 1px solid black; \nborder-collapse: collapse; \n} \n th, td { \npadding: 5px; \ntext-align: left; \n" + " white-space:pre \n} \n</style>";
    body += "<b>Salut " + nume + "!</b><br><br>"
    body += "Mai jos gasesti o lista cu scadentele cu durata de viata mai mica de 3 zile sau care au expirat:<br><br>"

    body += "\n\n<table style=\"border: 1px solid black\">";
    body += "\n<tr>";
    body += "<th>Marca masina</th>";
    body += "<th>Model masina</th>";
    body += "<th>Numar Inmatriculare</th>";
    body += "<th>Nume Scadent</th>";
    body += "<th>Data expiraare</th>";
    body += "<th>Km expirare</th>";
    body += "</tr>"

    for scadent in scadenteLista:
      body += "<tr>"
      body += "<td>" + scadent["marcaMasina"] + "</td>"
      body += "<td>" + scadent["modelMasina"] + "</td>"
      body += "<td><b>" + scadent["numarInmatriculare"] + "</b></td>"
      body += "<td>" + scadent["numeScadent"] + "</td>"
      body += "<td>" + str(scadent["dataExp"]) + "</td>"
      body += "<td>" + str(scadent["kmExp"]) + "</td>"
      body += "</tr>"


    body += "</table>"
    body += "<br><br>"

    body += "<b>Pentru mai multe detalii poti intra in <a href='https://carplanner.ro/" + user.email + "'>contul tau</a></b>"



  return {'nevoie':nevoie, 'body':body}


if __name__ == '__main__':

  subject = "Alerta scadent!"
  users = db.session.query(User).all()
  for user in users:
    print("Starting " + user.email)
    response = getBody(user)
    if response['nevoie'] is True:
      sendMail(user.email, subject, response['body'])
