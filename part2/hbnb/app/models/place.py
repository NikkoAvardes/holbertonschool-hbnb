# TODO: Import required modules (uuid, datetime, etc.)
# TODO: Define Place class with the following attributes:
#       - id (string, unique identifier, auto-generated)
#       - title (string, required, max 100 characters)
#       - description (string, optional)
#       - price (float, required, must be positive)
#       - latitude (float, required, range -90.0 to 90.0)
#       - longitude (float, required, range -180.0 to 180.0)
#       - owner_id (string, required, foreign key to User)
#       - reviews (list, relationship to Review objects)
#       - amenities (list, relationship to Amenity objects)
#       - created_at (datetime, auto-generated)
#       - updated_at (datetime, auto-updated)
# TODO: Implement __init__ method with validation
# TODO: Implement validate_coordinates method
# TODO: Implement add_review method
# TODO: Implement add_amenity method
# TODO: Implement update method to modify place data
# TODO: Implement to_dict method for serialization
# TODO: Add business rule: owner cannot review their own place