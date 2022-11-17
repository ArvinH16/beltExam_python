from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import thought
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.thought = []

    @classmethod
    def add_user(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, `password`) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result = connectToMySQL('thoughts').query_db(query, data)
        return result

    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('thoughts').query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def check_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('thoughts').query_db(query, data)
        if len(result) < 1:
            return False

        return cls(result[0])

    @classmethod
    def get_user_thoughts(cls, data):
        query = "SELECT * FROM thoughts LEFT JOIN users ON thoughts.user_id = users.id WHERE users.id = %(user_id)s"
        result = connectToMySQL('thoughts').query_db(query, data)
        one_creator = cls(result[0])
        
        for each in result:
            thought_data = {
                'id': each['id'],
                'thought': each['thought'],
                'likes': each['likes'],
                'created_at': each['created_at'],
                'updated_at': each['updated_at']
            }
            one_creator.thought.append(thought.Thought(thought_data))
        return one_creator

    @staticmethod
    def validate_registration(user):
        is_valid = True


        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('thoughts').query_db(query, user)
        if len(result) >= 1:
            flash("Email already taken", "register")
            is_valid = False

        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email", "register")
            is_valid = False

        if len(user["first_name"]) < 2:
            flash("First Name needs to be at least 2 characters", "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name needs to be at least 2 characters", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password needs to be at least 8 characters long", "register")
            is_valid = False
        
        if user['password'] != user['confirm_pass']:
            flash("Passwords are not matching", "register")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        if len(user['email']) < 1:
            flash("Email field is required", "login")
            is_valid = False
        if len(user['password']) < 1:
            flash("Password field is required", "login")
            is_valid = False
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email", "login")
            is_valid = False
        return is_valid