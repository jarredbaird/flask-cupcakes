"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "llama_eggs"
app.config['CORS_HEADERS'] = 'Content-Type'

debug = DebugToolbarExtension(app)
connect_db(app)

@app.route('/')
def index_page():
    cc = Cupcake.query.all()
    return render_template('index.html', cc=cc)

@app.route('/api/cupcakes', methods=["GET"])
def get_all_cupcakes():
    cc = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cc)

@app.route('/api/cupcakes/<int:cc_id>')
def get_cupcake(cc_id):
    cc = Cupcake.query.get_or_404(cc_id)
    return jsonify(cupcake=cc.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def add_cupcake():
    cc = Cupcake(flavor=request.json['flavor'],
                 size=request.json['size'],
                 rating=request.json['rating'],
                 image=request.json['image'])
    db.session.add(cc)
    db.session.commit()
    cc_json = jsonify(cupcake=cc.serialize())
    return (cc_json, 201)

@app.route('/api/cupcakes/<int:cc_id>', methods=['PATCH'])
def update_cupcake(cc_id):
    cc = Cupcake.query.get_or_404(cc_id)
    cc.flavor = request.json.get('flavor', cc.flavor)
    cc.image = request.json.get('image', cc.image)
    cc.rating = request.json.get('rating', cc.rating)
    cc.size = request.json.get('size', cc.size)
    db.session.commit()
    return jsonify(cupcake=cc.serialize())

@app.route('/api/cupcakes/<int:cc_id>', methods=["DELETE"])
def delete_cupcake(cc_id):
    cc = Cupcake.query.get_or_404(cc_id)
    db.session.delete(cc)
    db.session.commit()
    return jsonify(message="deleted")
    
