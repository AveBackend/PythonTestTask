from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apartment_no = db.Column(db.String(50), nullable=False)
    pet_name = db.Column(db.String(50), nullable=False)
    pet_breed = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    apartment_no = data['apartment_no']
    pet_name = data['pet_name']
    pet_breed = data['pet_breed']
    start_time = datetime.fromisoformat(data['start_time']).astimezone(pytz.UTC)

    # Валидация времени
    if start_time < datetime.now(pytz.UTC).replace(hour=7, minute=0, second=0) or start_time > datetime.now(
            pytz.UTC).replace(hour=23, minute=0, second=0):
        return jsonify({"error": "Время должно быть между 07:00 и 23:00"}), 400

    if start_time.minute not in [0, 30]:
        return jsonify({"error": "Время должно начинаться на начало часа или на половину"}), 400

    end_time = start_time + timedelta(minutes=30)

    existing_orders = Order.query.filter(
        Order.start_time < end_time,
        Order.end_time > start_time
    ).all()

    if existing_orders:
        return jsonify({"error": "Время уже занято"}), 409

    new_order = Order(
        apartment_no=apartment_no,
        pet_name=pet_name,
        pet_breed=pet_breed,
        start_time=start_time,
        end_time=end_time
    )

    db.session.add(new_order)
    db.session.commit()

    return jsonify({
        'id': new_order.id,
        'apartment_no': new_order.apartment_no,
        'pet_name': new_order.pet_name,
        'pet_breed': new_order.pet_breed,
        'start_time': new_order.start_time.isoformat(),
        'end_time': new_order.end_time.isoformat()
    }), 201

@app.route('/api/orders', methods=['GET'])
def get_orders():
    date_str = request.args.get('date')
    date = datetime.fromisoformat(date_str)

    filtered_orders = Order.query.filter(Order.start_time.startswith(date.isoformat())).all()

    orders_list = [{
        'id': order.id,
        'apartment_no': order.apartment_no,
        'pet_name': order.pet_name,
        'pet_breed': order.pet_breed,
        'start_time': order.start_time.isoformat(),
        'end_time': order.end_time.isoformat()
    } for order in filtered_orders]

    return jsonify(orders_list), 200

if __name__ == '__main__':
    app.run(debug=True)