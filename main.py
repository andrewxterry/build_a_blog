from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build_a_blog:1234@localhost:3306/build_a_blog'
app.config['SQLALCHEMY_ECHO'] = True 
db = SQLAlchemy(app)
app.secret_key = "aosdijf"

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    body = db.Column(db.String(2500))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/home')

def index():
    return render_template('home.html', title="Build a Blog")


@app.route('/new_post')
def new_post():
    if request.method == "GET":
        title = request.form.get('title')
        body = request.form.get('body')

        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()
    return render_template('new_post.html')


if __name__ == "__main__":
    app.run()

