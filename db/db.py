import mysql.connector
from dotenv import load_dotenv
import os

class Database:
    def __init__(self):
        load_dotenv()
        self.db_host = os.getenv("DB_HOST")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_name = os.getenv("DB_NAME")

        self.db_config = {
            "host": self.db_host,
            "user": self.db_user,
            "password": self.db_password,
            "database": self.db_name,
        }

        self.create_tables()

    def get_connection(self):
        return mysql.connector.connect(**self.db_config)

    def create_tables(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        equipo_table_query = """
        CREATE TABLE IF NOT EXISTS equipo (
            id_equipo INT PRIMARY KEY AUTO_INCREMENT,
            nombre_equipo VARCHAR(50) NOT NULL
        )
        """

        personas_table_query = """
        CREATE TABLE IF NOT EXISTS personas (
            id_persona INT PRIMARY KEY AUTO_INCREMENT,
            nombre_persona VARCHAR(50) NOT NULL,
            correo VARCHAR(100) NOT NULL,
            contraseña VARCHAR(150) NOT NULL
        )
        """
        
        webHookEvents = """ 
       CREATE TABLE webhook_event (
    id INT PRIMARY KEY AUTO_INCREMENT,
    eventos SET('CREATE_TEAM', 'ADD_MEMBER_TEAM', 'DELETE_MEMBER_TEAM', 'ADD_TASK_TEAM', 'DELETE_TASK_TEAM', 'UPDATE_TASK_TEAM', 'GET_TEAMS', 'GET_TEAM', 'GET_MEMBERS_TEAM', 'GET_TASKS_TEAM'),
    url VARCHAR(255)
);

);
        """

        tareas_table_query = """
        CREATE TABLE IF NOT EXISTS tareas (
            id_tarea INT PRIMARY KEY AUTO_INCREMENT,
            nombre_tarea VARCHAR(50) NOT NULL,
            descripcion VARCHAR(255) NOT NULL,
            estatus ENUM('completado', 'pendiente') NOT NULL
        )
        """

        equipo_personas_table_query = """
        CREATE TABLE IF NOT EXISTS equipo_personas (
            id_equipo INT,
            id_persona INT,
            PRIMARY KEY (id_equipo, id_persona),
            FOREIGN KEY (id_equipo) REFERENCES equipo(id_equipo),
            FOREIGN KEY (id_persona) REFERENCES personas(id_persona)
        )
        """

        equipo_tareas_table_query = """
        CREATE TABLE IF NOT EXISTS equipo_tareas (
            id_equipo INT,
            id_tarea INT,
            PRIMARY KEY (id_equipo, id_tarea),
            FOREIGN KEY (id_equipo) REFERENCES equipo(id_equipo),
            FOREIGN KEY (id_tarea) REFERENCES tareas(id_tarea)
        )
        """

        cursor.execute(equipo_table_query)
        cursor.execute(personas_table_query)
        cursor.execute(tareas_table_query)
        cursor.execute(equipo_personas_table_query)
        cursor.execute(equipo_tareas_table_query)

        connection.commit()
        cursor.close()
        connection.close()
