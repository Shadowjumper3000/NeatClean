# Entrepreneurship

## Setup Instructions

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