from flask import Flask, request, redirect, render_template, session, flash
from models import Blog, User
from app import db, app


@app.route('/home')

def index():
    posts = Blog.query.all()
    title = Blog.title
    body = Blog.body
    id = Blog.id

    return render_template('home.html', posts=posts, title=title, body=body, id=id)


@app.route('/new_post', methods=['POST', 'GET'])
def new_post():
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']

        if title == '':
            flash("Must have a blog title", 'error')
        if body == '':
            flash("Must have content in blog", "error")
        elif title != '' and body != '':
            new_blog = Blog(title, body)
            db.session.add(new_blog)
            db.session.commit()
            blog_id = str(new_blog.id)

            return redirect("/blog?id=" + blog_id)
    return render_template('/new_post.html')

@app.route('/blog', methods=['GET'])
def blog_id():
    blog_id = request.args.get('id')
    post = Blog.query.get(blog_id)
      
    
    return render_template("blog.html", post=post)


app.secret_key = "aosdijf"
if __name__ == "__main__":
    app.run()

