from db.db import Database

db = Database()
def getWebhookUrlsByEvent(event):
    try:
        connection = db.get_connection()
        cursor = connection.cursor()

        # Construye la consulta SQL para seleccionar las URLs con el evento específico
        query = f"SELECT url FROM webhook_event WHERE FIND_IN_SET(%s, eventos) > 0"
        cursor.execute(query, (event,))
        
        # Obtén los resultados y devuelve una lista de URLs
        results = cursor.fetchall()
        print(results)
        return [result[0] for result in results]

    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
            connection.close()

def createWebhook(webHook):
    try:
        connection = db.get_connection()
        cursor = connection.cursor()

            # Construye la consulta SQL para insertar el webhook en la tabla
        query = "INSERT INTO webhook_event (url, eventos) VALUES (%s, %s)"
        cursor.execute(query, (webHook['url'], ",".join(webHook['eventos'])))

            # Confirma la transacción
        connection.commit()

        return "webhook creado correctamente"  # Indica que la inserción fue exitosa

    except Exception as e:
        print(f"Error al insertar el webhook: {e}")
        return "error al insertar webhook"  # Indica que hubo un error en la inserción

    finally:
        if cursor:
            cursor.close()
            connection.close()