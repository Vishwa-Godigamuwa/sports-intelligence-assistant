import os
import certifi

from dotenv import load_dotenv
from pymongo import MongoClient


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise ValueError(
        "MONGODB_URI was not found in the .env file."
    )


# =========================================================
# CONNECT TO MONGODB
# =========================================================

client = MongoClient(
    MONGODB_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=30000
)


# =========================================================
# DATABASE AND COLLECTION
# =========================================================

db = client["sports_intelligence_assistant"]

users_collection = db["users"]


# =========================================================
# CONNECTION TEST
# =========================================================

def test_connection():

    try:
        client.admin.command("ping")

        print("MongoDB connection successful!")

    except Exception as error:

        print("MongoDB connection failed!")
        print(error)


# =========================================================
# TEMPORARY TEST
# =========================================================

if __name__ == "__main__":
    test_connection()