from flask import Flask, request, redirect, render_template, session, flash
from models import Blog, User
from app import db, app


@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'name' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user = User.query.filter_by(name=name).first()
        if user and user.password == password:
            session['name'] = name
            flash("Logged in", "login")
            return redirect('/home')
        else:
            flash("User password incorrect, or user does not exist", 'error')
            

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        verify = request.form['verify']

        if password != verify: 
            flash("Passwords must match", 'error')
            return redirect('/register')
        
        existing_user = User.query.filter_by(name=name).first()
        if not existing_user:
            new_user = User(name, password)
            db.session.add(new_user)
            db.session.commit()
            session['name'] = name
            return redirect("/home")

        else: 
            flash("This user name already exists", "error")
    
    return render_template('register.html')




@app.route('/home')

def index():
    posts = Blog.query.all()
    title = Blog.title
    body = Blog.body
    id = Blog.id
    user = User.query.all()

    return render_template('home.html', posts=posts, title=title, body=body, id=id, user=user)


@app.route('/new_post', methods=['POST', 'GET'])
def new_post():
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(name=session['name']).first()

        if title == '':
            flash("Must have a blog title", 'error')
        if body == '':
            flash("Must have content in blog", "error")
        elif title != '' and body != '':
            new_blog = Blog(title, body, owner)
            db.session.add(new_blog)
            db.session.commit()
            blog_id = str(new_blog.id)

            return redirect("/blog?id=" + blog_id)
    return render_template('/new_post.html')

@app.route('/blog', methods=['GET'])
def blog_id():
    blog_id = request.args.get('id')
    post = Blog.query.get(blog_id)
    owner = User.query.filter_by(name=session['name']).first()
      
    
    return render_template("blog.html", post=post, owner=owner)
    

@app.route('/logout')
def logout():
    del session['name']
    return redirect ('/')



app.secret_key = "aosdijf"
if __name__ == "__main__":
    app.run()

