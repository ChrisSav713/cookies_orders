from flask import Flask, render_template, redirect, request, url_for, session
from flask_app import app
from flask_app.models.order import Order

@app.route('/')
def index():
    return redirect('/cookies')

@app.route('/cookies')
def all_orders():
    orders = Order.get_all()
    return render_template('all_orders.html', orders=orders)

@app.route('/cookies/new')
def new_order():
    return render_template('new_order.html')

@app.route('/cookies/create', methods=['GET','POST'])
def create():
    data={
        "customer_name":request.form['customer_name'],
        "cookie_type":request.form['cookie_type'],
        "boxes":request.form['boxes']
    }
    if Order.validate_input(data):
        Order.save(data)
        return redirect('/')
    return redirect('/cookies/new')

@app.route('/cookies/update', methods=['GET','POST'])
def update_order():
    data={
        "id": request.form['id'],
        "customer_name": request.form['customer_name'],
        "cookie_type": request.form['cookie_type'],
        "boxes": request.form['boxes']
    }
    if Order.validate_input(data):
        Order.edit(data)
        return redirect('/')
    return redirect(f"/cookies/edit/{data['id']}")

@app.route('/cookies/edit/<int:id>')
def edit_order(id):
    data={
        "id":id
    }
    return render_template('change_order.html', order=Order.get_one(data))

@app.route('/cookies/delete/<int:id>')
def delete_order(id):
    data = {
        'id':id
    }
    Order.delete(data)
    return redirect('/')