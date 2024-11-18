from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

app.secret_key = "keloke"
users = {}


@app.route('/')
def home():
    if 'logged_in' in session:
        username = session['username']
        peliculas = users[username].get('peliculas', [])
        return render_template('home.html', username=username, peliculas = peliculas)
    else:
        error = "No estás logeado. "
        return render_template('home.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['password']

        if username not in users:
            users[username] = {
                "password": password,
                "peliculas": []
            }
            return render_template('register.html', username=username)
        else:
            error = f"El usuario {username} ya ha sido registrado. "
            return render_template('register.html', usuario=username, error=error)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['password']

        if username in users and users[username].get("password") == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = f"El usuario {username} o la contraseña no existe."
            return render_template('login.html', usuario=username, error=error)
    return render_template('login.html')

@app.route('/añadir-peliculas', methods=['GET', 'POST'])
def add_film():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        pelicula = request.form['pelicula']
        sinopsis = request.form['sinopsis']
        puntuacion = request.form['puntuacion']
        username = session['username']
        nueva_pelicula = {
            "pelicula": pelicula,
            "sinopsis": sinopsis,
            "puntuacion": puntuacion
        }

        users[username]['peliculas'].append(nueva_pelicula)

    return render_template('añadir_pelicula.html', username=session['username'])

@app.route('/logout')
def logout():
    username = session.get('username')
    if username in users:
        del users[username]
    session.pop('logged_in', None)
    session.pop('username', None)
    return render_template('logout.html', username=username)

if __name__ == '__main__':
    app.run()


