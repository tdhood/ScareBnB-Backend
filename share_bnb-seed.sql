
INSERT INTO users (email, username, first_name, last_name, bio, password, is_host)
VALUES ('joel@joelburton.com',
        'testuser',
        'Test',
        'User',
        'test bio',
        'password',
        FALSE),
       ('test@host.com',
        'hostuser',
        'Host',
        'User2',
        'test bio2',
        '$2b$12$AZH7virni5jlTTiGgEg4zu3lSvAw68qVEfSIOjJ3RqtbJbdW/Oi5q',
        TRUE);

INSERT INTO listings (title, location, description, price, image_url, rating, user_id)
VALUES('pool',
        'San Fran',
    'Backyard pool to escape the heat',
    200,
    'https://leisurepoolsusa.com/wp-content/uploads/2020/06/best-type-of-swimming-pool-for-my-home_2.jpg',
    5,
    1),
    ('backyard',
    'San Jose',
    'the size of a parking space',
    150,
    'https://leisurepoolsusa.com/wp-content/uploads/2020/06/best-type-of-swimming-pool-for-my-home_2.jpg',
    5,
    1);


