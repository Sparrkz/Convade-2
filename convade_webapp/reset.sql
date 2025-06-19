DROP DATABASE IF EXISTS convadedb;
CREATE DATABASE convadedb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CREATE USER IF NOT EXISTS 'conavdedaniel'@'localhost' IDENTIFIED BY 'gJ#8wPz7!mTc2L@q9FbK';
GRANT ALL PRIVILEGES ON convadedb.* TO 'conavdedaniel'@'localhost';
FLUSH PRIVILEGES;
