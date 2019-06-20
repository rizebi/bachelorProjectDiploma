import smtplib
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


def getBody(user):

  #masini = db.session.query(Masina).filter(Masina.IDUser == user.IDUser).all()

  #masini, marci = db.session.query(Masina, Marca).filter(Masina.IDAuto == Marca.IDAuto, Masina.proprietar == user).all():

  #print(masini)

  scadenteLista = []

  for masina, marca in db.session.query(Masina, Marca).filter(Masina.IDAuto == Marca.IDAuto, Masina.proprietar == user).all():
    scadente = db.session.query(Scadent).filter(Scadent.IDMasina == masina.IDMasina).all()

    for scadent in scadente:
      scadentObj = {}
      print(scadent.numeScadent, masina.numarInmatriculare, marca.marcaMasina, marca.modelMasina)


  body = """\
<html>
  <head></head>
  <body>

  <h2>Basic HTML Table</h2>

  <table style="width:100%">
    <tr>
      <th>Firstname</th>
      <th>Lastname</th>
      <th>Age</th>
    </tr>
    <tr>
      <td>Jill</td>
      <td>Smith</td>
      <td>50</td>
    </tr>
    <tr>
      <td>Eve</td>
      <td>Jackson</td>
      <td>94</td>
    </tr>
    <tr>
      <td>John</td>
      <td>Doe</td>
      <td>80</td>
    </tr>
  </table>

  </body>
</html>
"""
  return body


if __name__ == '__main__':

  subject = "Notificare saptamanala status scadente"
  users = db.session.query(User).all()
  for user in users:
    print("Starting " + user.email)
    body = getBody(user)
    #sendMail(email, subject, body)
