"""Flask app for Cupcakes"""
from flask import Flask, request, render_template,  redirect, flash, jsonify
from models import db, connect_db, DEFAULT_PIC, Cupcake

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.app_context().push()
connect_db(app)


@app.route('/')
def index():
    '''Renders the cupcakes and new cupcake form'''
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)


@app.route('/api/cupcakes')
def list_cupcakes():
    '''Returns JSON for all cupcakes in the DB'''
    
    all_cakes = Cupcake.query.all()
    all_cakes_JSON = [cake.serialize() for cake in all_cakes]
    response_JSON = jsonify(cupcakes=all_cakes_JSON)
    
    return (response_JSON)


@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    '''Returns JSON for a specific cupcake'''
    
    cupcake = Cupcake.query.get_or_404(id)
    cupcake_JSON = cupcake.serialize()
    response_JSON = jsonify(cupcake=cupcake_JSON)
    
    return (response_JSON)


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    '''Creates a new cupcake and return JSON'''
    
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image'] or DEFAULT_PIC
    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    
    db.session.add(new_cupcake) 
    db.session.commit()
    
    new_cupcake_JSON = new_cupcake.serialize()
    response_JSON = jsonify(cupcake=new_cupcake_JSON)
    
    return (response_JSON, 201)


@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    '''Updates a specific cupcake and returns JSON'''
    
    cupcake = Cupcake.query.get_or_404(id)
    
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    
    db.session.commit()
    
    cupcake_JSON = cupcake.serialize()
    response_JSON = jsonify(cupcake=cupcake_JSON)
    
    return (response_JSON)


@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_todo(id):
    '''Deletes a specific cupcake and returns deletion confirmation'''
    
    cupcake = Cupcake.query.get_or_404(id)
    
    db.session.delete(cupcake)
    db.session.commit()
    
    response_JSON = jsonify(message='Deleted')
    
    return (response_JSON)