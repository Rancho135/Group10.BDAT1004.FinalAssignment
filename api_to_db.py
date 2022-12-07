import requests
import time
import pymongo
import json

#make an API call and store the respone
#url1 = 'https://api.openweathermap.org/data/2.5/weather?q=London,CA&appid=4862887cedf2ef1a27d4b078649921f0'


def api_to_db():

  try:
  
    client = pymongo.MongoClient("mongodb+srv://BDAT:1004@openweatherdata.8d4derw.mongodb.net/?ss1=true&ss1_cert_reqs=CERT_NONE")
    db = client.get_database('openweatherApi')
    records = db.openweather_db
    pass
  except ServerSelectionTimeoutError:
    pass
  
  
  while True:
      cities_list = ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton', 'Ottawa', 'Winnipeg', 'Quebec City',
                     'Hamilton', 'Kitchener', 'London', 'Victoria', 'Halifax', 'Oshawa', 'Windsor', 'Saskatoon',
                     'St. Catharines', 'Regina', 'St. Johns', 'Kelowna', 'Barrie']
      for city_name in cities_list:
          r=requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name},CA&appid=4862887cedf2ef1a27d4b078649921f0")
          if r.status_code == 200:
              data = r.json()
              #print(data)
              records.insert_one(data)
              time.sleep(50)
          else:
              exit()


          return data

        