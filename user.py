class User(db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        username = db.Column(db.String(80), nullable=False)
        email = db.Column(db.String(120), nullable=False)