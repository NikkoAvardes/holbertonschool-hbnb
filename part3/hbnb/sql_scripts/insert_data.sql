-- Script SQL pour insérer les données initiales dans la base HBnB
-- Ce fichier ajoute l'utilisateur admin et les commodités de départ.

INSERT INTO users (id, email, first_name, last_name, password, is_admin)
VALUE ("36c9050e-ddd3-4c3b-9731-9f487208bbc1", "admin@hbnb.io", "Admin", "HBnB", "$2b$12$2GYovIRj3KCi2hjvRh0Gcu9o.f19B0Rr8lZo0AJHBbKWc0sjGc7Yi", true);

INSERT INTO amenities (id, name) VALUES 
("df0a11be-f30d-4a85-b532-64f420d3ddca", "WiFi"),
("1ec9c5ce-5317-4a99-b4ab-c92842f252a7", "Swimming Pool"),
("7282922e-fb89-4219-ac23-714b8254b085", "Air Conditioning");