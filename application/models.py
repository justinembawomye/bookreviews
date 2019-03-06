from application import db

class User(db.Model):

    """This class represents the users table."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)



    def __init__(self, username, email, password):
        """initialize with name."""
        self.username = username
        self.email = email
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"User: {self.username}"




class Books(db.Model):

    """This class represents the books table."""

    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(15), unique=True, nullable=False)
    title = db.Column(db.String(60), unique=True, nullable=False)
    author = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Books: {self.title}"
