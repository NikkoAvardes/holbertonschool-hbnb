-- Insert initial data into the database

-- Insert Administrator User - Using bcrypt-generator.com for hash bcrypt2 the password
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$6D/A418HGqInNHr.syUNf.HAyxcK6Uz2FB4yuiOQwSpytaoD48TTG',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insert User - Using bcrypt-generator.com for hash bcrypt2 the password
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc2',
    'User',
    'HBnB',
    'user@hbnb.io',
    'azerty123',
    FALSE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insert Initial Amenities - Using uuidgenerator.net pour generate UUID4
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES 
    ('2767d121-c1b4-4d16-a816-0f5113ab06d0', 'WiFi', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('bcf813cf-1fd0-4a7f-b69d-d4167331aaa1', 'Swimming Pool', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('32561383-c728-4ba3-9fd2-cb7ceab79fca', 'Air Conditioning', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);