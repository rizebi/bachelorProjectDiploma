from carplanner import db
from carplanner.models import Marca
import csv

with open('MarcaModel.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  masini = []
  for row in csv_reader:
    masina = Marca(row[0], row[1])
    masini.append(masina)

  db.session.add_all(masini)
  # Now save it to the database
  db.session.commit()
