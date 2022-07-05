<h1 align=center>Proyecto final</h1>
<h2 align=center>Bases de datos no relacionales</h2>

## Iniciar el sistema

1) Ejecutar el comando "pip install -r requirements.txt" para instalar todas las bibliotecas utilizadas en el proyecto.
2) Instalar la biblioteca gunicorn. Link a la documentación de la biblioteca: https://docs.gunicorn.org/en/stable/install.html
3) Dentro de "ciudadania/ciudadania/setttings.py" configurar la conección a la base de datos Neo4j.
4) Ejecutar el comando "python3 manage.py install_labels" 
5) Luego dentro del directorio "ciudadania/" ejecutar el comando "gunicorn ciudadania.wsgi".
6) (OPCIONAL) - Importar datos al sistema, puede ejecutar el comando "python3 manage.py import_json ../families.json"
7) La aplicación debería estar disponible en el puerto 8000.

## Realizar pruebas de carga

1) Iniciar el sistema.
2) Ejecutar el comando "pip install locust", esta es la biblioteca utilizada para realizar las pruebas de carga.
3) Pararse sobre el directorio "pruebas/" y ejecutar el comando "locust -f locustfile.py".
4) Ir a la url "localhost:8089", seleccionar la cantidad de usuarios con los que se quiere realizar la prueba e inicie la ejecución de las pruebas.




