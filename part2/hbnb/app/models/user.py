# TODO: Import required modules (uuid, datetime, etc.)
# TODO: Define User class with the following attributes:
#       - id (string, unique identifier, auto-generated)
#       - first_name (string, required, max 50 characters)
#       - last_name (string, required, max 50 characters)  
#       - email (string, required, unique, valid email format)
#       - password (string, required, min 6 characters, hashed)
#       - is_admin (boolean, default False)
#       - created_at (datetime, auto-generated)
#       - updated_at (datetime, auto-updated)
# TODO: Implement __init__ method with validation
# TODO: Implement validate_email method
# TODO: Implement hash_password method
# TODO: Implement update method to modify user data
# TODO: Implement to_dict method for serialization
# TODO: Add business rule: email must be unique across all users