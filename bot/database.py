import mysql.connector
from mysql.connector import Error
from config import DATABASE_URL


def init_db():
    try:
        # Conectarse a la base de datos
        connection = mysql.connector.connect(**DATABASE_URL)
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Crear tablas si no existen
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT PRIMARY KEY,
                    username VARCHAR(255),
                    email VARCHAR(255)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    audio_path VARCHAR(255),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')

            print("Base de datos inicializada correctamente.")

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

