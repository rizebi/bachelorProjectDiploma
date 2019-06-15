from carplanner import db
from carplanner.models import Marca, RevizieDefault, User, Masina
import csv

def populateMarca():
  with open('MarcaModel.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    masini = []
    for row in csv_reader:
      masina = Marca(row[0], row[1])
      masini.append(masina)

    db.session.add_all(masini)
    db.session.commit()

def populateRevizieDefault():
  toateMarcile = Marca.query.all()
  reviziiDefault = []
  revizieDefault = RevizieDefault(1, "Custom", 0, 0)
  reviziiDefault.append(revizieDefault)
  
  for marca in toateMarcile:
    revizieDefault = RevizieDefault(marca.IDAuto, "Ulei + Filtre", 365, 15000)
    reviziiDefault.append(revizieDefault)
    revizieDefault = RevizieDefault(marca.IDAuto, "Distributie", 1825, 60000)
    reviziiDefault.append(revizieDefault)
    revizieDefault = RevizieDefault(marca.IDAuto, "Elemente franare", 1095, 40000)
    reviziiDefault.append(revizieDefault)
    revizieDefault = RevizieDefault(marca.IDAuto, "Baterie", 1825, 60000)
    reviziiDefault.append(revizieDefault)

  db.session.add_all(reviziiDefault)
  db.session.commit()

def populateUser():
  useri = []
  useri.append(User("Unulescu", "Unu", "1@1.com", "1", "Unu.SRL"))
  useri.append(User("Doiulescu", "Doi", "2@2.com", "2", "Doi.SRL"))

  db.session.add_all(useri)
  db.session.commit()

def populateMasina():
  masini = []
  masini.append(Masina(1, 562, "Sotie", "VWER543ED354W1265", "Benzina", 1500, 2013, "BMN", "AG16UNU", "95435", "12"))
  masini.append(Masina(1, 536, "Andrei", "TRER343ED354AA262", "Motorina", 1900, 2016, "AF45R", "AG99UNU", "135433", "34"))
  masini.append(Masina(1, 485, "Personala", "WDB9061352N438162", "Motorina", 5000, 2019, "W629", "AG01UNU", "15430", "50"))
  masini.append(Masina(1, 430, "Roxana", "LRF9061352R438100", "Electric", 0, 2017, "400W", "AG77UNU", "23430", "17"))

  masini.append(Masina(2, 562, "Angajat1", "WDB9061352N438234", "Motorina", 2200, 2018, "W629", "AG13DOI", "195435", "102"))
  masini.append(Masina(2, 536, "Angajat2", "WDB9061352N438654", "Motorina", 2200, 2018, "W629", "AG14DOI", "235433", "304"))
  masini.append(Masina(2, 485, "Angajat3", "WDB9061352N438237", "Motorina", 2200, 2019, "W629", "AG15DOI", "215430", "250"))
  masini.append(Masina(2, 430, "Angajat4", "WDB9061352N432354", "Motorina", 3000, 2017, "W629", "AG16DOI", "323430", "175"))
  masini.append(Masina(2, 485, "Angajat5", "WDB90613523453252", "Motorina", 2200, 2019, "W629", "AG17DOI", "215430", "350"))
  masini.append(Masina(2, 430, "Angajat6", "WDB90612312335787", "Motorina", 2200, 2017, "W628", "AG18DOI", "423430", "317"))

  db.session.add_all(masini)
  db.session.commit()

if __name__ == '__main__':
  populateMarca()
  populateRevizieDefault()
  populateUser()
  populateMasina()
