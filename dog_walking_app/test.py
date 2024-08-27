from app import db, Order, app
with app.app_context():
    orders = Order.query.all()
    for order in orders:
        print(f'ID: {order.id}, Apartment: {order.apartment_no}, Pet: {order.pet_name}, Breed: {order.pet_breed}, Start Time: {order.start_time}, End Time: {order.end_time}')