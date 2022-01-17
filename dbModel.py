import json

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# использовал один раз при заполнении таблиц, возможно код с созданием таблиц надо вынести в отдельный файл
# from func import read_json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite3.db?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    age = db.Column(db.Integer)
    email = db.Column(db.String(50))
    role = db.Column(db.String(30))
    phone = db.Column(db.String(30))


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))


# использовал один раз для создания и заполнения таблиц, , возможно код с созданием таблиц надо вынести в отдельный файл
# db.drop_all()
# db.create_all()
#
# raw_json = read_json("Users.json")
# row_list = []
# for i in raw_json:
#     new_user = User(
#         id=i['id'],
#         first_name=i['first_name'],
#         last_name=i['last_name'],
#         age=i['age'],
#         email=i['email'],
#         role=i['role'],
#         phone=i['phone']
#     )
#     row_list.append(new_user)
#
# raw_json = read_json("Offers.json")
# for i in raw_json:
#     new_offer = Offer(
#         id=i['id'],
#         order_id=i['order_id'],
#         executor_id=i['executor_id']
#     )
#     row_list.append(new_offer)
#
# raw_json = read_json("Orders.json")
# for i in raw_json:
#     new_order = Order(
#         id=i["id"],
#         name=i["name"],
#         description=i["description"],
#         start_date=i["start_date"],
#         end_date=i["end_date"],
#         address=i["address"],
#         price=i["price"],
#         customer_id=i["customer_id"],
#         executor_id=i["executor_id"]
#     )
#     row_list.append(new_order)
#
#
# db.session.add_all(row_list)
# db.session.commit()


@app.route('/users/', methods=['GET', 'POST'])
def page_users():
    if request.method == 'GET':
        users = db.session.query(User).all()
        user_response = []
        for user in users:
            user_response.append(
                {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "age": user.age,
                    "email": user.email,
                    "role": user.role,
                    "phone": user.phone
                })
        return json.dumps(user_response)
    elif request.method == 'POST':
        user_data = json.loads(request.data)
        new_user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            age=user_data['age'],
            email=user_data['email'],
            role=user_data['role'],
            phone=user_data['phone']
        )
        db.session.add(new_user)
        db.session.commit()
        return 'new user created', 201


@app.route('/users/<int:sid>', methods=['GET', 'PUT', 'DELETE'])
def page_users_sid(sid: int):
    if request.method == 'GET':
        user = User.query.get(sid)
        if user is None:
            return "user not found"

        return json.dumps({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "age": user.age,
            "email": user.email,
            "role": user.role,
            "phone": user.phone
        })
    elif request.method == 'DELETE':
        u = User.query.get(sid)
        db.session.delete(u)
        db.session.commit()
        return f'user {sid} deleted', 204
    elif request.method == 'PUT':
        user_data = json.loads(request.data)
        u = User.query.get(sid)
        u.first_name = user_data['first_name']
        u.last_name = user_data['last_name']
        u.age = user_data['age']
        u.email = user_data['email']
        u.role = user_data['role']
        u.phone = user_data['phone']
        db.session.add(u)
        db.session.commit()
        return f'user {sid} updated', 204


@app.route('/orders/', methods=['GET', 'POST'])
def page_orders():
    if request.method == 'GET':
        orders = db.session.query(Order).all()
        order_response = []
        for order in orders:
            order_response.append(
                {
                    "id": order.id,
                    "name": order.name,
                    "description": order.description,
                    "start_date": order.start_date,
                    "end_date": order.end_date,
                    "address": order.address,
                    "price": order.price,
                    "customer_id": order.customer_id,
                    "executor_id": order.executor_id
                })
        return jsonify(order_response)
    if request.method == 'POST':
        user_data = json.loads(request.data)
        new_order = Order(
            name=user_data["name"],
            description=user_data["description"],
            start_date=user_data["start_date"],
            end_date=user_data["end_date"],
            address=user_data["address"],
            price=user_data["price"],
            customer_id=user_data["customer_id"],
            executor_id=user_data["executor_id"]
        )
        db.session.add(new_order)
        db.session.commit()
        return 'new order created', 201


@app.route('/orders/<int:sid>', methods=['GET', 'PUT', 'DELETE'])
def page_order_sid(sid: int):
    if request.method == 'GET':
        order = Order.query.get(sid)
        if order is None:
            return "order not found"
        json_raw = {
            "id": order.id,
            "name": order.name,
            "description": order.description,
            "start_date": order.start_date,
            "end_date": order.end_date,
            "address": order.address,
            "price": order.price,
            "customer_id": order.customer_id,
            "executor_id": order.executor_id
        }
        return json_raw
    elif request.method == 'DELETE':
        o = Order.query.get(sid)
        db.session.delete(o)
        db.session.commit()
        return f'order {sid} deleted', 204
    elif request.method == 'PUT':
        user_data = json.loads(request.data)
        o = Order.query.get(sid)
        o.name = user_data['name']
        o.description = user_data['description']
        o.start_date = user_data['start_date']
        o.end_date = user_data['end_date']
        o.address = user_data['address']
        o.price = user_data['price']
        o.customer_id = user_data['customer_id']
        o.executor_id = user_data['executor_id']
        db.session.add(o)
        db.session.commit()
        return f'order {sid} updated', 204


@app.route('/offers/', methods=['GET', 'POST'])
def page_offers():
    if request.method == 'GET':
        offers = db.session.query(Offer).all()
        offer_response = []
        for offer in offers:
            offer_response.append(
                {
                    "id": offer.id,
                    "order_id": offer.order_id,
                    "executor_id": offer.executor_id
                })
        return json.dumps(offer_response)
    elif request.method == 'POST':
        user_data = json.loads(request.data)
        new_offer = Offer(
            order_id=user_data['order_id'],
            executor_id=user_data['executor_id']
        )
        db.session.add(new_offer)
        db.session.commit()
        return 'Предложение добавлено', 201


@app.route('/offers/<int:sid>', methods=['GET', 'PUT', 'DELETE'])
def page_offer_sid(sid: int):
    if request.method == 'GET':
        offer = Offer.query.get(sid)
        if offer is None:
            return "offer not found"

        return json.dumps(
            {
                "id": offer.id,
                "order_id": offer.order_id,
                "executor_id": offer.executor_id
            })
    elif request.method == 'DELETE':
        o = Offer.query.get(sid)
        db.session.delete(o)
        db.session.commit()
        return f'offer {sid} deleted', 204
    elif request.method == 'PUT':
        user_data = json.loads(request.data)
        of = Offer.query.get(int(sid))
        of.order_id = user_data['order_id']
        of.executor_id = user_data['executor_id']
        db.session.add(of)
        db.session.commit()
        return f'offer {sid} updated', 204


app.run()
