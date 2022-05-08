from data.db_session import global_init
from routes import jobs_api, news_api, user_api
from flask import Flask, jsonify
from flask import make_response, render_template, redirect
import requests
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.user import RegisterForm, LoginForm
from data.users import User
from data import db_session
from data.news import News


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
apikey = "40d1649f-0493-4b70-98ba-98533de7710b"
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), error)


def get_city(city):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey={apikey}&geocode={city}&format=json"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]

        return toponym_coodrinates


@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    params = {}
    user = requests.get(f'http://127.0.0.1:5000/api/user/{user_id}').json()['user']
    print(user)
    cord = get_city(user['city_from']).split()
    cord = f'{cord[0]},{cord[1]}'
    print(cord)
    map_api_server = f"https://static-maps.yandex.ru/1.x/?ll={cord}&spn=0.116457,0.00619&l=sat"
    params = {
        'name': user['name'],
        'city': user['city_from'],
        'image': map_api_server
    }
    return render_template('user_show.html', **params)


@app.route("/")
@app.route("/index")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter((News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    global_init("db/blogs.db")
    app.register_blueprint(news_api.blueprint)
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(user_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()