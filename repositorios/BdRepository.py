from db.db import Database

db = Database()

class BaseRepository:
    def select_all(self, table_name):
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            raise ValueError("Error al ejecutar la consulta")
        finally:
            if cursor:
                cursor.close()
                connection.close()

    def selectByCondition(self, table_name, condition, selected_columns=None):
        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            # Convierte la lista de columnas a una cadena separada por comas
            columns_str = "*" if selected_columns is None else ", ".join(selected_columns)

            # Construye la consulta SQL con la condición y las columnas seleccionadas
            query = f"SELECT {columns_str} FROM {table_name} WHERE {condition}"

            cursor.execute(query)
            results = cursor.fetchall()

            if not results:
                print(f"No se encontraron resultados para la condición: {condition}")
                return None
        
            return results
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
                connection.close()

    def insertData(self, table_name, data):
        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            # Construye la consulta SQL para insertar datos en la tabla
            columns = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

            # Ejecuta la consulta SQL con los datos proporcionados
            cursor.execute(query, tuple(data.values()))

            # Confirma la transacción
            connection.commit()

            return True  # Indica que la inserción fue exitosa
        except Exception as e:
            print(f"Error al insertar datos: {e}")
            return False  # Indica que hubo un error en la inserción
        finally:
            if cursor:
                cursor.close()
                connection.close()
    
    def deleteData(self, table_name, condition):
        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            # Construye la consulta SQL para eliminar datos de la tabla
            query = f"DELETE FROM {table_name} WHERE {condition}"

            # Ejecuta la consulta SQL con la condición proporcionada
            cursor.execute(query)

            # Confirma la transacción
            connection.commit()

            # Devuelve la cantidad de filas afectadas por la eliminación
            return cursor.rowcount
        except Exception as e:
            print(f"Error al eliminar datos: {e}")
            return -1  # Indica que hubo un error en la eliminación
        finally:
            if cursor:
                cursor.close()
                connection.close()
                
    def insertAndReturn(self, table_name, data):
        try:
            connection = db.get_connection()
            cursor = connection.cursor()

        # Construye la consulta SQL para insertar datos en la tabla
            columns = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

        # Ejecuta la consulta SQL con los datos proporcionados
            cursor.execute(query, tuple(data.values()))

        # Confirma la transacción
            connection.commit()

        # Obtiene la información insertada sin necesidad de especificar columnas para el retorno
            inserted_data_query = f"SELECT * FROM {table_name} ORDER BY {list(data.keys())[0]} DESC LIMIT 1"
            cursor.execute(inserted_data_query)
            inserted_data = cursor.fetchone()

            return inserted_data

        except Exception as e:
            print(f"Error al insertar datos: {e}")
            return False  # Indica que hubo un error en la inserción
        finally:
            if cursor:
                cursor.close()
                connection.close()
    def updateData(self, table_name, data, condition):
        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            # Construye la consulta SQL para actualizar datos en la tabla
            set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"

            # Ejecuta la consulta SQL con los datos proporcionados
            cursor.execute(query, tuple(data.values()))

            # Confirma la transacción
            connection.commit()

            # Devuelve la cantidad de filas afectadas por la actualización
            return cursor.rowcount
        except Exception as e:
            print(f"Error al actualizar datos: {e}")
            return -1  # Indica que hubo un error en la actualización
        finally:
            if cursor:
                cursor.close()
                connection.close()  
                
    def myQuerySelect(self, query):
        connection = db.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            data = cursor.fetchall()
            return data
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
        # Puedes lograr el error si es necesario: logging.error(f"Error: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
                connection.close()
                           
