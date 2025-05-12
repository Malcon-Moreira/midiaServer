import os.path

from flask import Flask, jsonify, send_from_directory, request, render_template, url_for, make_response, redirect
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
)
from requirements import CHAVE_SECRETA
from views import check_user_exists, add_user, check_login

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = CHAVE_SECRETA
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

jwt = JWTManager(app)


@app.route('/sign_up', methods=['POST'])
def sign_up():
    username = request.json.get('username')
    password = request.json.get('password')

    if check_user_exists(username) == True:
        return jsonify({"Mensagem": "Usuário já cadastrado."})

    else:
        add_user(username, password)
        return jsonify({"Mensagem": "Usuario cadastrado com sucesso!"})


@app.route('/home', methods=['GET'])
@jwt_required()
def home():
    usuario = get_jwt_identity()
    pasta_videos = os.path.join(os.getcwd(), 'D:/filmes')
    lista_videos = [f for f in os.listdir(pasta_videos) if f.endswith('.mkv')]
    return render_template('home.html', usuario=usuario, videos=lista_videos)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_login(username, password) == True:
            access_token = create_access_token(identity=username)
            resp = make_response(redirect(url_for('home')))
            set_access_cookies(resp, access_token)
            return resp
        else:
            return jsonify({"Mensagem": "Usuário ou senha incorretos"})
    return render_template('login.html')


@app.route('/logout', methods=['POST'])
def logout():
    resp = make_response(redirect(url_for('login')))
    unset_jwt_cookies(resp)
    return resp


@app.route('/videos/<nome_arquivo>')
@jwt_required()
def servir_video(nome_arquivo):
    caminho = os.path.join(os.getcwd(), 'D:/filmes')
    return send_from_directory(caminho, nome_arquivo)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
