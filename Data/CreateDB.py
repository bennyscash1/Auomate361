import pymongo

# Function to get headers
def get_headers(include_token=False, bearer_token=None):
    headers = {
        "Content-Type": "application/json"
    }
    if include_token and bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"
    return headers

# Data to insert into the database
data = {
  "API": {
    "Email": "eve.holt@reqres.in",
    "Password": "pistol",
    "BaseApiUrl": "https://reqres.in/api/",
    "Headers": get_headers(include_token=False)
  },
  "WebUi": {
    "WebUrl": "https://practicetestautomation.com/practice-test-login/",
    "WebUserName": "student",
    "WebPassword": "Password123"
  },
  "Mobile": {
    "ContactName": "בני",
    "ContactNumber": "0584102220",
    "appPackage": "com.google.android.contacts",
    "appActivity": "com.android.contacts.activities.PeopleActivity"
  },
  "Common": {
    "Enviorment": "dev"
  }
}

# Connect to MongoDB server
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']  # Replace 'mydatabase' with your database name
collection = db['config']  # Create or get collection named 'config'

# Insert data into the collection
collection.insert_one(data)

# Retrieve data from the collection
result = collection.find_one()
print(result)
