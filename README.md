# Entrepreneurship

## Setup Instructions

To set up a Python virtual environment and install the required packages from `requirements.txt`, follow these steps:

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

5. **Run migrations**:
    ```sh
    python manage.py migrate
    ```