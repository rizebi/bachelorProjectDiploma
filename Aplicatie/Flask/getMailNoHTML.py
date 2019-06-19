from carplanner import db
from carplanner.models import Marca, RevizieDefault, User, Masina, Scadent

import smtplib

gmail_user = 'carplannerroot@gmail.com'
gmail_password = 'samsungS3'


def sendMail(email, subject, body):



  email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (gmail_user, email, subject, body)


  try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(gmail_user, email, email_text)
    server.close()

    print('Email sent!')
  except:
    print('Something went wrong...')





def getBody(mail):
  return "Mata Text"


if __name__ == '__main__':
  email = "carplannertest1@gmail.com"
  body = getBody(email)
  subject = "Mata"
  sendMail(email, subject, body)
