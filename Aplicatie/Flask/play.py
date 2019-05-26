from carplanner import db
from carplanner.models import *

toateMarcile = Marca.query.all()
for marca in toateMarcile:
  print(marca.IDAuto)
