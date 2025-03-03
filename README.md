# Entrepreneurship

## Setup Instructions

To set up a Python virtual environment and install the required packages from `requirements.txt`, follow these steps:

0. **Open the project in WSL**:

   - Open your WSL terminal.
   - Navigate to the project directory:
     ```sh
     cd /mnt/c/Users/DAHoe/OneDrive\ -\ IE\ University/Programming/Entrepreneurship
     ```
   - Be sure to activate LF endings in WSL:
     ```sh
     git config --global core.autocrlf input
     ```

1. **Create a virtual environment**:

   ```sh
   python -m venv .venv
   ```

2. **Activate the virtual environment**:

   - On Windows:
     ```sh
     source .\venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```sh
     source venv/bin/activate
     ```

3. **Install the required packages**:

   ```sh
   pip install -r requirements.txt
   ```

4. **Create MySQL database**:

   - Create a MySQL database named `entrepreneurship`:
     ```sql
     CREATE DATABASE entrepreneurship;
     ```
   - Create a MySQL user and grant privileges:
     ```sql
     CREATE USER 'your_mysql_username'@'localhost' IDENTIFIED BY 'your_mysql_password';
     GRANT ALL PRIVILEGES ON entrepreneurship.* TO 'your_mysql_username'@'localhost';
     FLUSH PRIVILEGES;
     ```

5. **Create .env file**:

   - Create a `.env` file in the root directory of the project.
   - Add the following environment variables to the `.env` file:
     ```env
     SECRET_KEY=your_secret_key
     DEBUG=True
     DB_NAME=entrepreneurship
     DB_USER=your_mysql_username
     DB_PASSWORD=your_mysql_password
     DB_HOST=localhost
     DB_PORT=3306
     ```

6. **Run migrations**:
   ```sh
   python manage.py migrate
   ```
