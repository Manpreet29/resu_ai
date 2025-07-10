from pymongo import MongoClient

# Replace with your actual username and password
mongo_uri = "mongodb+srv://manpreetsingh2904:<db_password>@cluster0.uvrttsq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB
client = MongoClient(mongo_uri)

# Access the database and collection
db = client["resu_ai"]  # Your database name
resumes_collection = db["resumes"]  # Your collection name
