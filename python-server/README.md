# Todo App - Python Backend

This is a Python Flask backend for a Todo application with MySQL database.

## Prerequisites

1. **MySQL Server** - Make sure MySQL is installed and running on your system
2. **Python 3.7+** - Ensure Python is installed

## Database Setup

### Option 1: Using Python Script (Recommended)

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Update the database configuration in `config.env`:
   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_PORT=3306
   DB_NAME=todoapp
   ```

3. Run the database creation script:
   ```bash
   python create_database.py
   ```

### Option 2: Manual MySQL Commands

If you have MySQL command line client installed, you can run these commands:

```sql
-- Connect to MySQL
mysql -u root -p

-- Create the database
CREATE DATABASE IF NOT EXISTS todoapp;

-- Use the database
USE todoapp;

-- Create todos table
CREATE TABLE IF NOT EXISTS todos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Project Structure

```
python-server/
├── requirements.txt          # Python dependencies
├── create_database.py       # Database setup script
├── config.env              # Database configuration
└── README.md               # This file
```

## Database Schema

### Todos Table
- `id`: Primary key (auto-increment)
- `title`: Todo title (required)
- `description`: Todo description (optional)
- `completed`: Completion status (default: false)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Users Table
- `id`: Primary key (auto-increment)
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Hashed password
- `created_at`: Account creation timestamp

## Next Steps

After setting up the database, you can:
1. Create a Flask application (`app.py`)
2. Implement REST API endpoints for CRUD operations
3. Add authentication and user management
4. Connect with your React frontend 