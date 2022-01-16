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
        return render_template('users_id.html', json=json.dumps(user_response))
    elif request.method == 'POST' and not request.form.get('del') and not request.form.get('upd_id'):
        new_user = User(
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            age=request.form.get('age'),
            email=request.form.get('email'),
            role=request.form.get('role'),
            phone=request.form.get('phone')
        )
        db.session.add(new_user)
        db.session.commit()
        return 'пользователь добавлен', 201
    elif request.method == 'POST' and request.form.get('del'):
        sid = int(request.form.get('del'))
        user = User.query.get(sid)
        db.session.delete(user)
        db.session.commit()
        return f'пользователь {sid} удален', 201
    elif request.method == 'POST' and request.form.get('upd_id'):
        upd_id = int(request.form.get('upd_id'))
        upd_user = User.query.get(upd_id)
        upd_user.first_name = request.form.get('first_name')
        upd_user.last_name = request.form.get('last_name')
        upd_user.age = request.form.get('age')
        upd_user.email = request.form.get('email')
        upd_user.role = request.form.get('role')
        upd_user.phone = request.form.get('phone')

        db.session.add(upd_user)
        db.session.commit()
        return 'пользователь обновлен', 201


@app.route('/users/<int:sid>', methods=['GET'])
def page_users_sid(sid: int):
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
        return render_template('orders_id.html', json=order_response)
    if request.method == 'POST' and not request.form.get('del_ord') and not request.form.get('upd_ord_id'):
        new_order = Order(
            name=request.form.get('name'),
            description=request.form.get('description'),
            start_date=request.form.get('start_date'),
            end_date=request.form.get('end_date'),
            address=request.form.get('address'),
            price=request.form.get('price'),
            customer_id=request.form.get('customer_id'),
            executor_id=request.form.get('executor_id')
        )
        db.session.add(new_order)
        db.session.commit()
        return 'Ордер добавлен', 201
    if request.method == 'POST' and request.form.get('del_ord'):
        sid = int(request.form.get('del_ord'))
        order = Order.query.get(sid)
        db.session.delete(order)
        db.session.commit()
        return f'Ордер {sid} удален', 201
    if request.method == 'POST' and request.form.get('upd_ord_id'):
        upd_ord_id = int(request.form.get('upd_ord_id'))
        upd_ord = Order.query.get(upd_ord_id)
        upd_ord.name = request.form.get('name')
        upd_ord.description = request.form.get('description')
        upd_ord.start_date = request.form.get('start_date')
        upd_ord.end_date = request.form.get('end_date')
        upd_ord.address = request.form.get('address')
        upd_ord.price = request.form.get('price')
        upd_ord.customer_id = request.form.get('customer_id')
        upd_ord.executor_id = request.form.get('executor_id')


        db.session.add(upd_ord)
        db.session.commit()
        return 'Ордер обновлен', 201




@app.route('/orders/<int:sid>', methods=['GET'])
def page_order_sid(sid: int):
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
        "customer_is": order.customer_id,
        "executor_id": order.executor_id
    }
    return render_template('order.html', json=json_raw)


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
        return render_template('offers_id.html', json= json.dumps(offer_response))
    elif request.method == 'POST' and not request.form.get('del_offer_id') and not request.form.get('upd_offer_id'):
        new_offer = Offer(
            order_id=request.form.get('order_id'),
            executor_id=request.form.get('executor_id')
        )
        db.session.add(new_offer)
        db.session.commit()
        return 'Предложение добавлено', 201
    elif request.method == 'POST' and request.form.get('del_offer_id'):
        sid = int(request.form.get('del_offer_id'))
        offer = Offer.query.get(sid)
        db.session.delete(offer)
        db.session.commit()
        return f'Предложение {sid} удалено', 201
    elif request.method == 'POST' and request.form.get('upd_offer_id'):
        upd_offer_id = int(request.form.get('upd_offer_id'))
        upd_offer = Offer.query.get(upd_offer_id)
        upd_offer.order_id = request.form.get('order_id')
        upd_offer.executor_id = request.form.get('executor_id')

        db.session.add(upd_offer)
        db.session.commit()
        return 'Предложение обновлено', 201


@app.route('/offers/<int:sid>')
def page_offer_sid(sid: int):
    offer = Offer.query.get(sid)
    if offer is None:
        return "offer not found"

    return json.dumps(
        {
            "id": offer.id,
            "order_id": offer.order_id,
            "executor_id": offer.executor_id
        })


app.run()
