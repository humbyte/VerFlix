from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from openai import OpenAI
from dotenv import load_dotenv
from db import db, db_config
from models import User, Message

load_dotenv()

client = OpenAI()
app = Flask(__name__)
bootstrap = Bootstrap5(app)
db_config(app)


@app.route('/')
def index():
    return render_template('landing.html')



@app.route('/chat/<int:user_id>', methods=['GET', 'POST'])
def chat(user_id):
    # user = db.session.query(User).first()
    user = db.session.query(User).filter(User.id == user_id).first()
    print(user.pelicula_favorita)
    print(user.genero_favorito)
    if request.method == 'GET':
        return render_template('chat.html', messages=user.messages)

    intent = request.form.get('intent')

    intents = {
        'Quiero tener suerte': 'Recomiéndame una película',
        'Terror': 'Recomiéndame una película de terror',
        'Acción': 'Recomiéndame una película de acción',
        'Comedia': 'Recomiéndame una película de comedia',
        'Enviar': request.form.get('message')
    }

    if intent in intents:
        user_message = intents[intent]

        # Guardar nuevo mensaje en la BD
        db.session.add(Message(content=user_message, author="user", user=user))
        db.session.commit()

        messages_for_llm = [{
            "role": "system",
            #Prompt personalizado con las preferencias
            "content": f"Eres un chatbot que recomienda películas, te llamas 'Flexie'. Tu rol es responder recomendaciones en base a {user.pelicula_favorita} y {user.genero_favorito} de manera breve y concisa. No repitas recomendaciones.",
        }]

        for message in user.messages:
            messages_for_llm.append({
                "role": message.author,
                "content": message.content,
            })

        chat_completion = client.chat.completions.create(
            messages=messages_for_llm,
            model="gpt-4o",
            temperature=1
        )

        model_recommendation = chat_completion.choices[0].message.content
        db.session.add(Message(content=model_recommendation, author="assistant", user=user))
        db.session.commit()

        return render_template('chat.html', messages=user.messages)


@app.route('/user/<username>')
def user(username):
    favorite_movies = [
        'The Shawshank Redemption',
        'The Godfather',
        'The Dark Knight',
    ]
    return render_template('user.html', username=username, favorite_movies=favorite_movies)


@app.post('/recommend')
def recommend():
    user = db.session.query(User).first()
    data = request.get_json()
    user_message = data['message']
    new_message = Message(content=user_message, author="user", user=user)
    db.session.add(new_message)
    db.session.commit()

    messages_for_llm = [{
        "role": "system",
        "content": "Eres un chatbot que recomienda películas, te llamas 'Flexie'. Tu rol es responder recomendaciones de manera breve y concisa. No repitas recomendaciones.",
    }]

    for message in user.messages:
        messages_for_llm.append({
            "role": message.author,
            "content": message.content,
        })

    chat_completion = client.chat.completions.create(
        messages=messages_for_llm,
        model="gpt-4o",
    )

    message = chat_completion.choices[0].message.content

    return {
        'recommendation': message,
        'tokens': chat_completion.usage.total_tokens,
    }

# Perfil Preferencias
@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def update_profile(user_id):
    # db = SessionLocal()
    user = db.session.query(User).filter(User.id == user_id).first()

    if request.method == 'POST':
        user.pelicula_favorita = request.form['pelicula_favorita']
        user.genero_favorito = request.form['genero_favorito']
        db.session.commit()
        db.session.refresh(user)
        return redirect(url_for('update_profile', user_id=user.id))

    return render_template('profile.html', user=user)
