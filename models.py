from flask_sqlalchemy import SQLAlchemy

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

    @property
    def full_name(self):
        """Full name of user"""

        return f"{self.first_name} {self.last_name}"
    
    
