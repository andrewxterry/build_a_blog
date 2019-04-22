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
    posts = Blog.query.all()
    title = Blog.title
    body = Blog.body

    return render_template('home.html', posts=posts, title=title, body=body)


@app.route('/new_post', methods=['POST', 'GET'])
def new_post():
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']


        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()
    return redirect('/home')



if __name__ == "__main__":
    app.run()

