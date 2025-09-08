# DNA Sequence Management System with AES-256 Encryption

A secure web application for managing DNA sequence data using Flask and AES-256 encryption. This system provides role-based access control and encrypted storage of sensitive DNA sequence information.

## Features

- **Secure Authentication**
  - Role-based access control (Researcher and User roles)
  - Session management
  - Protected routes

- **Data Security**
  - AES-256 encryption for DNA sequences
  - GCM mode for authenticated encryption
  - Secure key management
  - Query parameterization for SQL injection prevention

- **User Interface**
  - Clean and responsive Bootstrap-based UI
  - Separate interfaces for data input and viewing
  - Flash messages for user feedback

## Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Encryption**: AES-256-GCM using cryptography library
- **Frontend**: HTML, Bootstrap 4
- **Security Features**: Session management, Password protection

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install required dependencies:
```bash
pip install flask mysql-connector-python cryptography
```

3. Setup the MySQL database:
```sql
CREATE DATABASE dna_database;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(50)
);

CREATE TABLE dna_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    dna_sequence TEXT
);
```

4. Generate encryption key:
```bash
python key.py
```

5. Configure database connection in app.py:
```python
host='localhost'
user='your_username'
password='your_password'
database='dna_database'
```

## Usage

1. Run the application:
```bash
python app.py
```

2. Access the application at `http://localhost:5000`

3. Log in with appropriate credentials:
   - Researchers can input new DNA sequences
   - Users can view encrypted DNA sequences

## Security Features

- **Encryption**: Uses AES-256-GCM for DNA sequence encryption
- **Key Management**: Secure key storage in separate file
- **Authentication**: Role-based access control
- **Database Security**: Parameterized queries to prevent SQL injection
- **Session Management**: Secure session handling with Flask

## Project Structure

```
├── app.py              # Main application file
├── key.py             # Key generation script
├── secret.key         # Encryption key storage
├── templates/         # HTML templates
│   ├── login.html    # Login page
│   ├── input_data.html  # Data input interface
│   └── view_data.html   # Data viewing interface
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).
