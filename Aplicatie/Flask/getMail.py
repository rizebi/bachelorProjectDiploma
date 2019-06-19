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


def getBody(mail):


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
  email = "carplannertest1@gmail.com"
  body = getBody(email)
  subject = "Mata"
  sendMail(email, subject, body)
