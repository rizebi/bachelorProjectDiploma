from carplanner import db
from carplanner.models import Marca, RevizieDefault
import csv

def populateMarca():
  with open('MarcaModel.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    masini = []
    for row in csv_reader:
      masina = Marca(row[0], row[1])
      masini.append(masina)

    db.session.add_all(masini)
    # Now save it to the database
    db.session.commit()

def populateRevizieDefault():
  toateMarcile = Marca.query.all()
  reviziiDefault = []
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
  # Now save it to the database
  db.session.commit()




if __name__ == '__main__':
  populateMarca()
  populateRevizieDefault()
