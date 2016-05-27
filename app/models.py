from app import db

# Users are able to make posts, and see their past posts
class User(db.Model):

    __tablename__ = 'user'

    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    color = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.username)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_anonymous(self):
        return False

    # requires unique username logins
    def get_id(self):
        return self.username


# Posts are 140 or fewer characters text which have timestamps and authors
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    author_username = db.Column(db.String, db.ForeignKey('user.username'))

    def __repr__(self):
        return '<Post %r>' % (self.body)