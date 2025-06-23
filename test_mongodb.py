from pymongo.mongo_client import MongoClient

# URL-encoded password: Replace '@' with '%40'
uri = "mongodb+srv://syamkklr1133:Syam%401133@cluster0.mhgc8xi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)