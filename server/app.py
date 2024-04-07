#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def get_bakeries():
    # Query all bakeries from the database
    bakeries = Bakery.query.all()
    
    # Serialize the list of bakeries into JSON format
    all_bakeries = []
    for bakery in bakeries:
        bakery_dict= {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at.strftime("%Y-%m-%d %H:%M:%S") if bakery.created_at else None,
            'updated_at': bakery.updated_at.strftime("%Y-%m-%d %H:%M:%S") if bakery.updated_at else None,
            'baked_goods': [baked_good.to_dict() for baked_good in bakery.baked_goods]
        }
        all_bakeries.append(bakery_dict)
    
    # Return the JSON response
    return jsonify(all_bakeries)

@app.route('/bakeries/<int:id>')
def get_bakery_by_id(id):
    # Look up the bakery by its ID
    bakery = Bakery.query.get(id)
    if bakery:
        # Construct JSON response with bakery details and nested baked goods
        bakery_data = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Format created_at as string
            'baked_goods': [baked_good.name for baked_good in bakery.baked_goods]  
        }
        return jsonify(bakery_data), 200, {'Content-Type': 'application/json'}  
    else:
        return jsonify({'error': 'Bakery not found'}), 404, {'Content-Type': 'application/json'}  

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    # Serialize the list of baked goods into JSON format
    baked_goods_list = [{
        'id': bg.id,
        'name': bg.name,
        'price': bg.price,
        'created_at': bg.created_at.isoformat(),
        'updated_at': bg.updated_at.isoformat() if bg.updated_at else None,
        'bakery_id': bg.bakery_id
    } for bg in baked_goods]

    return jsonify(baked_goods_list)

@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    # Query the most expensive baked good
    most_expensive_baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive_baked_good:
        # Construct JSON response with details of the most expensive baked good
        baked_good_data = {
            'id': most_expensive_baked_good.id,
            'name': most_expensive_baked_good.name,
            'price': most_expensive_baked_good.price,
            'created_at': most_expensive_baked_good.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Format created_at as string
        }
        return jsonify(baked_good_data), 200
    else:
        return jsonify({'error': 'No baked goods found'}), 404
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)
