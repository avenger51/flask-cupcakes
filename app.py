"""Flask app for Cupcakes"""
from flask import Flask, render_template, flash, redirect, render_template, url_for, jsonify, request
#from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake




app = Flask(__name__)
app.config["SECRET_KEY"] = "pet adoption 1234"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#debug = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()


@app.route("/")
def cupcake_home():
    return render_template('index.html')

#THIS IS WAITING FOR THE AXIOS HERE: cupcake.js/showInitialCupcakes()
@app.route("/api/cupcakes", methods=['GET'])
def cupcake_list():
    """Get All Cupcake Data"""
    
    cupcakes = [cupcakes.serialize() for cupcakes in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)
    
    #without JSON:
    #cupcakes = Cupcake.query.all()
    #return render_template("index.html", cupcakes=cupcakes)

#insomnia fails with unsupported media type//10/12 1:pm
@app.route("/api/cupcakes", methods=['POST'])
def cupcake_create():
    
    data = request.json
    new_cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None  #added or None...
    )
    # won't work? new_cupcake = Cupcake(flavor=request.json["flavor"])
    db.session.add(new_cupcake)
    db.session.commit()
    #return (jsonify(cupcake=new_cupcake.to_dict()), 201)
    return (jsonify(cupcake=new_cupcake.serialize()), 201)
    #return (response_json, 201)
#
#
@app.route("/api/cupcakes/<int:id>")
def cupcake_detail(id):
    #functional
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

#EDIT INDIVIDUAL CUPCAKE:
@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def cupcake_update(id):
    data = request.json

    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())
    #saved for future reference
    #new_cupcake = Cupcake.query.get_or_404(id)
    #new_cupcake.flavor = request.json.get('flavor', new_cupcake.flavor)
    #new_cupcake.size = request.json.get('size', new_cupcake.size)
    #new_cupcake.rating = request.json.get('rating', new_cupcake.rating)
    #new_cupcake.image = request.json.get('image', new_cupcake.image)
    #db.session.commit()
    #return jsonify(new_cupcake=new_cupcake.serialize())

@app.route("/api/cupcakes/<int:id>", methods=['DELETE'])
def cupcake_delete(id):
    #functional
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")
    #return jsonify(cupcake=cupcake.serialize())

    
