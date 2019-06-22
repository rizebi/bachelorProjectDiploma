from carplanner import db
from carplanner.models import Marca, RevizieDefault, User, Masina, Scadent
import csv
import datetime

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
  user = User("Popescu", "Ion", "carplannertest1@gmail.com", "parola1", "Personal")
  user.imagineProfil='carplannertest1@gmail.com.jpg'
  useri.append(user)
  useri.append(User("Georgescu", "Alexandru", "carplannertest2@gmail.com", "parola2", "TransportMarfa.SRL"))

  db.session.add_all(useri)
  db.session.commit()

def populateMasina():
  masini = []
  masini.append(Masina(1, 562, "Sotie", "VWER543ED354W1265", "Benzina", 1500, 2013, "BMN", "AG16UNU", "95435", "12", datetime.datetime(2019, 1, 24, 0, 0)))
  masini.append(Masina(1, 536, "Andrei", "TRER343ED354AA262", "Motorina", 1900, 2016, "AF45R", "AG99UNU", "135433", "34", datetime.datetime(2019, 3, 4, 0, 0)))
  masini.append(Masina(1, 485, "Personala", "WDB9061352N438162", "Motorina", 5000, 2019, "W629", "AG01UNU", "15430", "50", datetime.datetime(2019, 1, 16, 0, 0)))
  masini.append(Masina(1, 430, "Roxana", "LRF9061352R438100", "Electric", 0, 2017, "400W", "AG77UNU", "23430", "17", datetime.datetime(2018, 11, 24, 0, 0)))

  masini.append(Masina(2, 490, "Angajat1", "WDB9061352N438234", "Motorina", 2200, 2018, "W629", "AG13DOI", "195435", "102", datetime.datetime(2019, 5, 24, 0, 0)))
  masini.append(Masina(2, 490, "Angajat2", "WDB9061352N438654", "Motorina", 2200, 2018, "W629", "AG14DOI", "235433", "304", datetime.datetime(2019, 6, 1, 0, 0)))
  masini.append(Masina(2, 490, "Angajat3", "WDB9061352N438237", "Motorina", 2200, 2019, "W629", "AG15DOI", "215430", "250", datetime.datetime(2019, 4, 10, 0, 0)))
  masini.append(Masina(2, 490, "Angajat4", "WDB9061352N432354", "Motorina", 3000, 2017, "W629", "AG16DOI", "323430", "175", datetime.datetime(2019, 4, 7, 0, 0)))
  masini.append(Masina(2, 490, "Angajat5", "WDB90613523453252", "Motorina", 2200, 2019, "W629", "AG17DOI", "215430", "350", datetime.datetime(2019, 2, 27, 0, 0)))
  masini.append(Masina(2, 490, "Angajat6", "WDB90612312335787", "Motorina", 2200, 2017, "W628", "AG18DOI", "423430", "317", datetime.datetime(2019, 1, 15, 0, 0)))

  db.session.add_all(masini)
  db.session.commit()

def populateScadent():
  scadente = []
  #self, IDRevizie, numeScadent, IDMasina, dataExp, areKM, kmExp, viataZile, viataKm

  scadente.append(Scadent(2246, "Ulei + Filtre", 1, datetime.datetime(2019, 7, 24, 0, 0), True, 115435, 365, 15000))
  scadente.append(Scadent(2247, "Distributie", 1, datetime.datetime(2022, 5, 24, 0, 0), True, 145430, 1825, 60000))
  scadente.append(Scadent(2248, "Elemente franare", 1, datetime.datetime(2019, 8, 20, 0, 0), True, 135035, 1095, 40000))
  scadente.append(Scadent(2249, "Baterie", 1, datetime.datetime(2021, 1, 10, 0, 0), True, 215430, 1825, 60000))
  scadente.append(Scadent(1, "Asigurare", 1, datetime.datetime(2020, 1, 10, 0, 0), False, 0, 365, 0))
  scadente.append(Scadent(1, "ITP", 1, datetime.datetime(2019, 9, 19, 0, 0), False, 0, 730, 0))
  scadente.append(Scadent(1, "Rovigneta", 1, datetime.datetime(2019, 8, 23, 0, 0), False, 0, 365, 0))


  scadente.append(Scadent(2142, "Ulei + Filtre", 2, datetime.datetime(2019, 7, 14, 0, 0), True, 155433, 365, 15000))
  scadente.append(Scadent(2143, "Distributie", 2, datetime.datetime(2019, 8, 22, 0, 0), True, 195400, 1825, 60000))
  scadente.append(Scadent(2144, "Elemente franare", 2, datetime.datetime(2021, 5, 20, 0, 0), True, 185433, 1095, 40000))
  scadente.append(Scadent(2145, "Baterie", 2, datetime.datetime(2022, 2, 15, 0, 0), True, 215430, 205004, 60000))
  scadente.append(Scadent(1, "Asigurare", 2, datetime.datetime(2020, 2, 10, 0, 0), False, 0, 365, 0))
  scadente.append(Scadent(1, "ITP", 2, datetime.datetime(2019, 12, 19, 0, 0), False, 0, 730, 0))
  scadente.append(Scadent(1, "Rovigneta", 2, datetime.datetime(2020, 1, 23, 0, 0), False, 0, 365, 0))


  scadente.append(Scadent(1938, "Ulei + Filtre", 3, datetime.datetime(2020, 6, 24, 0, 0), True, 75430, 365, 15000))
  scadente.append(Scadent(1939, "Distributie", 3, datetime.datetime(2022, 6, 2, 0, 0), True, 105430, 1825, 60000))
  scadente.append(Scadent(1940, "Elemente franare", 3, datetime.datetime(2021, 6, 27, 0, 0), True, 95430, 1095, 40000))
  scadente.append(Scadent(1941, "Baterie", 3, datetime.datetime(2022, 6, 24, 0, 0), True, 125430, 1825, 60000))
  scadente.append(Scadent(1, "Asigurare", 3, datetime.datetime(2019, 11, 10, 0, 0), False, 0, 365, 0))
  scadente.append(Scadent(1, "ITP", 3, datetime.datetime(2019, 11, 1, 0, 0), False, 0, 730, 0))
  scadente.append(Scadent(1, "Rovigneta", 3, datetime.datetime(2020, 5, 15, 0, 0), False, 0, 365, 0))

  scadente.append(Scadent(1718, "Ulei + Filtre", 4, datetime.datetime(2019, 10, 24, 0, 0), True, 30430, 365, 15000))
  scadente.append(Scadent(1719, "Distributie", 4, datetime.datetime(2020, 7, 14, 0, 0), True, 63430, 1825, 60000))
  scadente.append(Scadent(1720, "Elemente franare", 4, datetime.datetime(2019, 12, 6, 0, 0), True, 53430, 1095, 40000))
  scadente.append(Scadent(1721, "Baterie", 4, datetime.datetime(2022, 1, 2, 0, 0), True, 73430, 1825, 60000))
  scadente.append(Scadent(1, "Asigurare", 4, datetime.datetime(2020, 1, 10, 0, 0), False, 0, 365, 0))
  scadente.append(Scadent(1, "ITP", 4, datetime.datetime(2019, 9, 10, 0, 0), False, 0, 730, 0))
  scadente.append(Scadent(1, "Rovigneta", 4, datetime.datetime(2020, 4, 5, 0, 0), False, 0, 365, 0))


  db.session.add_all(scadente)
  db.session.commit()

if __name__ == '__main__':
  populateMarca()
  populateRevizieDefault()
  populateUser()
  populateMasina()
  populateScadent()
