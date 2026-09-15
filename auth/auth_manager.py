import bcrypt
from bson import ObjectId
from datetime import datetime, timezone

try:
    from auth.database import users_collection
except ModuleNotFoundError:
    from database import users_collection


# =========================================================
# PASSWORD FUNCTIONS
# =========================================================

def hash_password(password):
    """
    Hash a plain-text password before storing it in MongoDB.
    """
    password_bytes = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed_password.decode("utf-8")


def verify_password(password, password_hash):
    """
    Check whether the entered password matches
    the password hash stored in MongoDB.
    """
    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    )


# =========================================================
# REGISTER USER
# =========================================================

def register_user(name, email, password):
    # Clean user input
    name = name.strip()
    email = email.strip().lower()

    # Basic validation
    if not name or not email or not password:
        return {
            "success": False,
            "message": "All fields are required."
        }

    # Check whether the email is already registered
    existing_user = users_collection.find_one({
        "email": email
    })

    if existing_user:
        return {
            "success": False,
            "message": "An account with this email already exists."
        }

    # Hash the password
    password_hash = hash_password(password)

    # Create the new user
    user = {
        "name": name,
        "email": email,
        "password_hash": password_hash,
        "account_type": "free",
        "created_at": datetime.now(timezone.utc)
    }

    # Save user in MongoDB
    result = users_collection.insert_one(user)

    return {
        "success": True,
        "message": "Account created successfully!",
        "user_id": str(result.inserted_id)
    }


# =========================================================
# LOGIN USER
# =========================================================

def login_user(email, password):
    # Clean email input
    email = email.strip().lower()

    # Basic validation
    if not email or not password:
        return {
            "success": False,
            "message": "Email and password are required."
        }

    # Find user in MongoDB
    user = users_collection.find_one({
        "email": email
    })

    # User does not exist
    if not user:
        return {
            "success": False,
            "message": "Invalid email or password."
        }

    # Check password
    if not verify_password(password, user["password_hash"]):
        return {
            "success": False,
            "message": "Invalid email or password."
        }

    # Login successful
    return {
        "success": True,
        "message": "Login successful!",
        "user": {
            "user_id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "account_type": user["account_type"]
        }
    }


# =========================================================
# UPGRADE USER TO PREMIUM
# =========================================================

def upgrade_user(user_id):

    try:
        # Convert the user ID string back to MongoDB ObjectId
        object_id = ObjectId(user_id)

        # Update the account type
        result = users_collection.update_one(
            {"_id": object_id},
            {
                "$set": {
                    "account_type": "premium"
                }
            }
        )

        # User was not found
        if result.matched_count == 0:
            return {
                "success": False,
                "message": "User account not found."
            }

        # Upgrade successful
        return {
            "success": True,
            "message": "Account upgraded to Premium successfully!"
        }

    except Exception as error:
        return {
            "success": False,
            "message": f"Unable to upgrade account: {error}"
        }


# =========================================================
# TEMPORARY LOGIN TEST
# =========================================================

if __name__ == "__main__":
    result = login_user(
        email="test@example.com",
        password="TestPassword123"
    )

    print(result)