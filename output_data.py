# import all required python Lib
import time
import pymongo
import json



def get_weather():
  try:

    client = pymongo.MongoClient(
          "mongodb+srv://BDAT:1004@openweatherdata.8d4derw.mongodb.net/?ss1=true&ss1_cert_reqs=CERT_NONE"
      )
    db = client.get_database('openweatherApi')
    records = db.openweather_db

    pass

  except ServerSelectionTimeoutError:
    pass


   
  
    return records
