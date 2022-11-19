
INSERT INTO users (email, username, first_name, last_name, bio, password, is_host)
VALUES ('user@email.com',
        'testuser',
        'Test',
        'User',
        'test bio',
        'password',
        FALSE),
       ('host@host.com',
        'hostuser',
        'Host',
        'User2',
        'test bio2',
        '$2b$12$AZH7virni5jlTTiGgEg4zu3lSvAw68qVEfSIOjJ3RqtbJbdW/Oi5q',
        TRUE);

INSERT INTO listings (title, object_name, location, description, price, image_url, rating, user_id)
VALUES('Hauntingly Isolated',
        'lakehouse',
        'Remote',
    'No one can hear you scream',
    200,
    'https://www.businessnhmagazine.com/UploadedFiles/Articles/8151/66581491_m.jpg',
    5,
    1);


