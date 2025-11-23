
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES
    ('a1b2c3d4-e5f6-7890-abcd-1234567890cd', 'Coffee Maker', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('b1c2d3e4-f5a6-8901-bcde-2345678901de', 'Smart TV', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO place_amenity (place_id, amenity_id) VALUES
    ('c3d4e5f6-a7b8-9012-cdef-3456789012cd', '2767d121-c1b4-4d16-a816-0f5113ab06d0'), -- WiFi
    ('c3d4e5f6-a7b8-9012-cdef-3456789012cd', '32561383-c728-4ba3-9fd2-cb7ceab79fca'), -- Air Conditioning
    ('c3d4e5f6-a7b8-9012-cdef-3456789012cd', 'a1b2c3d4-e5f6-7890-abcd-1234567890cd'), -- Coffee Maker
    ('c3d4e5f6-a7b8-9012-cdef-3456789012cd', 'b1c2d3e4-f5a6-8901-bcde-2345678901de'); -- Smart TV
-- Sunny Apartment: WiFi, Swimming Pool, Air Conditioning
INSERT INTO place_amenity (place_id, amenity_id) VALUES
    ('a1b2c3d4-e5f6-7890-abcd-1234567890ab', '2767d121-c1b4-4d16-a816-0f5113ab06d0'), -- WiFi
    ('a1b2c3d4-e5f6-7890-abcd-1234567890ab', 'bcf813cf-1fd0-4a7f-b69d-d4167331aaa1'), -- Swimming Pool
    ('a1b2c3d4-e5f6-7890-abcd-1234567890ab', '32561383-c728-4ba3-9fd2-cb7ceab79fca'); -- Air Conditioning

-- Cozy Loft: WiFi, Air Conditioning
INSERT INTO place_amenity (place_id, amenity_id) VALUES
    ('b2c3d4e5-f6a7-8901-bcde-2345678901bc', '2767d121-c1b4-4d16-a816-0f5113ab06d0'), -- WiFi
    ('b2c3d4e5-f6a7-8901-bcde-2345678901bc', '32561383-c728-4ba3-9fd2-cb7ceab79fca'); -- Air Conditioning

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

INSERT INTO amenities (id, name, created_at, updated_at)
VALUES 
    ('2767d121-c1b4-4d16-a816-0f5113ab06d0', 'WiFi', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('bcf813cf-1fd0-4a7f-b69d-d4167331aaa1', 'Swimming Pool', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('32561383-c728-4ba3-9fd2-cb7ceab79fca', 'Air Conditioning', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '550e8400-e29b-41d4-a716-446655440000',
    'Maria',
    'Garcia',
    'maria.garcia@example.com', -- test_user1234
    '$2b$12$N6HuyLoIbmo0xQgILZdJLeYyYUtLPi9CausIFTzg1krsOKz6h1H6u',
    FALSE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);


INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES
    ('a1b2c3d4-e5f6-7890-abcd-1234567890ab', 'Sunny Apartment', 'Appartement lumineux avec balcon', 120.00, 48.8566, 2.3522, '550e8400-e29b-41d4-a716-446655440000', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
	('c3d4e5f6-a7b8-9012-cdef-3456789012cd', 'Apartment', 'A cozy apartment with modern amenities, perfect for a relaxing stay.', 110.00, 40.7128, -74.0060, '550e8400-e29b-41d4-a716-446655440000', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('b2c3d4e5-f6a7-8901-bcde-2345678901bc', 'Cozy Loft', 'Loft confortable au centre-ville', 95.00, 45.7640, 4.8357, '550e8400-e29b-41d4-a716-446655440000', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
