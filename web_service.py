from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import random
import string
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fallback-secret-key-for-development')

users_db = {
    os.environ.get('WEB_SERVICE_LOGIN', 'test_user'): os.environ.get('WEB_SERVICE_PASSWORD', 'test_password')
}

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users_db and users_db[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return "Неверные логин или пароль", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/generate_code')
def generate_code():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    new_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    return jsonify({'code': new_code})

if __name__ == '__main__':
    app.run(debug=True)