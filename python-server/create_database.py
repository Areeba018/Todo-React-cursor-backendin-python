import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv('config.env')

def create_database():
    """Create the todoapp database and tables"""
    connection = None
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '1234'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS todoapp")
            print("Database 'todoapp' created successfully!")
            
            # Use the database
            cursor.execute("USE todoapp")
            
            # Create users table
            create_users_table = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(create_users_table)
            print("Table 'users' created successfully!")

            # Create tasks table
            create_tasks_table = """
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                text TEXT NOT NULL,
                description TEXT,
                completed TINYINT(1) DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                tag VARCHAR(100),
                checklist TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
            
            cursor.execute(create_tasks_table)
            print("Table 'tasks' created successfully!")
            
            print("\nDatabase setup completed successfully!")
            print("Database: todoapp")
            print("Tables: users, tasks")
            
    except Error as e:
        print(f"Error: {e}")
        print("\nTo create the database manually, follow these steps:")
        print("1. Open MySQL command line: mysql -u root -p")
        print("2. Enter your MySQL password when prompted")
        print("3. Run these SQL commands:")
        print("   CREATE DATABASE IF NOT EXISTS todoapp;")
        print("   USE todoapp;")
        print("   CREATE TABLE IF NOT EXISTS users (")
        print("       id INT AUTO_INCREMENT PRIMARY KEY,")
        print("       username VARCHAR(50) UNIQUE NOT NULL,")
        print("       email VARCHAR(100) UNIQUE NOT NULL,")
        print("       password_hash VARCHAR(255) NOT NULL,")
        print("       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        print("   );")
        print("   CREATE TABLE IF NOT EXISTS tasks (")
        print("       id INT AUTO_INCREMENT PRIMARY KEY,")
        print("       user_id INT NOT NULL,")
        print("       text TEXT NOT NULL,")
        print("       description TEXT,")
        print("       completed TINYINT(1) DEFAULT 0,")
        print("       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,")
        print("       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,")
        print("       tag VARCHAR(100),")
        print("       checklist TEXT,")
        print("       FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE")
        print("   );")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    create_database() 