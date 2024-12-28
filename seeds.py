from db import db
from app import app
from models import User, Message

# Crear un nuevo usuario
nuevo_usuario = User(
    email="fran@ibanez.cl",
    pelicula_favorita="Dawn of the Living Dead",
    genero_favorito="Terror"
)

with app.app_context():
    db.create_all()

    # Añadir el nuevo usuario a la sesión
    db.session.add(nuevo_usuario)
    db.session.commit()

    # Crear un nuevo mensaje asociado al usuario
    message = Message(content=f"¡Hola {nuevo_usuario.email}, soy Flixie! 🎬🍿 Tu compañer@ de entretenimiento para encontrar la película perfecta en VerFlix.", author="assistant", user_id=nuevo_usuario.id)
    db.session.add(message)
    db.session.commit()

    print("Usuario y Mensaje creado!")

