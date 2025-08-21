# Python Flask Blog & User Management Web App

This is a simple, professional-looking web application built with Python and the Flask framework. It connects to a MySQL database and features a public blog page with search functionality, a login system, and a protected admin page for managing users.

    SECURITY WARNING: This application has been configured to use MD5 for password hashing. MD5 is a cryptographically broken and insecure algorithm. It should NEVER be used for storing passwords in a real-world application. This configuration is for educational or specific demonstration purposes only.

## Installation and Setup

Follow these steps to get the application running on your local machine.

### Step 1: Clone or Download the Files

Make sure you have all the files in the following structure:

```
/your-project-folder
|-- app.py
|-- setup_db.py
|-- requirements.txt
|-- db.yaml
|-- /templates
    |-- layout.html
    |-- index.html
    |-- login.html
    |-- users.html
    |-- search_results.html
```

### Step 2: Install MySQL Server

If you don't have MySQL installed, follow the instructions for your operating system.

    Ubuntu/Debian: `sudo apt update && sudo apt install mysql-server build-essential pkg-config python3-dev default-libmysqlclient-dev`.
    macOS (using Homebrew): `brew install mysql`

    Windows: Download the installer from the official MySQL website.

After installation, ensure the MySQL service is running with `sudo service mysql status`. After the installation, you can connecto to the database with `sudo mysql`. Once inside the MySQL(`mysql>`) shell you can create your custom user with `CREATE USER 'accesspoint'@'localhost' IDENTIFIED BY 'toor';` give it all privileges `GRANT ALL PRIVILEGES ON *.* TO 'accesspoint'@'localhost' WITH GRANT OPTION;` finally apply the changes `FLUSH PRIVILEGES;`. To exit the shell simply type `exit`.

Optionally, if you also want to enable MySQL's own query log (which would log every single query from all connections), you would need to edit the MySQL configuration file (usually `/etc/mysql/my.cnf` or a file inside `/etc/mysql/mysql.conf.d/`) and add these lines under the `[mysqld]` section:

```
general_log_file = /var/log/mysql/mysql.log
general_log      = 1
```
Then we would need to restart the MySQL database with `sudo service mysql restart`.

### Step 3: Create a Virtual Environment & Install Dependencies

It's highly recommended to use a virtual environment.

Create a virtual environment
`python3 -m venv venv`

Activate it (on macOS/Linux)
`source venv/bin/activate`

Or on Windows:
`.\venv\Scripts\activate`

Install all required Python packages
`pip install -r requirements.txt` or `python -m pip install -r requirements.txt`

### Step 4: Configure the Database Connection

Edit the `db.yaml` file and enter your MySQL database credentials. The script will create the database for you, but it needs your user/password to connect to the MySQL server.

```
mysql_host: 'localhost'
mysql_user: 'your_mysql_user'
mysql_password: 'your_mysql_password'
mysql_db: 'flask_blog_app' # This is the database the script will create
```

### Step 5: Run the Database Setup Script

This script will automatically create the database, tables, and the admin user (blogpage_admin / rockyou).

Run the script from your terminal:

`python setup_db.py`

You should see success messages indicating that the database and tables were created.

### Step 6: Run the Application

Now you can start the Flask web server.

`python app.py`

The application will be available at http://127.0.0.1:5000 in your web browser.
