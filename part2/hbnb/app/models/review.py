# TODO: Import required modules (uuid, datetime, etc.)
# TODO: Define Review class with the following attributes:
#       - id (string, unique identifier, auto-generated)
#       - text (string, required)
#       - rating (integer, required, range 1-5)
#       - user_id (string, required, foreign key to User)
#       - place_id (string, required, foreign key to Place)
#       - created_at (datetime, auto-generated)
#       - updated_at (datetime, auto-updated)
# TODO: Implement __init__ method with validation
# TODO: Implement validate_rating method (must be 1-5)
# TODO: Implement update method to modify review data
# TODO: Implement to_dict method for serialization
# TODO: Add business rule: user can only have one review per place
# TODO: Add business rule: user cannot review their own place