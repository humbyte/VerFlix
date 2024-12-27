import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Obtener la URL de la base de datos y el token de variables de entorno
database_url = os.environ.get("TURSO_DATABASE_URL")
auth_token = os.environ.get("TURSO_AUTH_TOKEN")

# Verificar que las variables de entorno estén configuradas
if not database_url or not auth_token:
     raise ValueError("Las variables de entorno TURSO_DATABASE_URL y TURSO_AUTH_TOKEN no están definidas.")

# Construir la URL de conexión con el token
connection_string = f"{database_url}?authToken={auth_token}"

# Configurar la conexión a la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Opcional

db = SQLAlchemy(app)

class Movie(db.Model): # Ejemplo de como crear un modelo
      id = db.Column(db.Integer, primary_key=True)
      title = db.Column(db.String(100), nullable=False)
      director = db.Column(db.String(100))
      year = db.Column(db.Integer)


if __name__ == "__main__":
     with app.app_context():
         db.create_all() # Se crea la base de datos con los modelos
         # Ejemplo de como agregar un dato.
         new_movie = Movie(title="Interestelar", director="Christopher Nolan", year=2014)
         db.session.add(new_movie)
         db.session.commit()
     print("Base de datos inicializada y un dato agregado.")