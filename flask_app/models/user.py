from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.hours = data['hours']
        self.pay = data['pay']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('db_coinclock').query_db(query,data)
    
    @staticmethod
    def validate_register(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters", "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if not user['password'] == user['password_confirm']:
            flash("Passwords do not match", "register")
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('db_coinclock').query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('db_coinclock').query_db(query,data)
        return cls(result[0])

    @classmethod
    def update_hours(cls,data):
        query = "UPDATE users SET hours = %(hours)s WHERE id = %(id)s;"
        return connectToMySQL('db_coinclock').query_db(query,data)

    @classmethod
    def update_pay(cls,data):
        query = "UPDATE users SET pay = %(pay)s WHERE id = %(id)s;"
        return connectToMySQL('db_coinclock').query_db(query,data)

    @classmethod
    def reset(cls,data):
        query = "UPDATE users SET hours = null, pay = null WHERE id = %(id)s;"
        return connectToMySQL('db_coinclock').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('db_coinclock').query_db(query,data)