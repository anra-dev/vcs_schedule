CREATE USER regvcs_admin WITH PASSWORD 'password';
CREATE DATABASE regvcs_db;
GRANT ALL PRIVILEGES ON DATABASE regvcs_db TO regvcs_admin;
