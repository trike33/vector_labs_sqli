# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import yaml
import hashlib # Import hashlib for MD5
import logging # Import the logging module
from functools import wraps

# Initialize the Flask application
app = Flask(__name__)

# --- Logging Configuration ---
# This will print logs to the console, including our custom SQL query logs.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# --- Database Configuration ---
try:
    db_config = yaml.safe_load(open('db.yaml'))
    app.config['MYSQL_HOST'] = db_config['mysql_host']
    app.config['MYSQL_USER'] = db_config['mysql_user']
    app.config['MYSQL_PASSWORD'] = db_config['mysql_password']
    app.config['MYSQL_DB'] = db_config['mysql_db']
    app.config['SECRET_KEY'] = 'a_very_secret_key_that_is_long_and_random_b9a8f7c6'
except FileNotFoundError:
    app.logger.error("FATAL: 'db.yaml' not found. Please create it with your database credentials.")
    exit()


# Initialize the MySQL extension
mysql = MySQL(app)

# --- Decorators for Access Control ---

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# --- Routes ---

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    query = "SELECT id, title, content, author, created_at FROM posts ORDER BY created_at DESC"
    app.logger.info(f"Executing query: {query}")
    cur.execute(query)
    posts = cur.fetchall()
    cur.close()
    return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        cur = mysql.connection.cursor()
        query = "SELECT id, username, password, is_admin FROM users WHERE username = %s"
        app.logger.info(f"Executing query: {query} with params: ('{username}',)")
        result = cur.execute(query, [username])

        if result > 0:
            data = cur.fetchone()
            user_id, db_username, password_hash_from_db, is_admin = data
            cur.close()

            candidate_hash = hashlib.md5(password_candidate.encode()).hexdigest()

            if candidate_hash == password_hash_from_db:
                session['logged_in'] = True
                session['username'] = db_username
                session['is_admin'] = is_admin
                flash('You are now logged in', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid login credentials', 'danger')
        else:
            cur.close()
            flash('Invalid login credentials', 'danger')
        
        return render_template('login.html')

    return render_template('login.html')

@app.route('/users')
@login_required
@admin_required
def users():
    cur = mysql.connection.cursor()
    query = "SELECT id, username, is_admin FROM users"
    app.logger.info(f"Executing query: {query}")
    cur.execute(query)
    user_list = cur.fetchall()
    cur.close()
    return render_template('users.html', users=user_list)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    cur = mysql.connection.cursor()
    
    query_select = "SELECT username FROM users WHERE id = %s"
    app.logger.info(f"Executing query: {query_select} with params: ({user_id},)")
    cur.execute(query_select, [user_id])
    user_to_delete = cur.fetchone()

    if user_to_delete and user_to_delete[0] == session['username']:
        flash('You cannot delete your own account.', 'danger')
        cur.close()
        return redirect(url_for('users'))

    query_delete = "DELETE FROM users WHERE id = %s"
    app.logger.info(f"Executing query: {query_delete} with params: ({user_id},)")
    cur.execute(query_delete, [user_id])
    mysql.connection.commit()
    cur.close()
    flash('User has been deleted.', 'success')
    return redirect(url_for('users'))

# --- SECURE FUNCTION ---
@app.route('/search')
def search():
    search_query = request.args.get('q')
    if not search_query:
        return redirect(url_for('index'))

    cur = mysql.connection.cursor()
    query = "SELECT id, title, content, author, created_at FROM posts WHERE title LIKE %s OR content LIKE %s"
    search_term = f"%{search_query}%"
    
    app.logger.info(f"Executing query: {query} with params: ('{search_term}', '{search_term}')")
    cur.execute(query, [search_term, search_term])
    
    posts = cur.fetchall()
    cur.close()
    
    if not posts:
        flash(f"No results found for '{search_query}'", 'warning')
    
    return render_template('search_results.html', posts=posts, query=search_query)

# --- ERROR-BASED and UNION-BASED VULNERABLE FUNCTION ---
@app.route('/search_vulnerable')
def search_vulnerable():
    search_query = request.args.get('q')
    if not search_query:
        return redirect(url_for('index'))

    cur = mysql.connection.cursor()

    # The vulnerability is here: using an f-string to directly inject user input.
    # An attacker could provide input like: ' OR 1=1; --
    # This would change the query to SELECT ... WHERE title LIKE '%' OR 1=1; -- %'
    # which would return all posts from the database.
    query = f"SELECT id, title, content, author, created_at FROM posts WHERE title LIKE '%{search_query}%'"
    
   # app.logger.info(f"Executing VULNERABLE query: {query}")
    cur.execute(query) # The user input is executed as part of the command
    
    posts = cur.fetchall()
    cur.close()
    
    return render_template('search_results.html', posts=posts, query=search_query)

# --- TIME-BASED VULNERABLE FUNCTION ---
@app.route('/search_time_based')
def search_time_based():
    search_query = request.args.get('q')
    if not search_query:
        search_query = "default" # Ensure query is never empty

    cur = mysql.connection.cursor()

    # VULNERABILITY: The input is directly embedded in the query.
    query = f"SELECT id, title FROM posts WHERE author = '{search_query}'"
    
    app.logger.info(f"Executing TIME-BASED VULNERABLE query: {query}")
    
    cur.execute(query)
    posts = cur.fetchall()
    cur.close()
    
    # This page will always look the same, forcing the attacker to use time.
    return "Search complete."

# --- BOOLEAN-BASED VULNERABLE FUNCTION ---
@app.route('/search_boolean_based')
def search_boolean_based():
    search_query = request.args.get('q')
    if not search_query:
        search_query = "default"

    cur = mysql.connection.cursor()

    # VULNERABILITY: The input is directly embedded in the query.
    query = f"SELECT id, title FROM posts WHERE title = '{search_query}'"
    
    app.logger.info(f"Executing BOOLEAN-BASED VULNERABLE query: {query}")
    
    cur.execute(query)
    posts = cur.fetchall()
    cur.close()
    
    # The page content changes based on the result
    if posts:
        return "Results found!"
    else:
        return "No results."
        
@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Debug mode provides verbose errors in the browser
    app.run(debug=True)
