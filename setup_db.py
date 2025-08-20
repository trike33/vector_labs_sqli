# setup_db.py
import mysql.connector
from mysql.connector import errorcode
import yaml
import hashlib
import sys

# --- SECURITY WARNING ---
# This script uses MD5 for password hashing as requested for a specific
# demonstration scenario. MD5 is NOT secure and should NEVER be used
# for real password storage. Use libraries like Werkzeug or passlib instead.

def setup_database():
    """
    Connects to MySQL server, creates the database if it doesn't exist,
    then creates tables, admin user, and sample posts.
    """
    try:
        # Load database configuration from YAML file
        with open('db.yaml', 'r') as file:
            db_config = yaml.safe_load(file)
    except FileNotFoundError:
        print("Error: 'db.yaml' not found. Please create it with your database credentials.")
        sys.exit(1)

    db_name = db_config['mysql_db']

    try:
        # Step 1: Connect to the MySQL server (without specifying a database)
        db_connection = mysql.connector.connect(
            host=db_config['mysql_host'],
            user=db_config['mysql_user'],
            password=db_config['mysql_password']
        )
        cursor = db_connection.cursor()
        print("Successfully connected to MySQL server.")
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        sys.exit(1)

    try:
        # Step 2: Create the database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARACTER SET 'utf8'")
        print(f"Database '{db_name}' created or already exists.")
        # Switch to the newly created database
        cursor.execute(f"USE {db_name}")
    except mysql.connector.Error as err:
        print(f"Failed to create database: {err}")
        sys.exit(1)


    # Step 3: Create tables and insert data
    try:
        # --- Create 'users' table ---
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE
        )
        """)
        print("Table 'users' ready.")

        # --- Create 'posts' table ---
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            author VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        print("Table 'posts' ready.")

        # --- Create Admin User ---
        admin_user = 'blogpage_admin'
        admin_pass_hash = hashlib.md5('rockyou'.encode()).hexdigest()
        cursor.execute("SELECT id FROM users WHERE username = %s", (admin_user,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (%s, %s, TRUE)", (admin_user, admin_pass_hash))
            print(f"Admin user '{admin_user}' created.")
        else:
            print(f"Admin user '{admin_user}' already exists.")

        # --- Create Additional Users with Complex Passwords ---
        new_users = [
            ('alice_dev', 'P@ssw0rdStr0ng!'),
            ('bob_editor', 'Secur!ty_R0ck$'),
            ('charlie_ux', 'MyC0mpl3xP@ss'),
            ('diana_qa', 'An0th3r!@#Pwd'),
            ('ethan_ops', 'L33tH@x0rPwd'),
            ('fiona_pm', '!nt3rn3tS@f3ty'),
            ('george_data', 'Us3r_P@ss_987'),
            ('hannah_mktg', 'Web$ecure_2025')
        ]
        
        users_to_insert = []
        for username, password in new_users:
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cursor.fetchone() is None:
                hashed_password = hashlib.md5(password.encode()).hexdigest()
                users_to_insert.append((username, hashed_password, False))

        if users_to_insert:
            insert_user_query = "INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s)"
            cursor.executemany(insert_user_query, users_to_insert)
            print(f"Added {len(users_to_insert)} new users.")
        else:
            print("Additional users already exist.")

        # --- Add Sample Blog Posts ---
        cursor.execute("SELECT COUNT(*) FROM posts")
        if cursor.fetchone()[0] < 5:
            sample_posts = [
                ('First Post', 'This is the content of the very first post. Welcome to our new blog!', 'Admin'),
                ('Flask is Great', 'Here is a post about why Flask is a great web framework for building lightweight and powerful web applications in Python.', 'alice_dev'),
                ('Database Security', 'This post discusses the importance of preventing SQL injection by using parameterized queries and other best practices.', 'Admin'),
                ('A Deep Dive into SQL', 'Exploring advanced SQL queries like window functions, common table expressions (CTEs), and recursive queries can unlock powerful data insights.', 'george_data'),
                ('Frontend vs. Backend', 'What is the difference between frontend and backend development? This article breaks down the roles, technologies, and skills required for each path.', 'charlie_ux'),
                ('Containerization with Docker', 'An introduction to Docker for web developers. Learn how to package your application and its dependencies into a portable container.', 'ethan_ops'),
                ('The Art of Writing Good Content', 'Discover tips and tricks for creating engaging and well-structured blog posts that capture your audience\'s attention.', 'bob_editor')
            ]
            cursor.execute("DELETE FROM posts")
            insert_posts_query = "INSERT INTO posts (title, content, author) VALUES (%s, %s, %s)"
            cursor.executemany(insert_posts_query, sample_posts)
            print("Sample blog posts have been inserted.")
        else:
            print("Sample posts already exist.")

        db_connection.commit()

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    finally:
        cursor.close()
        db_connection.close()
        print("Database setup complete. Connection closed.")

if __name__ == '__main__':
    setup_database()
