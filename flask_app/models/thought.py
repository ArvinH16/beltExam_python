from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Thought:
    def __init__(self, data):
        self.id = data['id']
        self.thought = data['thought']
        self.likes = data['likes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def all_thoughts_with_creator(cls):
        query = "SELECT * FROM thoughts JOIN users ON users.id = thoughts.user_id;"
        result = connectToMySQL('thoughts').query_db(query)
        all_thoughts_with_creator = []

        for thought in result:
            one_thought = cls(thought)
            print(one_thought)

            thought_creator_info = {
                "id": thought['users.id'],
                "first_name": thought["first_name"],
                "last_name": thought["last_name"],
                "email": thought['email'],
                'password': thought['password'],
                'created_at': thought['created_at'],
                'updated_at': thought['updated_at']
            }

            creator = user.User(thought_creator_info)
            one_thought.creator = creator

            all_thoughts_with_creator.append(one_thought)

        return all_thoughts_with_creator


    @classmethod
    def add_thought(cls, data):
        query = "INSERT INTO thoughts(thought, likes, user_id) VALUES(%(thought)s, 0, %(user_id)s)"
        result = connectToMySQL('thoughts').query_db(query, data)
        return result

    @classmethod
    def delete_thought(cls, data):
        query = "DELETE FROM thoughts WHERE id = %(thought_id)s"
        result = connectToMySQL('thoughts').query_db(query, data)
        return result

    @classmethod
    def like(cls, data):
        query = "UPDATE thoughts SET likes = likes + 1 WHERE id = %(thought_id)s"
        result = connectToMySQL('thoughts').query_db(query, data)
        return result

    @classmethod
    def unlike(cls, data):
        query = "UPDATE thoughts SET likes = likes - 1 WHERE id = %(thought_id)s"
        result = connectToMySQL('thoughts').query_db(query, data)
        return result

    @staticmethod
    def validate_thought(data):
        is_valid = True

        if len(data['thought']) < 5:
            flash("Thought needs to be at least 5 characters long", "thought")
            is_valid = False
        
        return is_valid