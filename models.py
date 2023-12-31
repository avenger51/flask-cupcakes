"""Models for Cupcake app."""



from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Cupcake(db.Model):
    """Cupcake Model."""

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    flavor = db.Column(db.Text,
                     nullable=False)
    size = db.Column(db.Text, nullable=True)  
    rating = db.Column(db.Float, nullable=True) 
    image = db.Column(db.Text, nullable=True)
 
    #BELOW IS REQUIRED TO CALL TO jsonify 
    def serialize(self):
        """Returns a dict representation of todo which we can turn into JSON"""
        return {
            'id': self.id,
            'flavor': self.flavor,
            'size': self.size,
            'rating' : self.rating,
            'image' : self.image
        }