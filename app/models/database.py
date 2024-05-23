import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

# Get the database
database = client["alma"]

# Get the collection
users_collection = database.get_collection("users")
leads_collection = database.get_collection("leads")
