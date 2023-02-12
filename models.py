from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):

        db.app = app
        db.init_app(app)

DEFAULT_IMG = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    first_name = db.Column(db.String(50),nullable = False)  
    
    last_name = db.Column(db.String(50),nullable = False)  
    
    image_url = db.Column(db.String, default = DEFAULT_IMG)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Full name of user"""

        return f"{self.first_name} {self.last_name}"

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    title = db.Column(db.String(50),nullable = False)  
    
    content = db.Column(db.String(50),nullable = False)  
    
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    

    @property 
    def proper_date(self):
        
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
    
class PostTag(db.Model):
    """Tag on a post."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    """Tag that can be added to posts."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        cascade="all,delete",
        backref="tags",
    )
    
