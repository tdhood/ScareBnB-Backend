\echo 'Delete and recreate share_bnb db?'
\prompt 'Return for yes or control-C to cancel > ' foo

DROP DATABASE share_bnb;
CREATE DATABASE share_bnb;
\connect share_bnb

\i share_bnb-schema.sql
\i share_bnb-seed.sql

\echo 'Delete and recreate share_bnb_test db?'
\prompt 'Return for yes or control-C to cancel > ' foo

DROP DATABASE share_bnb_test;
CREATE DATABASE share_bnb_test;
\connect share_bnb_test

\i share_bnb-schema.sql
