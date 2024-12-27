from db import db
from app import app
from models import User, Message

# Crear un nuevo usuario
nuevo_usuario = User(
    email="humber@katsbarnea.com",
    pelicula_favorita="Interstelar",
    genero_favorito="Ciencia Ficción"
)

with app.app_context():
    db.create_all()

    # Añadir el nuevo usuario a la sesión
    db.session.add(nuevo_usuario)
    db.session.commit()  # Confirmar los cambios
    db.session.refresh(nuevo_usuario)  # Refrescar la instancia para obtener los datos actualizados

    print(f"Usuario creado: {nuevo_usuario.email}, Película Favorita: {nuevo_usuario.pelicula_favorita}, Género Favorito: {nuevo_usuario.genero_favorito}")

    # Cerrar la sesión
    # db.close()
