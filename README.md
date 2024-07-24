# Telegram Bot para Diagnóstico por Imágenes

Este proyecto implementa un bot de Telegram para una empresa de diagnóstico por imágenes, permitiendo a los médicos enviar audios relacionados con estudios de pacientes. 

## Características

- **Menú Inicial:**
  - Ingresar al servicio
  - Registrar un nuevo médico
  - Tutorial de uso

- **Interacción:**
  - Validación de ID del médico con una base de datos SQL.
  - Registro de nuevos médicos con su correo electrónico, nombre y apellido.
  - Envío de audios y cancelación del último audio enviado.
  - Cierre de sesión.

## Requisitos

- Python 3.x
- MySQL
- MySQL Workbench
- pip
- virtualenv

## Instalación

1. Clona el repositorio:

    ```bash
    git clone https://github.com/tu-usuario/diagnostic-imaging-bot.git
    cd diagnostic-imaging-bot
    ```

2. Crea y activa un entorno virtual:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4. Configura la base de datos:

    - Abre MySQL Workbench y crea una nueva base de datos llamada `diagnostic_imaging`.
    - Ejecuta el siguiente script SQL para crear las tablas necesarias:

        ```sql
        USE diagnostic_imaging;

        CREATE TABLE users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            institution VARCHAR(255),
            audio_count INT DEFAULT 0
        );

        CREATE TABLE audios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            audio_id VARCHAR(255) UNIQUE NOT NULL,
            study_number VARCHAR(255),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        ```

5. Configura el archivo `bot/config.py` con tu token de Telegram y la URL de tu base de datos:

    ```python
    TOKEN = 'TU_TELEGRAM_BOT_TOKEN'
    DATABASE_URL = 'mysql+pymysql://usuario:password@localhost:3306/diagnostic_imaging'
    ```

## Uso

1. Inicia el bot:

    ```bash
    python -m bot.main
    ```

2. En Telegram, busca tu bot y envía el comando `/start` para comenzar la interacción.

## Contribución

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request para cualquier mejora o corrección.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.

