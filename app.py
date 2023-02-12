from crypt import methods
from pydoc import render_doc
from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'bloglydb_2023'
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


toolbar = DebugToolbarExtension(app)


connect_db(app)
db.create_all()



@app.route('/home')
def root():
    """Show recent list of posts, most-recent first."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404

"""User routes"""

@app.route('/')
def home():
    
    return redirect('/home')

@app.route('/users')
def all_users():

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('home.html', users=users)

@app.route('/users/new', methods=['GET'])
def add_new_user():

    return render_template('new-user.html')

@app.route("/users/new", methods=['POST'])
def new_users():

    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None)
    
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:users_id>')
def show_users(users_id):

    user = User.query.get_or_404(users_id)
    return render_template('users/show.html', user=user)

@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):


    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
  

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")




"""User posts routes"""

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):

    user = User.query.get_or_404(user_id)
    tags= Tag.query.all()
    post = Post.query.all()
    return render_template('posts/new.html', user=user, tags=tags, post=post)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user,
                    tags=tags,
                    )

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

    


@app.route('/posts/<int:post_id>')
def posts_show(post_id):

    post = Post.query.get_or_404(post_id)
    tags= Tag.query.all()
    return render_template('posts/show.html', post=post,tags=tags)

@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):

    post = Post.query.get_or_404(post_id)
    tags= Tag.query.all()
    return render_template('posts/edit.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")


"""Part 3 - Post tag routes"""

@app.route('/tags/list', methods=["GET"])
def tag_list():

    tags = Tag.query.all()
    return render_template('/tags/taglist.html', tags=tags)

@app.route('/tags/create', methods=["GET"])
def create_tag():

    posts = Post.query.all()
    return render_template('/tags/create.html', posts=posts)

@app.route('/tags/new', methods=["POST"])
def post_tags():

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags/list")

@app.route('/tags/<int:tag_id>')
def show_tags(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tags(tag_id):
    

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    

    return redirect("/tags/list")














    

