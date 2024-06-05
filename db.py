from pymongo import MongoClient

def get_database():
   client = MongoClient("mongodb://localhost:27017")
   return client['scrapeX']
  
if __name__ == "__main__":   
   dbname = get_database()
