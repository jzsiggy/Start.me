from flask import Flask, flash, render_template, url_for, request, session, redirect
# from flask_login import LoginManager, UserMixin
from flask_pymongo import PyMongo
import bcrypt
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = 'startme'
app.config["MONGO_URI"] = "mongodb://localhost:27017/users"
mongo = PyMongo(app)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session:
        return redirect(url_for('index'))
    
    else:
        if request.method =='POST':
            users = mongo.db.users
            existing_user = users.find_one({'name' : request.form['username']})

            if existing_user:
                if bcrypt.hashpw(request.form['pass'].encode('utf-8'), existing_user['password']) == existing_user['password']:
                    session['username'] = request.form['username']
                    return redirect(url_for('index'))
                flash('invalid username/passwd combination')
                return redirect(url_for('login'))
            flash('invalid username')
            return redirect(url_for('login'))

        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if session:
        return redirect(url_for('index'))
    else:    
        if request.method == 'POST':
            users = mongo.db.users
            existing_user = users.find_one({'name' : request.form['username']})
            
            if existing_user is None:
                email=request.form['email']
                hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
                users.insert({'name' : request.form['username'], 'password' : hashpass, 'email' : email})
                session['username'] = request.form['username']
                session['email'] = request.form['email']
                return redirect(url_for('index'))
            
            flash('that username already exists')
            return redirect(url_for('signup'))

        return render_template('signup.html')

@app.route('/signout')
def signout():
    if session:
        session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)