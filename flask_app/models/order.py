from dataclasses import dataclass
from flask_app.config.mysqlconnection import connectToMySQL
from flask import session, flash

class Order:
    def __init__(self,data):
        self.id = data['id']
        self.customer_name = data['customer_name']
        self.cookie_type = data['cookie_type']
        self.boxes = data['boxes']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM orders;"
        results = connectToMySQL('cookies_db').query_db(query)
        orders=[]
        for order_item in results:
            orders.append(cls(order_item))
        return orders

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM orders WHERE id = %(id)s;"
        result = connectToMySQL('cookies_db').query_db(query,data)
        return cls(result[0])

    @classmethod
    def save(cls, data):
        query = '''
        INSERT INTO orders ( customer_name, cookie_type, boxes, created_at, updated_at)
        VALUES (%(customer_name)s, %(cookie_type)s, %(boxes)s, NOW(), NOW());
        '''
        return connectToMySQL('cookies_db').query_db(query,data)
    
    @classmethod
    def edit(cls,data):
        query = '''
        UPDATE orders
        SET customer_name = %(customer_name)s,
        cookie_type = %(cookie_type)s,
        boxes = %(boxes)s,
        updated_at = NOW()
        WHERE id = %(id)s;
        '''
        return connectToMySQL('cookies_db').query_db(query,data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM orders WHERE id = %(id)s;'
        return connectToMySQL('cookies_db').query_db(query,data)

    @staticmethod
    def validate_input(order):
        is_valid = True
        if len(order['customer_name']) < 2:
            flash('Name must be at least two characters', 'customer_name')
            is_valid = False
        if len(order['cookie_type']) < 2:
            flash('Cookie type must be at least two characters', 'cookie_type')
            is_valid = False
        if int(order['boxes']) < 0:
            flash('Number of boxes must not be negative', 'boxes')
            is_valid = False
        return is_valid