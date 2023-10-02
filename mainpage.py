from flask import Flask, render_template, url_for, redirect, request

mainpage = Flask(__name__)

@mainpage.route('/')
def home():
    return render_template('home.html')


@mainpage.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@mainpage.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')


@mainpage.route('/logout', methods=['GET', 'POST'])
def logout():
    return redirect(url_for('login'))


@ mainpage.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@mainpage.route('/post_testing', methods=['GET','POST'])
def posting():
    return render_template('post_testing.html')

if __name__ == "__main__":
    mainpage.run(debug=True)